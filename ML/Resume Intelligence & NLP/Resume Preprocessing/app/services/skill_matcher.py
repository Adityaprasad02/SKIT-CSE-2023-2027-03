def normalize_skill(skill: str) -> str:
    """Normalize skill names for comparison."""

    skill = skill.lower().strip()

    aliases = {
        "rest apis": "rest api",
        "restful api": "rest api",
        "restful apis": "rest api",
        "apis": "api",
        "object oriented programming": "oop",
        "oops": "oop",
    }

    return aliases.get(skill, skill)


def calculate_skill_match(
    resume_skills: list[str],
    required_skills: list[str]
) -> dict:
    """
    Compare resume skills with skills required
    by the job description.
    """

    resume_normalized = {
        normalize_skill(skill): skill
        for skill in resume_skills
    }

    matched_skills = []
    missing_skills = []

    for required_skill in required_skills:

        normalized_required = normalize_skill(
            required_skill
        )

        if normalized_required in resume_normalized:
            matched_skills.append(
                resume_normalized[normalized_required]
            )
        else:
            missing_skills.append(required_skill)

    total_required = len(required_skills)
    total_matched = len(matched_skills)

    if total_required > 0:
        match_percentage = (
            total_matched / total_required
        ) * 100
    else:
        match_percentage = 0.0

    return {
        "matched_skills": sorted(set(matched_skills)),
        "missing_skills": sorted(set(missing_skills)),
        "skill_match_percentage": round(
            match_percentage,
            2
        )
    }