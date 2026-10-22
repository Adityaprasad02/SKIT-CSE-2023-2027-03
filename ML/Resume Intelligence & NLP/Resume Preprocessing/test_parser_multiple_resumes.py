from pathlib import Path

from app.services.parser import extract_text
from app.services.preprocessor import preprocess_resume
from app.services.section_extractor import extract_sections


def test_resume(file_path):

    print("\n" + "=" * 60)
    print(f"Testing Resume: {file_path}")
    print("=" * 60)

    raw_text = extract_text(file_path)

    cleaned_text = preprocess_resume(raw_text)

    sections = extract_sections(cleaned_text)

    for section, content in sections.items():

        print(f"\n--- {section.upper()} ---")

        if content.strip():
            print(content[:500])
        else:
            print("EMPTY")


# Take resume path from the user
resume_path = input(
    "\nEnter the complete resume file path (PDF/DOCX): "
).strip().strip('"')


# Validate file path
if not Path(resume_path).is_file():

    print("\nERROR: File does not exist.")

else:

    supported_extensions = [".pdf", ".docx"]

    if Path(resume_path).suffix.lower() not in supported_extensions:

        print("\nERROR: Only PDF and DOCX files are supported.")

    else:

        test_resume(resume_path)