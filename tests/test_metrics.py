"""Unit tests for dashboard metrics calculation functions."""

from datetime import date

from src.core.metrics import calculate_dashboard_metrics, calculate_subject_progress
from src.models.subject import Subject
from src.models.task import Task, TaskStatus


def test_calculate_dashboard_metrics_empty():
    """Test metrics calculation with empty dataset."""
    metrics = calculate_dashboard_metrics([], [])
    assert metrics["total_subjects"] == 0
    assert metrics["total_tasks"] == 0
    assert metrics["completion_rate"] == 0.0


def test_calculate_dashboard_metrics_non_empty():
    """Test metrics with sample subjects and tasks."""
    subjects = [
        Subject(name="Matemática", code="MAT", professor="A", workload_hours=60, id="s1"),
        Subject(name="Física", code="FIS", professor="B", workload_hours=60, id="s2"),
    ]
    tasks = [
        Task(
            title="T1",
            subject_id="s1",
            subject_name="Matemática",
            due_date=date.today(),
            status=TaskStatus.CONCLUIDA,
        ),
        Task(
            title="T2",
            subject_id="s1",
            subject_name="Matemática",
            due_date=date.today(),
            status=TaskStatus.PENDENTE,
        ),
        Task(
            title="T3",
            subject_id="s2",
            subject_name="Física",
            due_date=date.today(),
            status=TaskStatus.EM_ANDAMENTO,
        ),
        Task(
            title="T4",
            subject_id="s2",
            subject_name="Física",
            due_date=date.today(),
            status=TaskStatus.ATRASADA,
        ),
    ]

    m = calculate_dashboard_metrics(tasks, subjects)
    assert m["total_subjects"] == 2
    assert m["total_tasks"] == 4
    assert m["completed_tasks"] == 1
    assert m["pending_tasks"] == 1
    assert m["in_progress_tasks"] == 1
    assert m["overdue_tasks"] == 1
    assert m["completion_rate"] == 25.0


def test_calculate_subject_progress():
    """Test progress calculation for a specific subject."""
    tasks = [
        Task(
            title="T1",
            subject_id="s1",
            subject_name="Matemática",
            due_date=date.today(),
            status=TaskStatus.CONCLUIDA,
        ),
        Task(
            title="T2",
            subject_id="s1",
            subject_name="Matemática",
            due_date=date.today(),
            status=TaskStatus.CONCLUIDA,
        ),
        Task(
            title="T3",
            subject_id="s2",
            subject_name="Física",
            due_date=date.today(),
            status=TaskStatus.PENDENTE,
        ),
    ]

    p1 = calculate_subject_progress(tasks, "s1")
    assert p1["total_tasks"] == 2
    assert p1["completed_tasks"] == 2
    assert p1["completion_rate"] == 100.0

    p2 = calculate_subject_progress(tasks, "s2")
    assert p2["total_tasks"] == 1
    assert p2["completed_tasks"] == 0
    assert p2["completion_rate"] == 0.0
