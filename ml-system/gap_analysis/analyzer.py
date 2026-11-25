from benchmark.schemas.models import RoleBenchmark
from resume.preprocessing.pipeline import PreprocessedResume
from resume.skill_extraction.pipeline import extract_skills
from skills.resolver import SkillResolver
from skills.taxonomy import Taxonomy

from .models import GapItem, SkillGapReport


def _priority(importance: float, required: bool) -> str:
    if required and importance >= 0.8:
        return "critical"
    if required and importance >= 0.5:
        return "high"
    if importance >= 0.5:
        return "medium"
    return "low"


def analyze_resume_against_benchmark(
    resume: PreprocessedResume,
    benchmark: RoleBenchmark,
    resolver: SkillResolver,
    taxonomy: Taxonomy | None = None,
) -> SkillGapReport:
    """Calculate resume coverage for one role benchmark."""
    resume_skill_ids: set[str] = set()
    for extracted_skill in extract_skills(resume).skills:
        resolution = resolver.resolve(extracted_skill)
        if resolution is not None:
            resume_skill_ids.add(resolution["canonical_id"])

    matched: list[GapItem] = []
    missing: list[GapItem] = []
    covered_weight = 0.0
    total_weight = 0.0

    for requirement in benchmark.required_skills:
        skill = taxonomy.get_by_id(requirement.skill_id) if taxonomy else None
        name = skill.name if skill else requirement.skill_id
        present = requirement.skill_id in resume_skill_ids
        item = GapItem(
            skill_id=requirement.skill_id,
            name=name,
            importance=requirement.importance,
            required_level=requirement.required_level,
            required=requirement.required,
            present=present,
            priority=_priority(requirement.importance, requirement.required),
        )
        total_weight += requirement.importance
        if present:
            covered_weight += requirement.importance
            matched.append(item)
        else:
            missing.append(item)

    missing.sort(key=lambda item: (-item.importance, item.name.casefold()))
    matched.sort(key=lambda item: (-item.importance, item.name.casefold()))
    score = 100.0 * covered_weight / total_weight if total_weight else 0.0

    return SkillGapReport(
        benchmark_id=benchmark.benchmark_id,
        role=benchmark.role,
        score=round(score, 2),
        matched_skills=tuple(matched),
        missing_skills=tuple(missing),
    )
