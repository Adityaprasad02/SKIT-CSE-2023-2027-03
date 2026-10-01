from app.services.job_matcher import generate_job_match


ats_score = 59.66


result = generate_job_match(ats_score)


print("\n========== JOB MATCH RESULT ==========\n")

print(
    f"ATS Score: "
    f"{result['ats_score']:.2f}%"
)

print(
    f"Match Category: "
    f"{result['match_category']}"
)

print(
    f"Recommendation: "
    f"{result['recommendation']}"
)