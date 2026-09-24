from dataclasses import dataclass, field


@dataclass(frozen=True)
class SkillMatch:
    """
    A single skill detected in a resume.
    """

    skill: str
    matched_text: str
    source_section: str
    method: str
    confidence: float


@dataclass
class SkillExtractionResult:
    """
    Final output of the skill extraction pipeline.
    """

    skills: list[str] = field(default_factory=list)
    matches: list[SkillMatch] = field(default_factory=list)
    by_section: dict[str, list[str]] = field(default_factory=dict)