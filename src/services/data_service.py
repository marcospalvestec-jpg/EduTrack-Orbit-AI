"""Select local or Xano-backed academic data for the current session."""

from __future__ import annotations

from typing import Any

from src.core.auth_session import AUTH_TOKEN_KEY
from src.models.subject import Subject
from src.models.task import Task
from src.services.demo_auth import DEMO_EMAIL
from src.services.simulated_data import SimulatedDataService
from src.services.xano import XanoClient, XanoError, configured_xano_base_url


class XanoSubjectDataService:
    """Persist subjects in Xano while tasks remain local during migration."""

    is_remote = True

    def __init__(
        self, base_url: str, token: str, user_id: str, use_session_state: bool = True
    ) -> None:
        self.client = XanoClient(base_url)
        self.token = token
        self.local_tasks = SimulatedDataService(
            user_id=user_id, seed_demo=False, use_session_state=use_session_state
        )

    def get_subjects(self) -> list[Subject]:
        """Return all subjects owned by the authenticated Xano user."""
        response = self.client.request("GET", "subjects?page=1&per_page=100", token=self.token)
        if isinstance(response, dict):
            records = response.get("items", [])
        else:
            records = response
        if not isinstance(records, list):
            return []
        return [Subject.from_dict(record) for record in records if isinstance(record, dict)]

    def get_subject_by_id(self, subject_id: str) -> Subject | None:
        """Return one subject from Xano."""
        response = self.client.request("GET", f"subjects/{subject_id}", token=self.token)
        return Subject.from_dict(response) if isinstance(response, dict) else None

    def add_subject(self, subject: Subject) -> Subject:
        """Create a subject in Xano."""
        response = self.client.request(
            "POST",
            "subjects",
            token=self.token,
            payload={
                "name": subject.name,
                "code": subject.code,
                "professor": subject.professor,
                "workload_hours": subject.workload_hours,
                "color_hex": subject.color_hex,
            },
        )
        if not isinstance(response, dict):
            raise ValueError("O Xano não retornou a disciplina criada.")
        return Subject.from_dict(response)

    def update_subject(self, subject_id: str, **changes: object) -> Subject | None:
        """Update a subject in Xano and synchronize local task labels."""
        allowed = {"name", "code", "professor", "workload_hours", "color_hex"}
        payload = {key: value for key, value in changes.items() if key in allowed}
        response = self.client.request(
            "PATCH", f"subjects/{subject_id}", token=self.token, payload=payload
        )
        if not isinstance(response, dict):
            return None
        updated = Subject.from_dict(response)
        for task in self.local_tasks.get_tasks():
            if str(task.subject_id) == str(subject_id):
                self.local_tasks.update_task(task.id, subject_name=updated.name)
        return updated

    def delete_subject(self, subject_id: str) -> bool:
        """Delete a subject in Xano and discard its temporary local tasks."""
        self.client.request("DELETE", f"subjects/{subject_id}", token=self.token)
        for task in self.local_tasks.get_tasks():
            if str(task.subject_id) == str(subject_id):
                self.local_tasks.delete_task(task.id)
        return True

    def get_tasks(self) -> list[Task]:
        """Return tasks from the local layer until task migration is enabled."""
        return self.local_tasks.get_tasks()

    def get_task_by_id(self, task_id: str) -> Task | None:
        return self.local_tasks.get_task_by_id(task_id)

    def add_task(self, task: Task) -> Task:
        return self.local_tasks.add_task(task)

    def update_task(self, task_id: str, **changes: object) -> Task | None:
        return self.local_tasks.update_task(task_id, **changes)

    def delete_task(self, task_id: str) -> bool:
        return self.local_tasks.delete_task(task_id)

    def toggle_task_status(self, task_id: str) -> Task | None:
        return self.local_tasks.toggle_task_status(task_id)


def data_service_for_user(user: dict[str, Any]):
    """Return the Xano service for authenticated sessions, otherwise local data."""
    import streamlit as st

    base_url = configured_xano_base_url()
    token = st.session_state.get(AUTH_TOKEN_KEY)
    if base_url and isinstance(token, str) and token:
        return XanoSubjectDataService(base_url, token, str(user["email"]))
    return SimulatedDataService(
        user_id=str(user["email"]), seed_demo=user.get("email") == DEMO_EMAIL
    )


def load_academic_data(service) -> tuple[list[Subject], list[Task]]:
    """Load page data and show a friendly message when Xano is unavailable."""
    try:
        return service.get_subjects(), service.get_tasks()
    except XanoError as error:
        import streamlit as st

        st.error(f"Não foi possível carregar seus dados no Xano: {error}")
        st.info("Tente atualizar a página. Se o problema continuar, entre novamente.")
        st.stop()
