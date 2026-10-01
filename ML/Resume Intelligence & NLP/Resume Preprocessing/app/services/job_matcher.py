import re


def normalize_text(text: str) -> str:
    """
    Normalize text for job matching.
    """

    text = text.lower()

    text = re.sub(
        r"[^a-z0-9+#.\- ]",
        " ",
        text,
    )

    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text.strip()


def extract_terms(text: str) -> set[str]:
    """
    Extract normalized terms from text.
    """

    normalized_text = normalize_text(text)

    if not normalized_text:
        return set()

    return set(normalized_text.split())


def build_resume_text(sections: dict) -> str:
    """
    Combine extracted resume sections into
    a single text representation.
    """

    resume_parts = []

    for content in sections.values():

        if isinstance(content, str) and content.strip():
            resume_parts.append(content)

    return "\n".join(resume_parts)


def calculate_skill_overlap(
    resume_text: str,
    job_description: str,
) -> dict:
    """
    Compare terms found in the resume and
    job description.
    """

    resume_terms = extract_terms(resume_text)
    job_terms = extract_terms(job_description)

    matched_terms = sorted(
        resume_terms.intersection(job_terms)
    )

    missing_terms = sorted(
        job_terms - resume_terms
    )

    match_percentage = 0.0

    if job_terms:
        match_percentage = (
            len(matched_terms)
            / len(job_terms)
        ) * 100

    return {
        "matched_terms": matched_terms,
        "missing_terms": missing_terms,
        "match_percentage": round(
            match_percentage,
            2,
        ),
    }


def match_job(
    sections: dict,
    job_description: str,
) -> dict:
    """
    Perform initial resume-to-job matching.
    """

    resume_text = build_resume_text(
        sections
    )

    overlap = calculate_skill_overlap(
        resume_text,
        job_description,
    )

    return {
        "match_percentage": overlap[
            "match_percentage"
        ],
        "matched_terms": overlap[
            "matched_terms"
        ],
        "missing_terms": overlap[
            "missing_terms"
        ],
    }