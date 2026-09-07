"""Subject domain model."""

import uuid
from dataclasses import dataclass, field


@dataclass
class Subject:
    """Represents an academic subject/discipline."""

    name: str
    code: str
    professor: str
    workload_hours: int
    color_hex: str = "#1A3644"
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
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Subject":
        """Create subject model from dictionary."""
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            name=data["name"],
            code=data["code"],
            professor=data.get("professor", "Não informado"),
            workload_hours=int(data.get("workload_hours", 60)),
            color_hex=data.get("color_hex", "#1A3644"),
        )
