from app.services.keyword_matcher import calculate_keyword_match


resume_text = """
Android Developer with experience in Kotlin and Java.
Developed Android applications using MVVM architecture.
Worked with REST APIs and Git.
"""


job_description = """
We are looking for an Android Developer with experience
in Kotlin, Java, Android, MVVM, REST APIs and Retrofit.
Experience with mobile application development is preferred.
"""


result = calculate_keyword_match(
    resume_text,
    job_description
)


print("\n========== KEYWORD MATCHING ==========\n")

print("Matched Keywords:")
print(", ".join(result["matched_keywords"]))

print("\nMissing Keywords:")
print(", ".join(result["missing_keywords"]))

print(
    f"\nKeyword Match: "
    f"{result['keyword_match_percentage']:.2f}%"
)