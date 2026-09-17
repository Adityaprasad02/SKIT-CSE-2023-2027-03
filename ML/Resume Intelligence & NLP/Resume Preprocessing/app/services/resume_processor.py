from app.services.parser import extract_text
from app.services.preprocessor import preprocess_resume
from app.services.section_extractor import extract_sections
from app.services.contact_extractor import extract_contact_information
from app.services.skill_extractor import extract_skills
from app.services.resume_schema import validate_resume_data


def process_resume(file_path: str) -> dict:
    """
    Complete resume processing pipeline.
    """

    # Extract text
    raw_text = extract_text(file_path)

    # Preprocess text
    cleaned_text = preprocess_resume(raw_text)

    # Extract sections
    sections = extract_sections(cleaned_text)

    # Extract contact information
    contact = extract_contact_information(cleaned_text)

    # Extract skills
    skills = extract_skills(sections["skills"])

    # Build structured resume
    resume_data = {
        "contact": contact,
        "sections": sections,
        "skills": skills
    }

    # Validate structure
    is_valid, errors = validate_resume_data(resume_data)

    if not is_valid:
        raise ValueError(
            "Resume validation failed: " + "; ".join(errors)
        )

    return resume_data