from dataclasses import dataclass, field
from typing import Any


VALID_PROFICIENCY_LEVELS = {
    "beginner",
    "intermediate",
    "advanced",
    "expert",
}


@dataclass
class SkillRequirement:
    """A skill required by a role benchmark."""

    skill_id: str
    importance: float = 1.0
    required: bool = True
    required_level: str | None = None

    def __post_init__(self) -> None:
        self.skill_id = self.skill_id.strip()

        if not self.skill_id:
            raise ValueError("skill_id cannot be empty.")

        if not 0.0 <= self.importance <= 1.0:
            raise ValueError("importance must be between 0.0 and 1.0.")

        if self.required_level is not None:
            self.required_level = self.required_level.lower().strip()

            if self.required_level not in VALID_PROFICIENCY_LEVELS:
                raise ValueError(
                    f"Invalid required_level: {self.required_level}"
                )


@dataclass
class RoleBenchmark:
    """Structured skill requirements for a job role."""

    benchmark_id: str
    role: str
    required_skills: list[SkillRequirement]

    company: str | None = None
    source: str | None = None
    description: str | None = None
    version: int = 1
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.benchmark_id = self.benchmark_id.strip()
        self.role = self.role.strip()

        if not self.benchmark_id:
            raise ValueError("benchmark_id cannot be empty.")

        if not self.role:
            raise ValueError("role cannot be empty.")

        if self.version < 1:
            raise ValueError("version must be at least 1.")

        if not self.required_skills:
            raise ValueError(
                "A benchmark must contain at least one skill requirement."
            )

        skill_ids = [item.skill_id for item in self.required_skills]

        if len(skill_ids) != len(set(skill_ids)):
            raise ValueError(
                "Duplicate skill IDs are not allowed in a benchmark."
            )

    def validate_taxonomy(self, taxonomy: Any) -> None:
        """Raise an error if a required skill ID is absent from the taxonomy."""

        unknown_ids = [
            item.skill_id
            for item in self.required_skills
            if taxonomy.get_by_id(item.skill_id) is None
        ]

        if unknown_ids:
            raise ValueError(
                f"Unknown skill IDs in benchmark: {unknown_ids}"
            )

    def to_dict(self) -> dict[str, Any]:
        """Convert the benchmark into a JSON-serializable dictionary."""

        return {
            "benchmark_id": self.benchmark_id,
            "role": self.role,
            "company": self.company,
            "source": self.source,
            "description": self.description,
            "version": self.version,
            "required_skills": [
                {
                    "skill_id": item.skill_id,
                    "importance": item.importance,
                    "required": item.required,
                    "required_level": item.required_level,
                }
                for item in self.required_skills
            ],
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "RoleBenchmark":
        """Build a benchmark from a dictionary, such as a JSON record."""

        skills = [
            SkillRequirement(**item)
            for item in data["required_skills"]
        ]

        return cls(
            benchmark_id=data["benchmark_id"],
            role=data["role"],
            required_skills=skills,
            company=data.get("company"),
            source=data.get("source"),
            description=data.get("description"),
            version=data.get("version", 1),
            metadata=data.get("metadata", {}),
        )
