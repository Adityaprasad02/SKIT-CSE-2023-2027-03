import re


SECTION_NAMES = {
    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "employment history",
    ],
    "skills": [
        "skills",
        "technical skills",
        "core skills",
        "key skills",
    ],
    "education": [
        "education",
        "academic background",
        "educational background",
    ],
    "projects": [
        "projects",
        "personal projects",
        "academic projects",
    ],
    "achievements": [
        "achievements",
        "accomplishments",
        "awards",
    ],
    "certifications": [
        "certifications",
        "certificates",
    ],
}


def normalize_heading(line: str) -> str:
    """
    Normalize a possible section heading.
    """

    line = line.strip().lower()

    # Remove common heading punctuation
    line = re.sub(r"[:\-]+$", "", line)

    return line.strip()


def detect_section(line: str):
    """
    Check whether a line is a known resume section heading.
    """

    normalized_line = normalize_heading(line)

    for section, headings in SECTION_NAMES.items():
        if normalized_line in headings:
            return section

    return None


def extract_sections(text: str) -> dict:
    """
    Divide resume text into logical sections.
    """

    sections = {
        "experience": [],
        "skills": [],
        "education": [],
        "projects": [],
        "achievements": [],
        "certifications": [],
        "other": [],
    }

    current_section = "other"

    lines = text.split("\n")

    for line in lines:
        line = line.strip()

        if not line:
            continue

        detected_section = detect_section(line)

        if detected_section:
            current_section = detected_section
            continue

        sections[current_section].append(line)

    # Convert lists into text
    for section in sections:
        sections[section] = "\n".join(sections[section])

    return sections