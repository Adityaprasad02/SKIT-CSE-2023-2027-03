from dataclasses import dataclass


@dataclass(frozen=True)
class ResolvedSkill:
    skill_id: str
    name: str


@dataclass(frozen=True)
class JobRequirements:
    required_skills: tuple[ResolvedSkill, ...]
    preferred_skills: tuple[ResolvedSkill, ...]


@dataclass(frozen=True)
class MatchResult:
    score: float
    matched_required: tuple[ResolvedSkill, ...]
    missing_required: tuple[ResolvedSkill, ...]
    matched_preferred: tuple[ResolvedSkill, ...]
    missing_preferred: tuple[ResolvedSkill, ...]

    @property
    def matched_skills(self) -> tuple[ResolvedSkill, ...]:
        return self.matched_required + self.matched_preferred

    @property
    def missing_skills(self) -> tuple[ResolvedSkill, ...]:
        return self.missing_required + self.missing_preferred
