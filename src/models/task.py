"""Task domain model and enums."""

import uuid
from dataclasses import dataclass, field
from datetime import date, datetime
from enum import StrEnum


class TaskStatus(StrEnum):
    """Task status options."""

    PENDENTE = "Pendente"
    EM_ANDAMENTO = "Em Andamento"
    CONCLUIDA = "Concluída"
    ATRASADA = "Atrasada"


class TaskPriority(StrEnum):
    """Task priority levels."""

    BAIXA = "Baixa"
    MEDIA = "Média"
    ALTA = "Alta"


@dataclass
class Task:
    """Represents an academic task or deadline."""

    title: str
    subject_id: str
    subject_name: str
    due_date: date
    status: TaskStatus = TaskStatus.PENDENTE
    priority: TaskPriority = TaskPriority.MEDIA
    description: str = ""
    weight: float = 1.0
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    @property
    def is_overdue(self) -> bool:
        """Check if task is past due date and not completed."""
        return self.status != TaskStatus.CONCLUIDA and self.due_date < date.today()

    def update_computed_status(self) -> TaskStatus:
        """Update status based on completion and current date."""
        if self.status != TaskStatus.CONCLUIDA and self.due_date < date.today():
            self.status = TaskStatus.ATRASADA
        return self.status

    def to_dict(self) -> dict:
        """Convert task model to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "subject_id": self.subject_id,
            "subject_name": self.subject_name,
            "due_date": self.due_date.isoformat()
            if isinstance(self.due_date, date)
            else str(self.due_date),
            "status": self.status.value
            if isinstance(self.status, TaskStatus)
            else str(self.status),
            "priority": self.priority.value
            if isinstance(self.priority, TaskPriority)
            else str(self.priority),
            "description": self.description,
            "weight": self.weight,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Create task model from dictionary."""
        raw_date = data["due_date"]
        if isinstance(raw_date, str):
            due_date = datetime.strptime(raw_date, "%Y-%m-%d").date()
        else:
            due_date = raw_date

        status_val = data.get("status", TaskStatus.PENDENTE)
        if isinstance(status_val, str):
            status = TaskStatus(status_val)
        else:
            status = status_val

        priority_val = data.get("priority", TaskPriority.MEDIA)
        if isinstance(priority_val, str):
            priority = TaskPriority(priority_val)
        else:
            priority = priority_val

        return cls(
            id=data.get("id", str(uuid.uuid4())),
            title=data["title"],
            subject_id=data["subject_id"],
            subject_name=data["subject_name"],
            due_date=due_date,
            status=status,
            priority=priority,
            description=data.get("description", ""),
            weight=float(data.get("weight", 1.0)),
        )
