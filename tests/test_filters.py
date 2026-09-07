"""Unit tests for Pandas task filtering."""

from datetime import date

from src.core.filters import filter_tasks_dataframe, tasks_to_dataframe
from src.models.task import Task, TaskStatus


def test_tasks_to_dataframe_empty():
    """Test empty tasks conversion."""
    df = tasks_to_dataframe([])
    assert df.empty
    assert "subject_id" in df.columns


def test_filter_tasks_dataframe_by_subject():
    """Test filtering by subject ID."""
    tasks = [
        Task(
            title="T1",
            subject_id="s1",
            subject_name="Mat1",
            due_date=date.today(),
            status=TaskStatus.PENDENTE,
        ),
        Task(
            title="T2",
            subject_id="s2",
            subject_name="Fis1",
            due_date=date.today(),
            status=TaskStatus.PENDENTE,
        ),
    ]
    df = tasks_to_dataframe(tasks)
    filtered = filter_tasks_dataframe(df, subject_ids=["s1"])
    assert len(filtered) == 1
    assert filtered.iloc[0]["subject_id"] == "s1"


def test_filter_tasks_dataframe_by_status():
    """Test filtering by task status."""
    tasks = [
        Task(
            title="T1",
            subject_id="s1",
            subject_name="Mat1",
            due_date=date.today(),
            status=TaskStatus.CONCLUIDA,
        ),
        Task(
            title="T2",
            subject_id="s1",
            subject_name="Mat1",
            due_date=date.today(),
            status=TaskStatus.PENDENTE,
        ),
    ]
    df = tasks_to_dataframe(tasks)
    filtered = filter_tasks_dataframe(df, statuses=["Concluída"])
    assert len(filtered) == 1
    assert filtered.iloc[0]["status"] == "Concluída"


def test_filter_tasks_dataframe_by_search_query():
    """Test text search matching in title/description."""
    tasks = [
        Task(
            title="Implementar Hash",
            subject_id="s1",
            subject_name="Algo",
            due_date=date.today(),
            description="Python code",
        ),
        Task(
            title="Lista Derivadas",
            subject_id="s2",
            subject_name="Calc",
            due_date=date.today(),
            description="Math problems",
        ),
    ]
    df = tasks_to_dataframe(tasks)
    filtered = filter_tasks_dataframe(df, search_query="hash")
    assert len(filtered) == 1
    assert filtered.iloc[0]["title"] == "Implementar Hash"
