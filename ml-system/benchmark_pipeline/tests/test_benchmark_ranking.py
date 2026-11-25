from benchmark.schemas.models import RoleBenchmark, SkillRequirement
from benchmark_pipeline.pipeline import rank_resume_against_benchmarks
from resume.preprocessing.contact_extractor import ContactInfo
from resume.preprocessing.pipeline import PreprocessedResume
from skills.resolver import SkillResolver


class StubResolver:
    def resolve(self, skill_text):
        skill_id = skill_text.lower()
        if skill_id not in {"python", "docker"}:
            return None
        return {"canonical_id": skill_id}


def create_resume(text: str) -> PreprocessedResume:
    return PreprocessedResume(
        full_text=text,
        sections={"skills": text},
        contact_info=ContactInfo(emails=[], phones=[], linkedin=[], github=[]),
        detected_headers=[],
    )


def test_rank_resume_against_benchmarks_sorts_by_score():
    python_benchmark = RoleBenchmark(
        benchmark_id="python-v1",
        role="Python Engineer",
        required_skills=[SkillRequirement("python")],
    )
    docker_benchmark = RoleBenchmark(
        benchmark_id="docker-v1",
        role="DevOps Engineer",
        required_skills=[SkillRequirement("docker")],
    )

    rankings = rank_resume_against_benchmarks(
        create_resume("Python"),
        [docker_benchmark, python_benchmark],
        StubResolver(),
    )

    assert [report.role for report in rankings] == [
        "Python Engineer",
        "DevOps Engineer",
    ]
