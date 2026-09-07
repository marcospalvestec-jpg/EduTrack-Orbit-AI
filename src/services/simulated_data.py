"""Simulated data service layer for EduTrack AI MVP."""

from datetime import date, timedelta

from src.models.subject import Subject
from src.models.task import Task, TaskPriority, TaskStatus


def _get_initial_subjects() -> list[Subject]:
    """Return deterministic initial sample subjects."""
    return [
        Subject(
            id="sub-1",
            name="Algoritmos e Estrutura de Dados",
            code="CC101",
            professor="Prof. Carlos Silva",
            workload_hours=80,
            color_hex="#1A3644",
        ),
        Subject(
            id="sub-2",
            name="Cálculo I",
            code="MAT201",
            professor="Profa. Maria Oliveira",
            workload_hours=72,
            color_hex="#7C3AED",
        ),
        Subject(
            id="sub-3",
            name="Banco de Dados",
            code="CC203",
            professor="Prof. André Santos",
            workload_hours=60,
            color_hex="#10B981",
        ),
        Subject(
            id="sub-4",
            name="Engenharia de Software",
            code="CC304",
            professor="Profa. Renata Lima",
            workload_hours=60,
            color_hex="#F59E0B",
        ),
    ]


def _get_initial_tasks(reference_date: date | None = None) -> list[Task]:
    """Return deterministic initial sample tasks relative to reference_date."""
    ref = reference_date or date.today()
    return [
        Task(
            id="task-1",
            title="Implementar Tabela Hash em Python",
            subject_id="sub-1",
            subject_name="Algoritmos e Estrutura de Dados",
            due_date=ref - timedelta(days=2),
            status=TaskStatus.ATRASADA,
            priority=TaskPriority.ALTA,
            description="Entregar código e relatório de benchmark de colisões.",
            weight=2.0,
        ),
        Task(
            id="task-2",
            title="Estudo Dirigido: Árvores AVL",
            subject_id="sub-1",
            subject_name="Algoritmos e Estrutura de Dados",
            due_date=ref + timedelta(days=5),
            status=TaskStatus.PENDENTE,
            priority=TaskPriority.MEDIA,
            description="Resolver lista de exercícios de balanceamento.",
            weight=1.0,
        ),
        Task(
            id="task-3",
            title="Lista 3: Derivadas e Aplicações",
            subject_id="sub-2",
            subject_name="Cálculo I",
            due_date=ref - timedelta(days=1),
            status=TaskStatus.ATRASADA,
            priority=TaskPriority.ALTA,
            description="Resolver problemas 1 a 15 do capítulo 4.",
            weight=1.5,
        ),
        Task(
            id="task-4",
            title="Projeto 1: Modelagem ER do EduTrack",
            subject_id="sub-3",
            subject_name="Banco de Dados",
            due_date=ref - timedelta(days=5),
            status=TaskStatus.CONCLUIDA,
            priority=TaskPriority.ALTA,
            description="Diagrama Entidade-Relacionamento em SQL.",
            weight=2.5,
        ),
        Task(
            id="task-5",
            title="Consultas SQL Avançadas (JOINs e Group By)",
            subject_id="sub-3",
            subject_name="Banco de Dados",
            due_date=ref + timedelta(days=3),
            status=TaskStatus.EM_ANDAMENTO,
            priority=TaskPriority.MEDIA,
            description="Criar views e scripts de relatórios acadêmicos.",
            weight=1.5,
        ),
        Task(
            id="task-6",
            title="Especificação OpenSpec - Proposal Módulo 1",
            subject_id="sub-4",
            subject_name="Engenharia de Software",
            due_date=ref + timedelta(days=1),
            status=TaskStatus.EM_ANDAMENTO,
            priority=TaskPriority.ALTA,
            description="Elaborar proposal.md e spec.md para protótipo.",
            weight=3.0,
        ),
        Task(
            id="task-7",
            title="Revisão de Código em Par (Peer Review)",
            subject_id="sub-4",
            subject_name="Engenharia de Software",
            due_date=ref + timedelta(days=7),
            status=TaskStatus.PENDENTE,
            priority=TaskPriority.BAIXA,
            description="Auditar pull requests do grupo de trabalho.",
            weight=1.0,
        ),
        Task(
            id="task-8",
            title="Simulado Inicial de Cálculo I",
            subject_id="sub-2",
            subject_name="Cálculo I",
            due_date=ref - timedelta(days=10),
            status=TaskStatus.CONCLUIDA,
            priority=TaskPriority.MEDIA,
            description="Autoavaliação de limites e continuidade.",
            weight=1.0,
        ),
    ]


