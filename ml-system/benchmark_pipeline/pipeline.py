from benchmark.schemas.models import RoleBenchmark
from gap_analysis.analyzer import analyze_resume_against_benchmark
from gap_analysis.models import SkillGapReport
from resume.preprocessing.pipeline import PreprocessedResume
from skills.resolver import SkillResolver
from skills.taxonomy import Taxonomy


def rank_resume_against_benchmarks(
    resume: PreprocessedResume,
    benchmarks: tuple[RoleBenchmark, ...] | list[RoleBenchmark],
    resolver: SkillResolver,
    taxonomy: Taxonomy | None = None,
) -> tuple[SkillGapReport, ...]:
    """Rank role benchmark gaps by descending coverage score."""
    if not benchmarks:
        raise ValueError("At least one role benchmark is required.")

    reports = [
        analyze_resume_against_benchmark(resume, benchmark, resolver, taxonomy)
        for benchmark in benchmarks
    ]
    return tuple(sorted(reports, key=lambda report: (-report.score, report.role.casefold())))
