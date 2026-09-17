import re


STOP_WORDS = {
    "a", "an", "the", "and", "or", "but", "if",
    "for", "of", "to", "in", "on", "at", "by",
    "with", "from", "as", "is", "are", "was",
    "were", "be", "been", "being", "this", "that",
    "these", "those", "we", "you", "your", "our",
    "they", "their", "it", "its", "an", "will",
    "can", "have", "has", "had", "looking"
}


def tokenize(text: str) -> set[str]:
    """Extract meaningful keywords from text."""

    words = re.findall(
        r"\b[a-zA-Z][a-zA-Z0-9+#.-]*\b",
        text.lower()
    )

    return {
        word
        for word in words
        if word not in STOP_WORDS
    }


def calculate_keyword_match(
    resume_text: str,
    job_description: str
) -> dict:
    """
    Calculate meaningful keyword overlap between
    resume and job description.
    """

    resume_keywords = tokenize(resume_text)
    job_keywords = tokenize(job_description)

    matched_keywords = resume_keywords.intersection(
        job_keywords
    )

    missing_keywords = job_keywords.difference(
        resume_keywords
    )

    total_job_keywords = len(job_keywords)

    if total_job_keywords > 0:
        match_percentage = (
            len(matched_keywords)
            / total_job_keywords
        ) * 100
    else:
        match_percentage = 0.0

    return {
        "matched_keywords": sorted(matched_keywords),
        "missing_keywords": sorted(missing_keywords),
        "keyword_match_percentage": round(
            match_percentage,
            2
        )
    }