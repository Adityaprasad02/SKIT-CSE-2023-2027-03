from dataclasses import dataclass


@dataclass(frozen=True)
class GapItem:
    skill_id: str
    name: str
    importance: float
    required_level: str | None
    required: bool
    present: bool
    priority: str


@dataclass(frozen=True)
class SkillGapReport:
    benchmark_id: str
    role: str
    score: float
    matched_skills: tuple[GapItem, ...]
    missing_skills: tuple[GapItem, ...]

    @property
    def all_skills(self) -> tuple[GapItem, ...]:
        return self.matched_skills + self.missing_skills
