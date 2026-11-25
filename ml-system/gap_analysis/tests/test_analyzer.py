from benchmark.schemas.models import RoleBenchmark, SkillRequirement
from gap_analysis import analyze_resume_against_benchmark
from resume.preprocessing.contact_extractor import ContactInfo
from resume.preprocessing.pipeline import PreprocessedResume
from skills.hierarchy import SkillHierarchy
from skills.normalization import SkillNormalizer
from skills.resolver import SkillResolver
from skills.synonym_mapping import SynonymMapper
from skills.taxonomy import load_taxonomy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def create_resolver():
    taxonomy = load_taxonomy(ROOT / "skills" / "taxonomy" / "taxonomy.json")
    resolver = SkillResolver(
        normalizer=SkillNormalizer(),
        mapper=SynonymMapper(
            ROOT / "skills" / "synonym_mapping" / "mappings.json",
            taxonomy=taxonomy,
        ),
        hierarchy=SkillHierarchy(
            ROOT / "skills" / "hierarchy" / "relationships.json"
        ),
    )
    return resolver, taxonomy


def create_resume(text: str) -> PreprocessedResume:
    return PreprocessedResume(
        full_text=text,
        sections={"skills": text},
        contact_info=ContactInfo(emails=[], phones=[], linkedin=[], github=[]),
        detected_headers=["SKILLS"],
    )


def test_gap_analysis_reports_weighted_coverage_and_priority():
    resolver, taxonomy = create_resolver()
    benchmark = RoleBenchmark(
        benchmark_id="backend-v1",
        role="Backend Engineer",
        required_skills=[
            SkillRequirement("python", importance=1.0, required=True),
            SkillRequirement("docker", importance=0.5, required=False),
        ],
    )

    report = analyze_resume_against_benchmark(
        create_resume("Python"),
        benchmark,
        resolver,
        taxonomy,
    )

    assert report.score == 66.67
    assert [item.skill_id for item in report.matched_skills] == ["python"]
    assert [item.skill_id for item in report.missing_skills] == ["docker"]
    assert report.missing_skills[0].priority == "medium"
