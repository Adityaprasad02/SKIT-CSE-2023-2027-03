from app.services.job_parser import parse_job_description


job_description = """
We are looking for an Android Developer.

Requirements:
Kotlin, Java, Android, MVVM, REST APIs and Retrofit.
Experience with mobile application development is preferred.
"""


result = parse_job_description(job_description)


print("\n========== JOB DESCRIPTION PARSER ==========\n")

print("Cleaned Job Description:")
print(result["cleaned_text"])

print("\nNumber of Characters:")
print(result["length"])

print("\nLines:")
for line in result["lines"]:
    print("-", line)