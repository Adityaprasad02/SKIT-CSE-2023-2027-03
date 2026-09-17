from app.services.resume_processor import process_resume
from app.services.semantic_analyzer import SemanticAnalyzer


file_path = "sample_resume.pdf"

job_description = """
We are looking for an Android Developer with experience
in Kotlin, Java, Android development, MVVM, REST APIs,
Retrofit, Coroutines and mobile application development.
"""


print("\n========== RESUME INTELLIGENCE PIPELINE ==========\n")

# Step 1: Process resume
resume = process_resume(file_path)

print("Resume processing: SUCCESS")


# Step 2: Combine important resume content
resume_text = "\n".join([
    resume["sections"]["experience"],
    resume["sections"]["skills"],
    resume["sections"]["projects"],
    resume["sections"]["education"],
    resume["sections"]["achievements"]
])


# Step 3: Semantic analysis
analyzer = SemanticAnalyzer()

score = analyzer.calculate_similarity(
    resume_text,
    job_description
)


print("\n========== SEMANTIC MATCH ==========\n")
print(f"Similarity Score: {score}")
print(f"Match Percentage: {score * 100:.2f}%")


# Step 4: Display extracted skills
print("\n========== EXTRACTED SKILLS ==========\n")

for category, skills in resume["skills"].items():
    print(f"{category}:")

    if skills:
        print(", ".join(skills))
    else:
        print("None")

    print()