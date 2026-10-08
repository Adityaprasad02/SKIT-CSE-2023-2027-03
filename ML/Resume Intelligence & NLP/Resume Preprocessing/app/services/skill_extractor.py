import re

from app.services.skill_dictionary import SKILL_ALIASES


def normalize_skill_text(text: str) -> str:
    """
    Normalize text before skill matching.
    """

    text = text.lower()

    text = text.replace("–", "-")
    text = text.replace("—", "-")

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def contains_skill(text: str, alias: str) -> bool:
    """
    Check whether an alias occurs as a complete term.
    """

    pattern = (
        r"(?<![a-z0-9])"
        + re.escape(alias)
        + r"(?![a-z0-9])"
    )

    return re.search(pattern, text) is not None


def extract_skills(text: str) -> set[str]:
    """
    Extract canonical skills from text.

    When multiple aliases overlap, prefer the more
    specific/longer skill phrase.
    """

    if not text:
        return set()

    normalized_text = normalize_skill_text(text)

    detected_skills = set()
    matched_aliases = {}

    for canonical_skill, aliases in SKILL_ALIASES.items():

        for alias in aliases:

            normalized_alias = normalize_skill_text(alias)

            if contains_skill(
                normalized_text,
                normalized_alias,
            ):
                detected_skills.add(canonical_skill)

                matched_aliases[canonical_skill] = (
                    normalized_alias
                )

                break

    # Remove a shorter skill when it is completely
    # contained inside a more specific detected skill.
    skills_to_remove = set()

    for skill_a, alias_a in matched_aliases.items():

        for skill_b, alias_b in matched_aliases.items():

            if skill_a == skill_b:
                continue

            if (
                alias_a != alias_b
                and alias_a in alias_b
                and len(alias_b) > len(alias_a)
            ):
                skills_to_remove.add(skill_a)

    detected_skills.difference_update(
        skills_to_remove
    )

    return detected_skills