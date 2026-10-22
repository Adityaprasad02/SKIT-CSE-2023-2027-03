import re

from resume.skill_extraction.dictionary_extractor import (
    extract_dictionary_skills,
)
from skills.resolver import SkillResolver
from skills.taxonomy import Taxonomy

from .models import JobRequirements, ResolvedSkill


PREFERRED_MARKERS = re.compile(
    r"\b(preferred|preferably|nice[- ]to[- ]have|bonus|desired|a plus)\b",
    re.IGNORECASE,
)
REQUIRED_MARKERS = re.compile(
    r"\b(required|must[- ]have|minimum qualifications?|basic qualifications?|"
    r"what you(?:'|’)ll need|what you(?:'|’)ll bring)\b",
    re.IGNORECASE,
)


def _resolve_skill(
    skill_name: str,
    resolver: SkillResolver,
    taxonomy: Taxonomy | None,
) -> ResolvedSkill | None:
    resolution = resolver.resolve(skill_name)
    if resolution is None:
        return None

    skill_id = resolution["canonical_id"]
    canonical_skill = taxonomy.get_by_id(skill_id) if taxonomy else None
    return ResolvedSkill(
        skill_id=skill_id,
        name=canonical_skill.name if canonical_skill else skill_name,
    )


def parse_job_description(
    text: str,
    resolver: SkillResolver,
    taxonomy: Taxonomy | None = None,
) -> JobRequirements:
    """Extract taxonomy-backed skills, treating unmarked requirements as required."""
    if not isinstance(text, str):
        raise TypeError("Job description must be a string")

    preferred: dict[str, ResolvedSkill] = {}
    required: dict[str, ResolvedSkill] = {}
    preferred_section = False

    for line in text.splitlines():
        if PREFERRED_MARKERS.search(line):
            preferred_section = True
        elif REQUIRED_MARKERS.search(line):
            preferred_section = False

        destination = preferred if preferred_section else required
        matches = extract_dictionary_skills(line, source_section="job_description")
        matches.sort(
            key=lambda match: line.casefold().find(match.matched_text.casefold())
        )
        for match in matches:
            skill = _resolve_skill(match.skill, resolver, taxonomy)
            if skill is not None:
                destination.setdefault(skill.skill_id, skill)

    for skill_id in required:
        preferred.pop(skill_id, None)

    return JobRequirements(
        required_skills=tuple(required.values()),
        preferred_skills=tuple(preferred.values()),
    )
