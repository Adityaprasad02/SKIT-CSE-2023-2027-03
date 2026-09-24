from resume.preprocessing.pipeline import (
    PreprocessedResume,
)
from resume.skill_extraction.extractor import (
    extract_skills_from_text,
)
from resume.skill_extraction.models import (
    SkillExtractionResult,
    SkillMatch,
)


SKILL_SOURCE_SECTIONS = {
    "skills",
    "experience",
    "projects",
    "education",
    "certifications",
}


def extract_skills(
    resume: PreprocessedResume,
) -> SkillExtractionResult:

    all_matches: list[SkillMatch] = []

    by_section: dict[str, list[str]] = {}

    for section, text in resume.sections.items():

        if section not in SKILL_SOURCE_SECTIONS:
            continue

        if not text.strip():
            continue

        matches = extract_skills_from_text(
            text=text,
            source_section=section,
        )

        all_matches.extend(matches)

        section_skills = []

        for match in matches:

            if match.skill not in section_skills:
                section_skills.append(match.skill)

        if section_skills:
            by_section[section] = section_skills

    # Preserve first-seen order while removing duplicates.
    skills: list[str] = []

    for match in all_matches:

        if match.skill not in skills:
            skills.append(match.skill)

    return SkillExtractionResult(
        skills=skills,
        matches=all_matches,
        by_section=by_section,
    )