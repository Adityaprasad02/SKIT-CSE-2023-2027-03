from typing import Any


SECTION_NAMES = [
    "experience",
    "skills",
    "education",
    "projects",
    "achievements",
    "certifications",
    "responsibilities",
    "courses",
    "extracurricular",
    "other",
]


CONTACT_FIELDS = [
    "name",
    "email",
    "phone",
    "location",
    "linkedin",
    "github",
    "leetcode",
]


def validate_resume_data(
    resume_data: dict[str, Any]
) -> tuple[bool, list[str]]:
    """
    Validate the normalized resume structure.
    """

    errors = []

    # Top-level fields
    required_fields = [
        "contact",
        "sections",
        "skills",
    ]

    for field in required_fields:
        if field not in resume_data:
            errors.append(
                f"Missing field: {field}"
            )

    if errors:
        return False, errors

    # Contact validation
    for field in CONTACT_FIELDS:
        if field not in resume_data["contact"]:
            errors.append(
                f"Missing contact field: {field}"
            )

    # Section validation
    for section in SECTION_NAMES:
        if section not in resume_data["sections"]:
            errors.append(
                f"Missing section: {section}"
            )

    # Skills validation
    if not isinstance(
        resume_data["skills"],
        dict
    ):
        errors.append(
            "Skills must be a dictionary."
        )

    return len(errors) == 0, errors