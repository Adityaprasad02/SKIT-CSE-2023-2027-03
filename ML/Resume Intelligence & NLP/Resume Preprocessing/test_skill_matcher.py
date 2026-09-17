from app.services.skill_matcher import calculate_skill_match


resume_skills = [
    "Java",
    "Kotlin",
    "Android",
    "MVVM",
    "Git"
]


required_skills = [
    "Android",
    "Java",
    "Kotlin",
    "MVVM",
    "REST API",
    "Retrofit"
]


result = calculate_skill_match(
    resume_skills,
    required_skills
)


print("\n========== SKILL MATCHING ==========\n")

print("Resume Skills:")
print(", ".join(resume_skills))

print("\nRequired Skills:")
print(", ".join(required_skills))

print("\nMatched Skills:")
print(", ".join(result["matched_skills"]))

print("\nMissing Skills:")
print(", ".join(result["missing_skills"]))

print(
    f"\nSkill Match: "
    f"{result['skill_match_percentage']:.2f}%"
)