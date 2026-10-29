from app.services.career_roles import CAREER_ROLES
from app.services.skill_gap_analyzer import normalize_skills, analyze_skill_gaps


def recommend_careers(candidate_skills, top_n=5):
    """
    Rank career roles by required and preferred skill matches.

    Returns recommendations with scores, matched skills, and skill gaps.
    """
    candidate = normalize_skills(candidate_skills)
    recommendations = []

    for role, profile in CAREER_ROLES.items():
        required = normalize_skills(profile.get("required_skills", set()))
        preferred = normalize_skills(profile.get("preferred_skills", set()))

        matched_required = sorted(candidate & required)
        missing_required = sorted(required - candidate)
        matched_preferred = sorted(candidate & preferred)
        missing_preferred = sorted(preferred - candidate)

        required_score = (
            len(matched_required) / len(required) * 100
            if required else 100.0
        )
        preferred_score = (
            len(matched_preferred) / len(preferred) * 100
            if preferred else 0.0
        )

        # Required skills carry more weight than preferred skills.
        overall_score = round(
            0.8 * required_score + 0.2 * preferred_score, 2
        )

        gap_analysis = analyze_skill_gaps(
            candidate_skills=candidate,
            required_skills=required,
            preferred_skills=preferred,
        )

        recommendations.append({
            "role": role,
            "match_percentage": overall_score,
            "required_skill_match_percentage": round(required_score, 2),
            "matched_required_skills": matched_required,
            "missing_required_skills": missing_required,
            "matched_preferred_skills": matched_preferred,
            "missing_preferred_skills": missing_preferred,
            "related_skill_matches": gap_analysis["related_skill_matches"],
            "prioritized_gaps": gap_analysis["prioritized_gaps"],
        })

    recommendations.sort(
        key=lambda item: (
            item["match_percentage"],
            item["required_skill_match_percentage"],
            item["role"],
        ),
        reverse=True,
    )

    return recommendations[:max(0, top_n)]
