from app.services.job_skill_extractor import extract_job_skills


job_description = """
We are looking for an Android Developer.

Requirements:
Kotlin, Java, Android, MVVM, REST APIs and Retrofit.
Experience with mobile application development is preferred.
"""


skills = extract_job_skills(job_description)


print("\n========== JOB SKILL EXTRACTION ==========\n")

print("Job Description:")
print(job_description.strip())

print("\nRequired Skills:")

for skill in skills:
    print("-", skill)