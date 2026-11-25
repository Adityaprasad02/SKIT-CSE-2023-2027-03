import argparse
import json
from pathlib import Path

from benchmark.loader import load_benchmark
from benchmark_pipeline.pipeline import rank_resume_against_benchmarks
from recommendation.cli import build_skill_resolver, score_resume_against_job
from recommendation.cli import summarize_match


ROOT = Path(__file__).resolve().parent


def _load_job_description(arguments: argparse.Namespace) -> str:
    if arguments.job_description:
        return arguments.job_description
    if arguments.job_file:
        return Path(arguments.job_file).read_text(encoding="utf-8")
    return ""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run the complete ml-system resume analysis pipeline",
    )
    parser.add_argument(
        "resume",
        nargs="?",
        default=str(ROOT / "resume" / "tests" / "integration" / "fixtures" / "sample_resume.docx"),
        help="Resume PDF or DOCX path",
    )
    parser.add_argument("--job-description")
    parser.add_argument("--job-file")
    parser.add_argument("--benchmark")
    parser.add_argument("--benchmark-dir")
    parser.add_argument("--semantic", action="store_true")
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args(argv)

    try:
        resolver, taxonomy = build_skill_resolver()
        job_description = _load_job_description(arguments)
        payload: dict = {}

        if job_description:
            match = score_resume_against_job(arguments.resume, job_description)
            payload["match"] = {
                "score": match.score,
                "matched_required": [skill.skill_id for skill in match.matched_required],
                "missing_required": [skill.skill_id for skill in match.missing_required],
                "matched_preferred": [skill.skill_id for skill in match.matched_preferred],
                "missing_preferred": [skill.skill_id for skill in match.missing_preferred],
            }
            if arguments.semantic:
                from resume.preprocessing.pipeline import preprocess_resume
                from recommendation.semantic_matcher import SemanticMatcher

                resume = preprocess_resume(arguments.resume)
                payload["match"]["semantic_score"] = SemanticMatcher().score(
                    resume.full_text,
                    job_description,
                )

        benchmarks = []
        if arguments.benchmark:
            benchmarks.append(load_benchmark(arguments.benchmark, taxonomy))
        if arguments.benchmark_dir:
            from benchmark.loader import load_benchmarks

            benchmarks.extend(load_benchmarks(arguments.benchmark_dir, taxonomy))

        if benchmarks:
            from resume.preprocessing.pipeline import preprocess_resume

            resume = preprocess_resume(arguments.resume)
            rankings = rank_resume_against_benchmarks(
                resume,
                benchmarks,
                resolver,
                taxonomy,
            )
            payload["benchmarks"] = [
                {
                    "benchmark_id": report.benchmark_id,
                    "role": report.role,
                    "score": report.score,
                    "matched_skills": [item.skill_id for item in report.matched_skills],
                    "missing_skills": [item.skill_id for item in report.missing_skills],
                }
                for report in rankings
            ]

        if arguments.json:
            print(json.dumps(payload, indent=2))
        else:
            if job_description:
                print(summarize_match(match))
            for ranking in payload.get("benchmarks", []):
                print(
                    f"{ranking['role']}: {ranking['score']:.2f}/100 "
                    f"(missing: {', '.join(ranking['missing_skills']) or 'none'})"
                )
    except Exception as exc:
        parser.exit(status=1, message=f"Error: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())