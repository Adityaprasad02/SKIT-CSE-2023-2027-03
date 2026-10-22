from pathlib import Path

from resume.preprocessing.contact_extractor import ContactInfo
from resume.preprocessing.pipeline import PreprocessedResume
from skills.hierarchy import SkillHierarchy
from skills.normalization import SkillNormalizer
from skills.resolver import SkillResolver
from skills.synonym_mapping import SynonymMapper
from skills.taxonomy import load_taxonomy

from recommendation import match_resume_to_job, parse_job_description


ML_SYSTEM_DIR = Path(__file__).resolve().parents[3]


def create_resolver():
    taxonomy = load_taxonomy(ML_SYSTEM_DIR / "skills" / "taxonomy" / "taxonomy.json")
    resolver = SkillResolver(
        normalizer=SkillNormalizer(),
        mapper=SynonymMapper(
            ML_SYSTEM_DIR / "skills" / "synonym_mapping" / "mappings.json",
            taxonomy=taxonomy,
        ),
        hierarchy=SkillHierarchy(
            ML_SYSTEM_DIR / "skills" / "hierarchy" / "relationships.json"
        ),
    )
    return resolver, taxonomy


def create_resume(skills: str) -> PreprocessedResume:
    return PreprocessedResume(
        full_text=skills,
        sections={"skills": skills},
        contact_info=ContactInfo(emails=[], phones=[], linkedin=[], github=[]),
        detected_headers=["SKILLS"],
    )


def test_parser_resolves_aliases_and_separates_preferred_skills():
    resolver, taxonomy = create_resolver()

    requirements = parse_job_description(
        "Required skills: Python and ML\n"
        "Preferred qualifications:\n"
        "Experience with PyTorch and Docker",
        resolver,
        taxonomy,
    )

    assert [(skill.skill_id, skill.name) for skill in requirements.required_skills] == [
        ("python", "Python"),
        ("machine_learning", "Machine Learning"),
    ]
    assert [(skill.skill_id, skill.name) for skill in requirements.preferred_skills] == [
        ("pytorch", "PyTorch"),
        ("docker", "Docker"),
    ]


def test_match_weights_required_skills_and_returns_explanations():
    resolver, taxonomy = create_resolver()

    result = match_resume_to_job(
        create_resume("Python and PyTorch"),
        "Required: Python and Docker\nPreferred: PyTorch",
        resolver,
        taxonomy,
    )

    assert result.score == 60.0
    assert [skill.skill_id for skill in result.matched_required] == ["python"]
    assert [skill.skill_id for skill in result.missing_required] == ["docker"]
    assert [skill.skill_id for skill in result.matched_preferred] == ["pytorch"]
    assert result.missing_preferred == ()
    assert [skill.skill_id for skill in result.matched_skills] == ["python", "pytorch"]
    assert [skill.skill_id for skill in result.missing_skills] == ["docker"]


def test_parser_defaults_unmarked_skills_to_required_and_deduplicates():
    resolver, taxonomy = create_resolver()

    requirements = parse_job_description(
        "Python is required.\nPreferred: Python and Docker",
        resolver,
        taxonomy,
    )

    assert [skill.skill_id for skill in requirements.required_skills] == ["python"]
    assert [skill.skill_id for skill in requirements.preferred_skills] == ["docker"]


def test_match_without_job_skills_has_zero_score():
    resolver, taxonomy = create_resolver()

    result = match_resume_to_job(
        create_resume("Python"),
        "A great opportunity with a collaborative team.",
        resolver,
        taxonomy,
    )

    assert result.score == 0.0
    assert result.matched_skills == ()
    assert result.missing_skills == ()
