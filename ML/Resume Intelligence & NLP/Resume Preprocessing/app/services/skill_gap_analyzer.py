from app.services.skill_extractor import SKILL_ALIASES as EXTRACTOR_ALIASES
from app.services.skill_dictionary import (
    RELATED_SKILLS,
    SKILL_ALIASES as ALIAS_GROUPS,
)


def normalize_skills(skills) -> set[str]:
    if not skills:
        return set()

    if isinstance(skills, dict):
        values = []
        for category_skills in skills.values():
            if isinstance(category_skills, (list, set, tuple)):
                values.extend(category_skills)
        skills = values

    if isinstance(skills, str):
        skills = [skills]

    alias_map = {}

    # Original extractor format: alias -> canonical skill
    for alias, canonical in EXTRACTOR_ALIASES.items():
        alias_map[str(alias).strip().lower()] = str(canonical).strip().lower()

    # Dictionary format: canonical skill -> set/list of aliases
    for canonical, aliases in ALIAS_GROUPS.items():
        canonical_name = str(canonical).strip().lower()
        alias_map[canonical_name] = canonical_name

        if isinstance(aliases, str):
            aliases = [aliases]

        for alias in aliases:
            alias_map[str(alias).strip().lower()] = canonical_name

    normalized = set()

    for skill in skills:
        value = str(skill).strip().lower()
        if value:
            normalized.add(alias_map.get(value, value))

    return normalized
def analyze_skill_gaps(
    candidate_skills,
    required_skills,
    preferred_skills=None,
) -> dict:
    """Compare candidate skills with required and preferred job skills."""
    candidate = normalize_skills(candidate_skills)
    required = normalize_skills(required_skills)
    preferred = normalize_skills(preferred_skills)

    matched_required = sorted(candidate & required)
    missing_required = sorted(required - candidate)
    matched_preferred = sorted(candidate & preferred)
    missing_preferred = sorted(preferred - candidate)

    related_matches = []

    for skill in missing_required:
        related = {
            str(item).strip().lower()
            for item in RELATED_SKILLS.get(skill, set())
        }
        candidate_related = sorted(candidate & related)

        if candidate_related:
            related_matches.append({
                "required_skill": skill,
                "related_candidate_skills": candidate_related,
            })

    prioritized_gaps = [
        {
            "skill": skill,
            "priority": "high",
            "reason": "Required by the job description but not detected in the resume.",
        }
        for skill in missing_required
    ]

    prioritized_gaps.extend(
        {
            "skill": skill,
            "priority": "medium",
            "reason": "Preferred by the job description but not detected in the resume.",
        }
        for skill in missing_preferred
    )

    recommendations = []

    if missing_required:
        recommendations.append(
            "Prioritize learning and demonstrating missing required skills: "
            + ", ".join(missing_required) + "."
        )

    if missing_preferred:
        recommendations.append(
            "Consider developing familiarity with preferred skills: "
            + ", ".join(missing_preferred) + "."
        )

    if related_matches:
        recommendations.append(
            "Highlight transferable skills where they genuinely support the job requirements."
        )

    if not prioritized_gaps:
        recommendations.append(
            "No skill gaps were detected in the supplied lists. Verify both inputs are complete."
        )

    match_percentage = (
        round(len(matched_required) / len(required) * 100, 2)
        if required else 100.0
    )

    return {
        "matched_required_skills": matched_required,
        "missing_required_skills": missing_required,
        "matched_preferred_skills": matched_preferred,
        "missing_preferred_skills": missing_preferred,
        "related_skill_matches": related_matches,
        "prioritized_gaps": prioritized_gaps,
        "required_skill_match_percentage": match_percentage,
        "recommendations": recommendations,
    }
