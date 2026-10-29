from collections.abc import Sequence
from dataclasses import dataclass
import math

from recommendation import match_resume_to_job
from recommendation.models import MatchResult
from resume.preprocessing.pipeline import PreprocessedResume
from skills.resolver import SkillResolver
from skills.taxonomy import Taxonomy


@dataclass(frozen=True)
class EvaluationExample:
    resume: PreprocessedResume
    job_description: str
    is_relevant: bool


@dataclass(frozen=True)
class EvaluationMetrics:
    sample_count: int
    threshold: float
    accuracy: float
    precision: float
    recall: float
    f1: float
    true_positive: int
    false_positive: int
    true_negative: int
    false_negative: int


def evaluate_matcher(
    examples: Sequence[EvaluationExample],
    resolver: SkillResolver,
    taxonomy: Taxonomy | None = None,
    threshold: float = 50.0,
) -> EvaluationMetrics:
    """Evaluate binary job relevance labels against the matcher's score threshold."""
    if not math.isfinite(threshold) or not 0.0 <= threshold <= 100.0:
        raise ValueError("threshold must be between 0.0 and 100.0.")
    if not examples:
        raise ValueError("At least one evaluation example is required.")

    counts = {
        "true_positive": 0,
        "false_positive": 0,
        "true_negative": 0,
        "false_negative": 0,
    }

    for example in examples:
        result: MatchResult = match_resume_to_job(
            example.resume,
            example.job_description,
            resolver,
            taxonomy,
        )
        predicted_relevant = result.score >= threshold
        if predicted_relevant and example.is_relevant:
            counts["true_positive"] += 1
        elif predicted_relevant:
            counts["false_positive"] += 1
        elif example.is_relevant:
            counts["false_negative"] += 1
        else:
            counts["true_negative"] += 1

    sample_count = len(examples)
    true_positive = counts["true_positive"]
    false_positive = counts["false_positive"]
    true_negative = counts["true_negative"]
    false_negative = counts["false_negative"]
    precision = (
        true_positive / (true_positive + false_positive)
        if true_positive + false_positive
        else 0.0
    )
    recall = (
        true_positive / (true_positive + false_negative)
        if true_positive + false_negative
        else 0.0
    )

    return EvaluationMetrics(
        sample_count=sample_count,
        threshold=threshold,
        accuracy=(true_positive + true_negative) / sample_count,
        precision=precision,
        recall=recall,
        f1=(2 * precision * recall / (precision + recall))
        if precision + recall
        else 0.0,
        true_positive=true_positive,
        false_positive=false_positive,
        true_negative=true_negative,
        false_negative=false_negative,
    )
