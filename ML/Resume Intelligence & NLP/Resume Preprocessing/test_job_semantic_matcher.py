from app.services.resume_processor import process_resume
from app.services.job_semantic_matcher import calculate_job_semantic_match


file_path = "sample_resume.pdf"

job_description = """
We are looking for an Android Developer with experience
in Kotlin, Java, Android, MVVM, REST APIs, Retrofit,
Coroutines and mobile application development.
"""


# Process the resume
resume = process_resume(file_path)


# Combine relevant resume sections
resume_text = "\n".join([
    resume["sections"]["experience"],
    resume["sections"]["skills"],
    resume["sections"]["projects"],
    resume["sections"]["education"],
    resume["sections"]["achievements"]
])


# Calculate semantic similarity
score = calculate_job_semantic_match(
    resume_text,
    job_description
)


print("\n========== JOB SEMANTIC MATCHING ==========\n")

print(f"Semantic Similarity Score: {score}")
print(f"Semantic Match: {score * 100:.2f}%")
