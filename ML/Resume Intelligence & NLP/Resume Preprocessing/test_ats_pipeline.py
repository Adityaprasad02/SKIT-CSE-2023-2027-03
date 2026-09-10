from app.services.ats_pipeline import analyze_resume_for_job


file_path = "sample_resume.pdf"

job_description = """
We are looking for an Android Developer with experience
in Kotlin, Java, Android, MVVM, REST APIs, Retrofit,
Coroutines and mobile application development.
"""


result = analyze_resume_for_job(
    file_path,
    job_description
)


print("\n========== FINAL ATS ANALYSIS ==========\n")

print("Required Skills:")
print(", ".join(result["required_skills"]))

print("\nMatched Skills:")
print(", ".join(result["matched_skills"]))

print("\nMissing Skills:")
print(", ".join(result["missing_skills"]))

print(
    f"\nSkill Match: "
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

print(
    f"Match Category: "
    f"{result['match_category']}"
)

print(
    f"Recommendation: "
    f"{result['recommendation']}"
)