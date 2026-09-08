"""Subject domain model."""

import uuid
from dataclasses import dataclass, field
from datetime import date, timedelta


@dataclass
class Subject:
    """Represents an academic subject/discipline."""

    name: str
    code: str
    professor: str
    workload_hours: int
    color_hex: str = "#1A3644"
    description: str = ""
    start_date: date = field(default_factory=date.today)
    end_date: date = field(default_factory=lambda: date.today() + timedelta(days=120))
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_dict(self) -> dict:
        """Convert subject model to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "professor": self.professor,
            "workload_hours": self.workload_hours,
            "color_hex": self.color_hex,
            "description": self.description,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Subject":
        """Create subject model from dictionary."""
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            name=data["name"],
            code=data.get("code") or "",
            professor=data.get("professor", "Não informado"),
            workload_hours=int(data.get("workload_hours", 60)),
            color_hex=data.get("color_hex") or "#1A3644",
            description=data.get("description") or "",
            start_date=date.fromisoformat(data["start_date"])
            if data.get("start_date")
            else date.today(),
            end_date=date.fromisoformat(data["end_date"])
            if data.get("end_date")
            else date.today() + timedelta(days=120),
        )
