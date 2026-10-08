"""
Calculate job relevance scores by comparing
candidate skills with job requirements.
"""

from app.services.skill_extractor import extract_skills
from app.services.skill_dictionary import (
    RELATED_SKILLS,
    SKILL_ALIASES,
)


def match_skills(
    candidate_skills: set[str],
    job_skills: set[str],
) -> tuple[list[str], list[str], list[str], float]:
    """
    Match candidate skills against job skills.

    Exact match:
        1.0 credit

    Related skill:
        0.5 credit

    No match:
        0.0 credit
    """

    exact_matches = []
    related_matches = []
    missing_skills = []

    total_credit = 0.0

    for job_skill in sorted(job_skills):

        if job_skill in candidate_skills:
            exact_matches.append(job_skill)
            total_credit += 1.0
            continue

        related_found = False

        related_options = RELATED_SKILLS.get(
            job_skill,
            set()
        )

        for related_skill in related_options:
            if related_skill in candidate_skills:
                related_matches.append(
                    f"{job_skill} <- {related_skill}"
                )
                total_credit += 0.5
                related_found = True
                break

        if not related_found:
            missing_skills.append(job_skill)

    return (
        exact_matches,
        related_matches,
        missing_skills,
        total_credit,
    )
def calculate_skill_match(
    candidate_skills: list[str],
    required_skills: list[str],
    preferred_skills: list[str],
) -> dict:
    """
    Calculate required and preferred skill matches.

    Exact match:
        100% credit

    Related skill:
        50% credit

    Scoring:
        Required skills  -> 35 points
        Preferred skills -> 15 points
    """

    candidate = {
        skill.strip().lower()
        for skill in candidate_skills
        if skill.strip()
    }

    required = {
        skill.strip().lower()
        for skill in required_skills
        if skill.strip()
    }

    preferred = {
        skill.strip().lower()
        for skill in preferred_skills
        if skill.strip()
    }

    (
        matched_required,
        related_required,
        missing_required,
        required_credit,
    ) = match_skills(candidate, required)

    (
        matched_preferred,
        related_preferred,
        missing_preferred,
        preferred_credit,
    ) = match_skills(candidate, preferred)

    if required:
        required_percentage = (
            required_credit / len(required)
        ) * 100
    else:
        required_percentage = 100.0

    if preferred:
        preferred_percentage = (
            preferred_credit / len(preferred)
        ) * 100
    else:
        preferred_percentage = 100.0

    required_score = (
        required_percentage / 100
    ) * 35

    preferred_score = (
        preferred_percentage / 100
    ) * 15

    return {
        "required": {
            "matched": matched_required,
            "related": related_required,
            "missing": missing_required,
            "percentage": round(required_percentage, 2),
            "score": round(required_score, 2),
            "max_score": 35,
        },
        "preferred": {
            "matched": matched_preferred,
            "related": related_preferred,
            "missing": missing_preferred,
            "percentage": round(preferred_percentage, 2),
            "score": round(preferred_score, 2),
            "max_score": 15,
        },
        "skill_score": round(
            required_score + preferred_score,
            2,
        ),
        "max_skill_score": 50,
    }
def calculate_context_relevance(
    candidate_text: list[str],
    required_skills: list[str],
    preferred_skills: list[str],
) -> dict:
    """
    Measure how strongly the candidate's experience
    supports the job requirements.

    Maximum:
        15 points
    """

    text = "\n".join(
        item for item in candidate_text
        if isinstance(item, str) and item.strip()
    )

    detected_skills = extract_skills(text)

    required = {
        skill.strip().lower()
        for skill in required_skills
        if skill.strip()
    }

    preferred = {
        skill.strip().lower()
        for skill in preferred_skills
        if skill.strip()
    }

    (
        matched_required,
        related_required,
        missing_required,
        required_credit,
    ) = match_skills(detected_skills, required)

    (
        matched_preferred,
        related_preferred,
        missing_preferred,
        preferred_credit,
    ) = match_skills(detected_skills, preferred)

    if required:
        required_percentage = (
            required_credit / len(required)
        ) * 100
    else:
        required_percentage = 100.0

    if preferred:
        preferred_percentage = (
            preferred_credit / len(preferred)
        ) * 100
    else:
        preferred_percentage = 100.0

    relevance_percentage = (
        required_percentage * 0.7
        + preferred_percentage * 0.3
    )

    relevance_score = (
        relevance_percentage / 100
    ) * 15

    return {
        "matched_required": matched_required,
        "related_required": related_required,
        "missing_required": missing_required,
        "matched_preferred": matched_preferred,
        "related_preferred": related_preferred,
        "missing_preferred": missing_preferred,
        "percentage": round(relevance_percentage, 2),
        "score": round(relevance_score, 2),
        "max_score": 15,
    }
