def get_match_category(ats_score: float) -> str:
    """Classify the job match based on ATS score."""

    if ats_score >= 80:
        return "Excellent Match"

    if ats_score >= 60:
        return "Good Match"

    if ats_score >= 40:
        return "Moderate Match"

    return "Low Match"


def generate_match_recommendation(ats_score: float) -> str:
    """Generate a simple recommendation."""

    if ats_score >= 80:
        return "Strongly recommended for this job."

    if ats_score >= 60:
        return "Good match, but some improvements may help."

    if ats_score >= 40:
        return "Resume needs improvement for this job."

    return "Resume has a low match with this job."


def generate_job_match(ats_score: float) -> dict:
    """Generate the final job match result."""

    category = get_match_category(ats_score)
    recommendation = generate_match_recommendation(
        ats_score
    )

    return {
        "ats_score": round(ats_score, 2),
        "match_category": category,
        "recommendation": recommendation
    }