"""Unit tests for Subject and Task data models."""

from datetime import date, timedelta

from src.models.subject import Subject
from src.models.task import Task, TaskPriority, TaskStatus


def test_subject_serialization():
    """Test Subject creation and dictionary conversion."""
    subj = Subject(
        id="sub-test-1",
        name="Cálculo I",
        code="MAT101",
        professor="Prof. Teste",
        workload_hours=60,
        color_hex="#1A3644",
    )

    data = subj.to_dict()
    assert data["id"] == "sub-test-1"
    assert data["name"] == "Cálculo I"
    assert data["code"] == "MAT101"

    deserialized = Subject.from_dict(data)
    assert deserialized.name == subj.name
    assert deserialized.workload_hours == 60


def test_task_status_computed_overdue():
    """Test task overdue logic."""
    yesterday = date.today() - timedelta(days=1)
    task = Task(
        title="Entrega Atrasada",
        subject_id="sub-1",
        subject_name="Algoritmos",
        due_date=yesterday,
        status=TaskStatus.PENDENTE,
    )

    assert task.is_overdue is True
    updated_status = task.update_computed_status()
    assert updated_status == TaskStatus.ATRASADA
    assert task.status == TaskStatus.ATRASADA


def test_task_serialization():
    """Test Task dictionary conversion and deserialization."""
    today = date.today()
    task = Task(
        id="task-test-100",
        title="Projeto Final",
        subject_id="sub-10",
        subject_name="Engenharia de Software",
        due_date=today,
        status=TaskStatus.EM_ANDAMENTO,
        priority=TaskPriority.ALTA,
        description="Fazer testes",
    )

    d = task.to_dict()
    assert d["id"] == "task-test-100"
    assert d["status"] == "Em Andamento"
    assert d["priority"] == "Alta"

    rebuilt = Task.from_dict(d)
    assert rebuilt.id == task.id
    assert rebuilt.status == TaskStatus.EM_ANDAMENTO
    assert rebuilt.priority == TaskPriority.ALTA
    assert rebuilt.due_date == today
