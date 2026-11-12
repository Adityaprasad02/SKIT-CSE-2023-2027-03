import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from resume.preprocessing.pipeline import preprocess_resume
from skills.hierarchy import SkillHierarchy
from skills.normalization import SkillNormalizer
from skills.resolver import SkillResolver
from skills.synonym_mapping import SynonymMapper
from skills.taxonomy import Taxonomy, load_taxonomy

from recommendation.matcher import match_resume_to_job
from recommendation.models import MatchResult


def _ml_system_root() -> Path:
    return Path(__file__).resolve().parents[1]


def build_skill_resolver() -> tuple[SkillResolver, Taxonomy]:
    """Create a resolver and taxonomy for a resume-to-job matching run."""
    root = _ml_system_root()
    taxonomy = load_taxonomy(root / "skills" / "taxonomy" / "taxonomy.json")
    resolver = SkillResolver(
        normalizer=SkillNormalizer(),
        mapper=SynonymMapper(
            root / "skills" / "synonym_mapping" / "mappings.json",
            taxonomy=taxonomy,
        ),
        hierarchy=SkillHierarchy(
            root / "skills" / "hierarchy" / "relationships.json"
        ),
    )
    return resolver, taxonomy


def score_resume_against_job(
    resume_path: str | Path,
    job_description: str,
) -> MatchResult:
    """Preprocess a resume and score it against a job description."""
    resume = preprocess_resume(str(resume_path))
    resolver, taxonomy = build_skill_resolver()
    return match_resume_to_job(resume, job_description, resolver, taxonomy)


def summarize_match(result: MatchResult) -> str:
    """Return a user-friendly textual summary of a match result."""
    matched_required = [skill.name for skill in result.matched_required]
    missing_required = [skill.name for skill in result.missing_required]
    matched_preferred = [skill.name for skill in result.matched_preferred]
    missing_preferred = [skill.name for skill in result.missing_preferred]

    lines = [
        f"Overall match score: {result.score:.2f}/100",
        (
            "Required skill coverage: "
            f"{len(result.matched_required)}/{len(result.matched_required) + len(result.missing_required)}"
        ),
        (
            "Preferred skill coverage: "
            f"{len(result.matched_preferred)}/{len(result.matched_preferred) + len(result.missing_preferred)}"
        ),
    ]

    if matched_required:
        lines.append(f"Matched required skills: {', '.join(matched_required)}")
    else:
        lines.append("Matched required skills: none")

    if missing_required:
        lines.append(f"Missing required skills: {', '.join(missing_required)}")
    else:
        lines.append("Missing required skills: none")

    if matched_preferred:
        lines.append(f"Matched preferred skills: {', '.join(matched_preferred)}")
    else:
        lines.append("Matched preferred skills: none")

    if missing_preferred:
        lines.append(f"Missing preferred skills: {', '.join(missing_preferred)}")
    else:
        lines.append("Missing preferred skills: none")

    return "\n".join(lines)


def _load_job_description(arguments: argparse.Namespace) -> str:
    if arguments.job_description:
        return arguments.job_description

    if arguments.job_file:
        return Path(arguments.job_file).read_text(encoding="utf-8")

    raise ValueError("Either --job-description or --job-file is required.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Score a resume against a job description using the ml-system taxonomy.",
    )
    parser.add_argument("resume_path", help="Path to the resume (.pdf or .docx)")
    parser.add_argument(
        "--job-description",
        help="Text of the job description directly in the command line.",
    )
    parser.add_argument(
        "--job-file",
        help="Path to a text file containing the job description.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit the match result as JSON instead of human-readable text.",
    )
    args = parser.parse_args(argv)

    try:
        job_description = _load_job_description(args)
        result = score_resume_against_job(args.resume_path, job_description)
    except Exception as exc:  # pragma: no cover - CLI safety path
        parser.exit(status=1, message=f"Error: {exc}\n")

    if args.json:
        payload = {
            "score": result.score,
            "matched_required": [skill.__dict__ for skill in result.matched_required],
            "missing_required": [skill.__dict__ for skill in result.missing_required],
            "matched_preferred": [skill.__dict__ for skill in result.matched_preferred],
            "missing_preferred": [skill.__dict__ for skill in result.missing_preferred],
        }
        print(json.dumps(payload, indent=2))
        return 0

    print(summarize_match(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
