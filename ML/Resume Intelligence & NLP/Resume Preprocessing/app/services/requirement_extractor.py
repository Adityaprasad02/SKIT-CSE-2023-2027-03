import re
from app.services.skill_extractor import extract_skills

REQUIRED_HEADINGS = {
    "required",
    "requirements",
    "required skills",
    "must have",
    "mandatory",
    "essential qualifications",
    "minimum qualifications",
    "qualifications required",
}


PREFERRED_HEADINGS = {
    "preferred",
    "preferred skills",
    "nice to have",
    "good to have",
    "bonus",
    "desired",
    "preferred qualifications",
}


GENERAL_HEADINGS = {
    "responsibilities",
    "about the role",
    "job description",
    "overview",
    "summary",
    "education",
    "experience",
    "qualifications",
}


def normalize_text(text: str) -> str:
    """
    Normalize job-description text.
    """

    text = text.lower()

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def normalize_heading(text: str) -> str:
    """
    Normalize a possible JD section heading.
    """

    text = normalize_text(text)

    text = re.sub(r"^[\-\*\•\d\.\)\s]+", "", text)

    text = re.sub(r"[:\-]+$", "", text)

    return text.strip()


def detect_heading(text: str) -> str | None:
    """
    Detect whether a line represents a known
    requirement section heading.
    """

    heading = normalize_heading(text)

    if heading in REQUIRED_HEADINGS:
        return "required"

    if heading in PREFERRED_HEADINGS:
        return "preferred"

    if heading in GENERAL_HEADINGS:
        return "general"

    return None


def classify_requirement(text: str) -> str:
    """
    Classify a standalone requirement line.
    """

    normalized = normalize_text(text)

    required_patterns = [
        r"\brequired\b",
        r"\bmust have\b",
        r"\bmandatory\b",
        r"\bessential\b",
        r"\bminimum\b",
        r"\bstrong knowledge\b",
        r"\bproficiency in\b",
        r"\bproficient in\b",
    ]

    preferred_patterns = [
        r"\bpreferred\b",
        r"\bnice to have\b",
        r"\bgood to have\b",
        r"\bbonus\b",
        r"\bdesired\b",
        r"\bfamiliarity with\b",
    ]

    for pattern in required_patterns:
        if re.search(pattern, normalized):
            return "required"

    for pattern in preferred_patterns:
        if re.search(pattern, normalized):
            return "preferred"

    return "general"


def extract_requirement_lines(text: str) -> dict:
    """
    Extract requirement text while respecting
    section headings in the job description.
    """

    required = []
    preferred = []
    general = []

    current_section = "general"

    for raw_line in text.splitlines():

        line = raw_line.strip()

        if not line:
            continue

        heading_type = detect_heading(line)

        if heading_type:
            current_section = heading_type
            continue

        if current_section == "required":
            required.append(line)

        elif current_section == "preferred":
            preferred.append(line)

        else:
            classification = classify_requirement(line)

            if classification == "required":
                required.append(line)

            elif classification == "preferred":
                preferred.append(line)

            else:
                general.append(line)

    return {
        "required": required,
        "preferred": preferred,
        "general": general,
    }


def extract_experience_requirement(
    text: str,
) -> str | None:
    """
    Extract an experience requirement such as
    '2+ years of experience'.
    """

    pattern = (
        r"\b\d+\+?\s*(?:to|-)?\s*\d*\s*"
        r"(?:years?|yrs?)\s*(?:of)?\s*experience\b"
    )

    match = re.search(
        pattern,
        normalize_text(text),
    )

    if match:
        return match.group(0)

    return None


def extract_education_requirement(
    text: str,
) -> list[str]:
    """
    Extract common education qualifications.
    """

    normalized = normalize_text(text)

    education_terms = [
        "bachelor's degree",
        "bachelors degree",
        "bachelor degree",
        "master's degree",
        "masters degree",
        "master degree",
        "b.tech",
        "btech",
        "m.tech",
        "mtech",
        "b.e.",
        "be degree",
        "m.e.",
        "me degree",
        "computer science degree",
        "engineering degree",
    ]

    found = []

    for term in education_terms:
        if term in normalized:
            found.append(term)

    return sorted(set(found))


def analyze_job_description(text: str) -> dict:
    """
    Build a structured representation of a
    job description including extracted skills.
    """

    requirements = extract_requirement_lines(text)

    experience = extract_experience_requirement(text)

    education = extract_education_requirement(text)

    required_text = "\n".join(
        requirements["required"]
    )

    preferred_text = "\n".join(
        requirements["preferred"]
    )

    required_skills = sorted(
        extract_skills(required_text)
    )

    preferred_skills = sorted(
        extract_skills(preferred_text)
    )

    return {
        "required": requirements["required"],
        "preferred": requirements["preferred"],
        "general": requirements["general"],
        "required_skills": required_skills,
        "preferred_skills": preferred_skills,
        "experience_requirement": experience,
        "education_requirements": education,
    }
    