"""Unit tests for SimulatedDataService state management."""

from datetime import date

from src.models.subject import Subject
from src.models.task import Task
from src.services.simulated_data import SimulatedDataService


def test_simulated_data_service_initialization():
    """Test service initialization in plain python environment."""
    service = SimulatedDataService(use_session_state=False)
    subjects = service.get_subjects()
    tasks = service.get_tasks()

    assert len(subjects) >= 4
    assert len(tasks) >= 8


def test_simulated_data_service_toggle_task_status():
    """Test toggling task completion state."""
    service = SimulatedDataService(use_session_state=False)
    tasks = service.get_tasks()
    first_task = tasks[0]
    initial_status = first_task.status

    toggled = service.toggle_task_status(first_task.id)
    assert toggled is not None
    assert toggled.status != initial_status


def test_new_user_starts_with_empty_academic_data():
    """New accounts must not inherit demonstration records."""
    service = SimulatedDataService(use_session_state=False, seed_demo=False)

    assert service.get_subjects() == []
    assert service.get_tasks() == []


def test_subject_update_keeps_task_name_in_sync():
    """Renaming a subject updates the cached label shown by its tasks."""
    service = SimulatedDataService(use_session_state=False, seed_demo=False)
    subject = service.add_subject(Subject("Banco de Dados", "BD1", "Prof. Ana", 60))
    service.add_task(
        Task(
            title="Modelo relacional",
            subject_id=subject.id,
            subject_name=subject.name,
            due_date=date.today(),
        )
    )

    service.update_subject(subject.id, name="Banco de Dados Avançado")

    assert service.get_subject_by_id(subject.id).name == "Banco de Dados Avançado"
    assert service.get_tasks()[0].subject_name == "Banco de Dados Avançado"


def test_subject_delete_cascades_to_tasks():
    """Deleting a subject also removes its dependent tasks."""
    service = SimulatedDataService(use_session_state=False, seed_demo=False)
    subject = service.add_subject(Subject("Cálculo", "MAT1", "Prof. Bia", 80))
    task = service.add_task(
        Task(
            title="Lista de derivadas",
            subject_id=subject.id,
            subject_name=subject.name,
            due_date=date.today(),
        )
    )

    assert service.delete_subject(subject.id) is True
    assert service.get_subjects() == []
    assert service.get_task_by_id(task.id) is None


def test_task_can_be_updated_and_deleted():
    """Task edit and delete operations persist in the service."""
    service = SimulatedDataService(use_session_state=False, seed_demo=False)
    subject = service.add_subject(Subject("Redes", "RED1", "Prof. Caio", 40))
    task = service.add_task(
        Task(
            title="Trabalho inicial",
            subject_id=subject.id,
            subject_name=subject.name,
            due_date=date.today(),
        )
    )

    updated = service.update_task(task.id, title="Trabalho revisado")

    assert updated is not None
    assert updated.title == "Trabalho revisado"
    assert service.delete_task(task.id) is True
    assert service.get_tasks() == []