class SimulatedDataService:
    """Service providing in-memory and st.session_state simulated data."""

    def __init__(self, use_session_state: bool = True, reference_date: date | None = None):
        self.use_session_state = use_session_state
        self.reference_date = reference_date or date.today()
        self._subjects: list[Subject] = []
        self._tasks: list[Task] = []
        self._initialize_data()

    def _initialize_data(self) -> None:
        """Initialize data in session_state or memory."""
        import sys

        in_streamlit = "streamlit" in sys.modules

        if self.use_session_state and in_streamlit:
            import streamlit as st

            if "subjects" not in st.session_state:
                st.session_state["subjects"] = [s.to_dict() for s in _get_initial_subjects()]
            if "tasks" not in st.session_state:
                st.session_state["tasks"] = [
                    t.to_dict() for t in _get_initial_tasks(self.reference_date)
                ]

            self._subjects = [Subject.from_dict(s) for s in st.session_state["subjects"]]
            self._tasks = [Task.from_dict(t) for t in st.session_state["tasks"]]
        else:
            self._subjects = _get_initial_subjects()
            self._tasks = _get_initial_tasks(self.reference_date)

        self._update_computed_statuses()

    def _sync_to_session_state(self) -> None:
        """Sync internal list back to st.session_state if active."""
        import sys

        if self.use_session_state and "streamlit" in sys.modules:
            import streamlit as st

            st.session_state["subjects"] = [s.to_dict() for s in self._subjects]
            st.session_state["tasks"] = [t.to_dict() for t in self._tasks]

    def _update_computed_statuses(self) -> None:
        """Compute status changes (e.g. overdue tasks)."""
        today = date.today()
        for task in self._tasks:
            if task.status != TaskStatus.CONCLUIDA and task.due_date < today:
                task.status = TaskStatus.ATRASADA

    def get_subjects(self) -> list[Subject]:
        """Return list of all subjects."""
        return list(self._subjects)

    def get_subject_by_id(self, subject_id: str) -> Subject | None:
        """Find a subject by ID."""
        for s in self._subjects:
            if s.id == subject_id:
                return s
        return None

    def add_subject(self, subject: Subject) -> Subject:
        """Add a new subject."""
        self._subjects.append(subject)
        self._sync_to_session_state()
        return subject

    def get_tasks(self) -> list[Task]:
        """Return list of all tasks with updated statuses."""
        self._update_computed_statuses()
        return list(self._tasks)

    def add_task(self, task: Task) -> Task:
        """Add a new task."""
        self._tasks.append(task)
        self._sync_to_session_state()
        return task

    def toggle_task_status(self, task_id: str) -> Task | None:
        """Toggle task status between CONCLUIDA and PENDENTE/ATRASADA."""
        for task in self._tasks:
            if task.id == task_id:
                if task.status == TaskStatus.CONCLUIDA:
                    task.status = (
                        TaskStatus.ATRASADA if task.due_date < date.today() else TaskStatus.PENDENTE
                    )
                else:
                    task.status = TaskStatus.CONCLUIDA
                self._sync_to_session_state()
                return task
        return None

    def reset_to_defaults(self) -> None:
        """Reset dataset to initial deterministic values."""
        self._subjects = _get_initial_subjects()
        self._tasks = _get_initial_tasks(self.reference_date)
        self._update_computed_statuses()
        self._sync_to_session_state()
