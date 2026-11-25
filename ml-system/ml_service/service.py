from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from benchmark_pipeline.pipeline import rank_resume_against_benchmarks
from benchmark.schemas.models import RoleBenchmark
from gap_analysis.analyzer import analyze_resume_against_benchmark
from recommendation.cli import build_skill_resolver
from recommendation.matcher import match_resume_to_job
from recommendation.semantic_matcher import SemanticMatcher
from resume.preprocessing.contact_extractor import ContactInfo
from resume.preprocessing.pipeline import PreprocessedResume


class MLService:
    """In-process facade used by HTTP and CLI entry points."""

    def __init__(self) -> None:
        self.resolver, self.taxonomy = build_skill_resolver()

    @staticmethod
    def _resume_from_text(resume_text: str) -> PreprocessedResume:
        if not isinstance(resume_text, str):
            raise TypeError("resume_text must be a string")
        if not resume_text.strip():
            raise ValueError("resume_text cannot be empty")
        return PreprocessedResume(
            full_text=resume_text,
            sections={"skills": resume_text},
            contact_info=ContactInfo(emails=[], phones=[], linkedin=[], github=[]),
            detected_headers=[],
        )

    def score(
        self,
        resume_text: str,
        job_description: str,
        *,
        include_semantic: bool = False,
    ) -> dict:
        resume = self._resume_from_text(resume_text)
        if not isinstance(job_description, str) or not job_description.strip():
            raise ValueError("job_description cannot be empty")

        match = match_resume_to_job(
            resume,
            job_description,
            self.resolver,
            self.taxonomy,
        )
        payload = {
            "score": match.score,
            "matched_required": [skill.skill_id for skill in match.matched_required],
            "missing_required": [skill.skill_id for skill in match.missing_required],
            "matched_preferred": [skill.skill_id for skill in match.matched_preferred],
            "missing_preferred": [skill.skill_id for skill in match.missing_preferred],
        }
        if include_semantic:
            payload["semantic_score"] = SemanticMatcher().score(
                resume_text,
                job_description,
            )
        return payload

    def gap(self, resume_text: str, benchmark_data: dict) -> dict:
        resume = self._resume_from_text(resume_text)
        if not isinstance(benchmark_data, dict):
            raise TypeError("benchmark must be an object")
        benchmark = RoleBenchmark.from_dict(benchmark_data)
        benchmark.validate_taxonomy(self.taxonomy)
        report = analyze_resume_against_benchmark(
            resume,
            benchmark,
            self.resolver,
            self.taxonomy,
        )
        return {
            "benchmark_id": report.benchmark_id,
            "role": report.role,
            "score": report.score,
            "matched_skills": [item.__dict__ for item in report.matched_skills],
            "missing_skills": [item.__dict__ for item in report.missing_skills],
        }

    def rank(self, resume_text: str, benchmarks: list[dict]) -> dict:
        resume = self._resume_from_text(resume_text)
        if not isinstance(benchmarks, list) or not benchmarks:
            raise ValueError("benchmarks must be a non-empty list")

        parsed = []
        for benchmark_data in benchmarks:
            if not isinstance(benchmark_data, dict):
                raise TypeError("each benchmark must be an object")
            benchmark = RoleBenchmark.from_dict(benchmark_data)
            benchmark.validate_taxonomy(self.taxonomy)
            parsed.append(benchmark)

        reports = rank_resume_against_benchmarks(
            resume,
            parsed,
            self.resolver,
            self.taxonomy,
        )
        return {
            "rankings": [
                {
                    "benchmark_id": report.benchmark_id,
                    "role": report.role,
                    "score": report.score,
                    "missing_skills": [item.skill_id for item in report.missing_skills],
                }
                for report in reports
            ]
        }
