def calculate_ats_score(
    skill_match_percentage: float,
    keyword_match_percentage: float,
    semantic_similarity: float
) -> dict:
    """
    Calculate the overall ATS score.

    Weights:
    Skill Match: 50%
    Keyword Match: 20%
    Semantic Match: 30%
    """

    semantic_percentage = semantic_similarity * 100

    skill_score = skill_match_percentage * 0.50
    keyword_score = keyword_match_percentage * 0.20
    semantic_score = semantic_percentage * 0.30

    ats_score = (
        skill_score
        + keyword_score
        + semantic_score
    )

    return {
        "skill_match_percentage": round(
            skill_match_percentage, 2
        ),
        "keyword_match_percentage": round(
            keyword_match_percentage, 2
        ),
        "semantic_match_percentage": round(
            semantic_percentage, 2
        ),
        "ats_score": round(
            ats_score, 2
        )
    }