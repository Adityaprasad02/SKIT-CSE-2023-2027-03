import json

from app.services.resume_processor import process_resume


file_path = "sample_resume.pdf"

try:
    resume = process_resume(file_path)

    print("\n========== RESUME VALIDATION ==========\n")
    print("Status: VALID")

    print("\n========== STRUCTURED RESUME ==========\n")

    print(
        json.dumps(
            resume,
            indent=4,
            ensure_ascii=False
        )
    )

except Exception as error:
    print("\n========== RESUME VALIDATION ==========\n")
    print("Status: INVALID")
    print(f"Error: {error}")