import re


SECTION_NAMES = {
    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "employment history",
        "work history",
        "internship",
        "internships",
        "online internship",
    ],

    "skills": [
        "skills",
        "technical skills",
        "technical skill",
        "core skills",
        "key skills",
        "key skill",
        "programming skills",
        "technical expertise",
        "areas of expertise",
    ],

    "education": [
        "education",
        "academic background",
        "educational background",
        "academic qualifications",
        "academic qualification",
        "educational qualifications",
        "educational qualification",
        "academic details",
    ],

    "projects": [
        "projects",
        "personal projects",
        "academic projects",
        "key projects",
        "major projects",
        "project work",
        "project experience",
    ],

    "research": [
        "research",
        "research experience",
        "research projects",
        "research work",
        "thesis",
        "master's thesis",
        "masters thesis",
        "msr thesis",
        "dissertation",
    ],

    "achievements": [
        "achievements",
        "accomplishments",
        "awards",
        "scholastic achievements",
        "academic achievements",
        "scholastic accomplishments",
    ],

    "certifications": [
        "certifications",
        "certificates",
        "professional certifications",
        "professional certificates",
    ],

    "responsibilities": [
        "positions of responsibility",
        "position of responsibility",
        "leadership",
        "leadership experience",
    ],

    "courses": [
        "relevant courses",
        "relevant coursework",
        "coursework",
        "courses",
    ],

    "extracurricular": [
        "extra-curricular activities",
        "extracurricular activities",
        "extra curricular activities",
        "extra-curricular",
        "extracurricular",
    ],
}


def normalize_heading(line: str) -> str:
    """
    Normalize a possible section heading.
    """

    line = line.strip().lower()

    # Remove common punctuation at the end.
    line = re.sub(r"[:*\-–—]+$", "", line)

    # Normalize repeated whitespace.
    line = re.sub(r"\s+", " ", line)

    return line.strip()


def detect_section(line: str):
    """
    Detect whether a line represents a known
    resume section heading.
    """

    normalized_line = normalize_heading(line)

    for section, headings in SECTION_NAMES.items():
        if normalized_line in headings:
            return section

    return None


def extract_sections(text: str) -> dict:
    """
    Extract normalized sections from resume text.
    """

    sections = {
        "experience": [],
        "skills": [],
        "education": [],
        "projects": [],
        "research": [],
        "achievements": [],
        "certifications": [],
        "responsibilities": [],
        "courses": [],
        "extracurricular": [],
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

    for section in sections:
        sections[section] = "\n".join(sections[section])

    return sections