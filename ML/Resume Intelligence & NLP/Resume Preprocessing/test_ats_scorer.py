from app.services.ats_scorer import calculate_ats_score


skill_match = 66.67
keyword_match = 61.54
semantic_similarity = 0.4674


result = calculate_ats_score(
    skill_match,
    keyword_match,
    semantic_similarity
)


print("\n========== ATS SCORING ==========\n")

print(
    f"Skill Match: "
    f"{result['skill_match_percentage']:.2f}%"
)

print(
    f"Keyword Match: "
    f"{result['keyword_match_percentage']:.2f}%"
)

print(
    f"Semantic Match: "
    f"{result['semantic_match_percentage']:.2f}%"
)

print(
    f"\nOverall ATS Score: "
    f"{result['ats_score']:.2f}%"
)