def calculate_project_relevance(
    project_text: list[str],
    required_skills: list[str],
    preferred_skills: list[str],
) -> dict:
    """
    Measure how strongly the candidate's projects
    support the job requirements.

    Maximum:
        10 points
    """

    text = "\n".join(
        item for item in project_text
        if isinstance(item, str) and item.strip()
    )

    detected_skills = extract_skills(text)

    required = {
        skill.strip().lower()
        for skill in required_skills
        if skill.strip()
    }

    preferred = {
        skill.strip().lower()
        for skill in preferred_skills
        if skill.strip()
    }

    (
        matched_required,
        related_required,
        missing_required,
        required_credit,
    ) = match_skills(detected_skills, required)

    (
        matched_preferred,
        related_preferred,
        missing_preferred,
        preferred_credit,
    ) = match_skills(detected_skills, preferred)

    if required:
        required_percentage = (
            required_credit / len(required)
        ) * 100
    else:
        required_percentage = 100.0

    if preferred:
        preferred_percentage = (
            preferred_credit / len(preferred)
        ) * 100
    else:
        preferred_percentage = 100.0

    relevance_percentage = (
        required_percentage * 0.7
        + preferred_percentage * 0.3
    )

    relevance_score = (
        relevance_percentage / 100
    ) * 10

    return {
        "matched_required": matched_required,
        "related_required": related_required,
        "missing_required": missing_required,
        "matched_preferred": matched_preferred,
        "related_preferred": related_preferred,
        "missing_preferred": missing_preferred,
        "percentage": round(relevance_percentage, 2),
        "score": round(relevance_score, 2),
        "max_score": 10,
    }
def calculate_education_match(
    candidate_education: list[str],
    education_requirements: list[str],
) -> dict:
    """
    Compare candidate education with the education
    requirements extracted from the job description.

    Maximum:
        5 points
    """

    candidate_text = " ".join(
        item for item in candidate_education
        if isinstance(item, str) and item.strip()
    ).lower()

    requirements = {
        item.strip().lower()
        for item in education_requirements
        if item.strip()
    }

    if not requirements:
        return {
            "matched": [],
            "missing": [],
            "percentage": 100.0,
            "score": 5.0,
            "max_score": 5,
        }

    matched = []
    missing = []

    for requirement in sorted(requirements):
        if requirement in candidate_text:
            matched.append(requirement)
        else:
            missing.append(requirement)

    percentage = (
        len(matched) / len(requirements)
    ) * 100

    score = (
        percentage / 100
    ) * 5

    return {
        "matched": matched,
        "missing": missing,
        "percentage": round(percentage, 2),
        "score": round(score, 2),
        "max_score": 5,
    }
def calculate_resume_completeness(
    candidate_profile: dict,
) -> dict:
    """
    Measure whether the candidate profile contains
    the core resume sections.

    Maximum:
        10 points
    """

    core_sections = {
        "skills": candidate_profile.get("skills", []),
        "experience": candidate_profile.get("experience", []),
        "projects": candidate_profile.get("projects", []),
        "education": candidate_profile.get("education", []),
    }

    section_scores = {}
    missing_sections = []

    points_per_section = 2.5

    for section, content in core_sections.items():
        has_content = bool(content)

        section_scores[section] = (
            points_per_section
            if has_content
            else 0.0
        )

        if not has_content:
            missing_sections.append(section)

    score = sum(section_scores.values())

    percentage = (
        score / 10
    ) * 100

    return {
        "sections": section_scores,
        "missing_sections": missing_sections,
        "percentage": round(percentage, 2),
        "score": round(score, 2),
        "max_score": 10,
    }
def calculate_keyword_relevance(
    candidate_text: str,
    job_description: str,
) -> dict:
    """
    Measure overlap of meaningful non-skill keywords.

    Skill matching is handled separately by the skill
    scoring components, so known skill phrases are removed
    before calculating keyword relevance.

    Maximum:
        10 points
    """

    import re

    stop_words = {
        "a",
        "an",
        "and",
        "are",
        "as",
        "at",
        "be",
        "by",
        "for",
        "from",
        "has",
        "have",
        "in",
        "is",
        "of",
        "on",
        "or",
        "that",
        "the",
        "this",
        "to",
        "with",
        "will",
        "you",
        "your",
        "we",
        "our",
        "should",
        "must",
        "can",
        "looking",
        "developer",
        "developers",
        "experience",
        "experienced",
        "role",
        "position",
        "candidate",
        "candidates",
        "team",
        "work",
        "working",
        "responsibilities",
        "requirements",
        "required",
        "preferred",
        "skills",
        "knowledge",
    }

    def remove_skill_phrases(text: str) -> str:
        """
        Remove known skill phrases so that skill terms
        are not counted again as generic keywords.
        """

        normalized = text.lower()

        aliases = []

        for skill_aliases in SKILL_ALIASES.values():
            aliases.extend(skill_aliases)

        aliases = sorted(
            set(aliases),
            key=len,
            reverse=True,
        )

        for alias in aliases:
            pattern = (
                r"(?<![a-z0-9])"
                + re.escape(alias.lower())
                + r"(?![a-z0-9])"
            )

            normalized = re.sub(
                pattern,
                " ",
                normalized,
            )

        return normalized

    def tokenize(text: str) -> set[str]:
        words = re.findall(
            r"\b[a-zA-Z][a-zA-Z0-9.-]*\b",
            text.lower(),
        )

        return {
            word
            for word in words
            if len(word) >= 3
            and word not in stop_words
        }

    candidate_clean = remove_skill_phrases(
        candidate_text
    )

    job_clean = remove_skill_phrases(
        job_description
    )

    candidate_keywords = tokenize(
        candidate_clean
    )

    job_keywords = tokenize(
        job_clean
    )

    matched_keywords = sorted(
        candidate_keywords.intersection(
            job_keywords
        )
    )

    missing_keywords = sorted(
        job_keywords - candidate_keywords
    )

    if job_keywords:
        percentage = (
            len(matched_keywords)
            / len(job_keywords)
        ) * 100
    else:
        percentage = 50.0

    score = (
        percentage / 100
    ) * 10

    return {
        "matched": matched_keywords,
        "missing": missing_keywords,
        "percentage": round(percentage, 2),
        "score": round(score, 2),
        "max_score": 10,
    }