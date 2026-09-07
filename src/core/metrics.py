"""Academic progress and dashboard metrics calculations."""

from src.models.subject import Subject
from src.models.task import Task, TaskStatus


def calculate_dashboard_metrics(
    tasks: list[Task], subjects: list[Subject]
) -> dict[str, float | int]:
    """Calculate summary dashboard metrics.

    Returns:
        dict containing:
        - total_subjects (int)
        - total_tasks (int)
        - completed_tasks (int)
        - pending_tasks (int)
        - in_progress_tasks (int)
        - overdue_tasks (int)
        - completion_rate (float percentage 0-100)
    """
    total_subjects = len(subjects)
    total_tasks = len(tasks)

    if total_tasks == 0:
        return {
            "total_subjects": total_subjects,
            "total_tasks": 0,
            "completed_tasks": 0,
            "pending_tasks": 0,
            "in_progress_tasks": 0,
            "overdue_tasks": 0,
            "completion_rate": 0.0,
        }

    completed = sum(1 for t in tasks if t.status == TaskStatus.CONCLUIDA)
    pending = sum(1 for t in tasks if t.status == TaskStatus.PENDENTE)
    in_progress = sum(1 for t in tasks if t.status == TaskStatus.EM_ANDAMENTO)
    overdue = sum(1 for t in tasks if t.status == TaskStatus.ATRASADA or t.is_overdue)

    rate = round((completed / total_tasks) * 100.0, 1)

    return {
        "total_subjects": total_subjects,
        "total_tasks": total_tasks,
        "completed_tasks": completed,
        "pending_tasks": pending,
        "in_progress_tasks": in_progress,
        "overdue_tasks": overdue,
        "completion_rate": rate,
    }


def calculate_subject_progress(tasks: list[Task], subject_id: str) -> dict[str, float | int]:
    """Calculate task progress metrics for a specific subject."""
    subject_tasks = [t for t in tasks if t.subject_id == subject_id]
    total = len(subject_tasks)

    if total == 0:
        return {
            "total_tasks": 0,
            "completed_tasks": 0,
            "pending_tasks": 0,
            "overdue_tasks": 0,
            "completion_rate": 0.0,
        }

    completed = sum(1 for t in subject_tasks if t.status == TaskStatus.CONCLUIDA)
    pending = sum(
        1 for t in subject_tasks if t.status in (TaskStatus.PENDENTE, TaskStatus.EM_ANDAMENTO)
    )
    overdue = sum(1 for t in subject_tasks if t.status == TaskStatus.ATRASADA or t.is_overdue)
    rate = round((completed / total) * 100.0, 1)

    return {
        "total_tasks": total,
        "completed_tasks": completed,
        "pending_tasks": pending,
        "overdue_tasks": overdue,
        "completion_rate": rate,
    }
