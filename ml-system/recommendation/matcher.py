from resume.preprocessing.pipeline import PreprocessedResume
from resume.skill_extraction.pipeline import extract_skills
from skills.resolver import SkillResolver
from skills.taxonomy import Taxonomy

from .job_parser import _resolve_skill, parse_job_description
from .models import MatchResult, ResolvedSkill


def _partition_skills(
    requirements: tuple[ResolvedSkill, ...],
    resume_skill_ids: set[str],
) -> tuple[tuple[ResolvedSkill, ...], tuple[ResolvedSkill, ...]]:
    matched = tuple(skill for skill in requirements if skill.skill_id in resume_skill_ids)
    missing = tuple(skill for skill in requirements if skill.skill_id not in resume_skill_ids)
    return matched, missing


def match_resume_to_job(
    resume: PreprocessedResume,
    job_description: str,
    resolver: SkillResolver,
    taxonomy: Taxonomy | None = None,
) -> MatchResult:
    """Score a preprocessed resume against required and preferred job skills."""
    requirements = parse_job_description(job_description, resolver, taxonomy)
    resume_skill_ids = {
        resolved.skill_id
        for skill_name in extract_skills(resume).skills
        if (resolved := _resolve_skill(skill_name, resolver, taxonomy)) is not None
    }

    matched_required, missing_required = _partition_skills(
        requirements.required_skills,
        resume_skill_ids,
    )
    matched_preferred, missing_preferred = _partition_skills(
        requirements.preferred_skills,
        resume_skill_ids,
    )

    required_coverage = (
        len(matched_required) / len(requirements.required_skills)
        if requirements.required_skills
        else 0.0
    )
    preferred_coverage = (
        len(matched_preferred) / len(requirements.preferred_skills)
        if requirements.preferred_skills
        else 0.0
    )

    if requirements.required_skills and requirements.preferred_skills:
        score = 80 * required_coverage + 20 * preferred_coverage
    elif requirements.required_skills:
        score = 100 * required_coverage
    elif requirements.preferred_skills:
        score = 100 * preferred_coverage
    else:
        score = 0.0

    return MatchResult(
        score=round(score, 2),
        matched_required=matched_required,
        missing_required=missing_required,
        matched_preferred=matched_preferred,
        missing_preferred=missing_preferred,
    )
