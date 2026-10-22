"""
Build a structured candidate profile from extracted
resume sections.
"""


def clean_items(text: str) -> list[str]:
    """
    Convert section text into clean non-empty lines.
    """

    if not isinstance(text, str):
        return []

    items = []

    for line in text.splitlines():
        line = line.strip()

        if line:
            items.append(line)

    return items


def build_candidate_profile(sections: dict) -> dict:
    """
    Convert extracted resume sections into a
    structured candidate profile.
    """

    skills_text = sections.get("skills", "")
    experience_text = sections.get("experience", "")
    projects_text = sections.get("projects", "")
    education_text = sections.get("education", "")
    certifications_text = sections.get("certifications", "")
    achievements_text = sections.get("achievements", "")

    return {
        "skills": clean_items(skills_text),
        "experience": clean_items(experience_text),
        "projects": clean_items(projects_text),
        "education": clean_items(education_text),
        "certifications": clean_items(
            certifications_text
        ),
        "achievements": clean_items(
            achievements_text
        ),
    }