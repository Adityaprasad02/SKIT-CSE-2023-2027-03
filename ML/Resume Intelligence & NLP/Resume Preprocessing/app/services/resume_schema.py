from typing import Any


REQUIRED_CONTACT_FIELDS = [
    "name",
    "email",
    "phone",
    "location",
    "linkedin",
    "github",
    "leetcode",
]

REQUIRED_SECTIONS = [
    "experience",
    "skills",
    "education",
    "projects",
    "achievements",
    "certifications",
    "other",
]

REQUIRED_SKILL_CATEGORIES = [
    "programming_languages",
    "mobile_development",
    "computer_science",
    "tools_and_practices",
    "other_technologies",
]


def validate_resume_data(resume_data: dict[str, Any]) -> tuple[bool, list[str]]:
    """
    Validate the structure of the processed resume.
    """

    errors = []

    # Check top-level fields
    for field in ["contact", "sections", "skills"]:
        if field not in resume_data:
            errors.append(f"Missing field: {field}")

    # Stop if required top-level fields are missing
    if errors:
        return False, errors

    # Check contact fields
    for field in REQUIRED_CONTACT_FIELDS:
        if field not in resume_data["contact"]:
            errors.append(f"Missing contact field: {field}")

    # Check sections
    for section in REQUIRED_SECTIONS:
        if section not in resume_data["sections"]:
            errors.append(f"Missing section: {section}")

    # Check skill categories
    for category in REQUIRED_SKILL_CATEGORIES:
        if category not in resume_data["skills"]:
            errors.append(f"Missing skill category: {category}")

    return len(errors) == 0, errors