import re
from collections import Counter


def normalize_text(text: str) -> str:
    """
    Normalize text for ATS-style keyword analysis.
    """

    text = text.lower()

    # Replace special characters with spaces
    text = re.sub(r"[^a-z0-9+#.\- ]", " ", text)

    # Normalize multiple spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def tokenize(text: str) -> list[str]:
    """
    Convert text into normalized tokens.
    """

    normalized = normalize_text(text)

    return normalized.split()


def extract_keywords(text: str) -> list[str]:
    """
    Extract meaningful keywords from text.

    This is intentionally simple and transparent.
    Later we can replace/extend this with NLP-based
    skill extraction.
    """

    tokens = tokenize(text)

    # Common words that are usually not useful
    # for ATS keyword comparison.
    stop_words = {
        "the",
        "and",
        "or",
        "of",
        "to",
        "in",
        "for",
        "with",
        "a",
        "an",
        "on",
        "at",
        "by",
        "from",
        "as",
        "is",
        "are",
        "be",
        "this",
        "that",
        "will",
        "can",
        "have",
        "has",
        "using",
        "used",
        "work",
        "working",
        "experience",
        "years",
        "role",
        "job",
        "responsible",
        "responsibilities",
        "skills",
        "knowledge",
    }

    keywords = []

    for token in tokens:

        if token in stop_words:
            continue

        if len(token) < 2:
            continue

        keywords.append(token)

    return keywords


def calculate_keyword_match(
    resume_text: str,
    job_description: str,
) -> dict:
    """
    Compare keywords appearing in the resume
    and job description.
    """

    resume_keywords = set(
        extract_keywords(resume_text)
    )

    jd_keywords = set(
        extract_keywords(job_description)
    )

    matched_keywords = sorted(
        resume_keywords.intersection(jd_keywords)
    )

    missing_keywords = sorted(
        jd_keywords - resume_keywords
    )

    match_percentage = 0.0

    if jd_keywords:
        match_percentage = (
            len(matched_keywords)
            / len(jd_keywords)
        ) * 100

    return {
        "matched_keywords": matched_keywords,
        "missing_keywords": missing_keywords,
        "match_percentage": round(
            match_percentage,
            2,
        ),
    }


def analyze_resume_sections(
    sections: dict,
) -> dict:
    """
    Check which important resume sections
    are present and which are empty.
    """

    important_sections = [
        "experience",
        "skills",
        "education",
        "projects",
    ]

    present_sections = []
    missing_sections = []

    for section in important_sections:

        content = sections.get(
            section,
            "",
        )

        if content and content.strip():
            present_sections.append(section)
        else:
            missing_sections.append(section)

    return {
        "present_sections": present_sections,
        "missing_sections": missing_sections,
    }


def calculate_section_score(
    sections: dict,
) -> float:
    """
    Calculate a simple section completeness score.

    This is NOT a universal ATS score.
    It only measures whether important sections
    were detected.
    """

    important_sections = [
        "experience",
        "skills",
        "education",
        "projects",
    ]

    completed = 0

    for section in important_sections:

        content = sections.get(
            section,
            "",
        )

        if content and content.strip():
            completed += 1

    return round(
        (completed / len(important_sections)) * 100,
        2,
    )


def analyze_ats(
    sections: dict,
    job_description: str,
) -> dict:
    """
    Run the complete initial ATS analysis.

    Returns:
        - section analysis
        - keyword matching
        - missing keywords
        - section completeness
    """

    # Combine all extracted resume sections
    resume_parts = []

    for content in sections.values():

        if content and isinstance(content, str):
            resume_parts.append(content)

    resume_text = "\n".join(resume_parts)

    keyword_analysis = calculate_keyword_match(
        resume_text,
        job_description,
    )

    section_analysis = analyze_resume_sections(
        sections
    )

    section_score = calculate_section_score(
        sections
    )

    return {
        "keyword_analysis": keyword_analysis,
        "section_analysis": section_analysis,
        "section_completeness": section_score,
    }