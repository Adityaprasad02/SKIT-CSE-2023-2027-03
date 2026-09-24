from resume.skill_extraction.dictionary_extractor import (
    extract_dictionary_skills,
)
from resume.skill_extraction.models import SkillMatch
from resume.skill_extraction.phrase_extractor import (
    extract_phrase_candidates,
)


def extract_skills_from_text(
    text: str,
    source_section: str,
) -> list[SkillMatch]:

    matches = extract_dictionary_skills(
        text=text,
        source_section=source_section,
    )

    dictionary_skills = {
        match.skill.lower()
        for match in matches
    }

    phrase_candidates = extract_phrase_candidates(text)

    for phrase in phrase_candidates:

        normalized = phrase.lower()

        if normalized in dictionary_skills:
            continue

        matches.append(
            SkillMatch(
                skill=phrase,
                matched_text=phrase,
                source_section=source_section,
                method="phrase",
                confidence=0.50,
            )
        )

    return matches