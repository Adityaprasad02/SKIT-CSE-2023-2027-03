import pytest

from evaluation import EvaluationExample, evaluate_matcher
from resume.preprocessing.contact_extractor import ContactInfo
from resume.preprocessing.pipeline import PreprocessedResume


class StubResolver:
    def resolve(self, skill_text):
        skill_id = skill_text.casefold()
        if skill_id not in {"python", "docker"}:
            return None
        return {"canonical_id": skill_id}


def create_resume(skills: str) -> PreprocessedResume:
    return PreprocessedResume(
        full_text=skills,
        sections={"skills": skills},
        contact_info=ContactInfo(emails=[], phones=[], linkedin=[], github=[]),
        detected_headers=["SKILLS"],
    )


def test_evaluate_matcher_reports_binary_classification_metrics():
    examples = [
        EvaluationExample(create_resume("Python"), "Required: Python", True),
        EvaluationExample(create_resume(""), "Required: Python", False),
        EvaluationExample(create_resume("Python"), "Required: Python", False),
        EvaluationExample(create_resume(""), "Required: Python", True),
    ]

    metrics = evaluate_matcher(examples, StubResolver(), threshold=75.0)

    assert metrics.sample_count == 4
    assert metrics.threshold == 75.0
    assert metrics.accuracy == 0.5
    assert metrics.precision == 0.5
    assert metrics.recall == 0.5
    assert metrics.f1 == 0.5
    assert (
        metrics.true_positive,
        metrics.false_positive,
        metrics.true_negative,
        metrics.false_negative,
    ) == (1, 1, 1, 1)


@pytest.mark.parametrize("threshold", [-0.1, 100.1, float("nan"), float("inf")])
def test_evaluate_matcher_rejects_invalid_threshold(threshold):
    with pytest.raises(ValueError, match="threshold"):
        evaluate_matcher(
            [EvaluationExample(create_resume(""), "", False)],
            StubResolver(),
            threshold=threshold,
        )


def test_evaluate_matcher_rejects_empty_dataset():
    with pytest.raises(ValueError, match="At least one"):
        evaluate_matcher([], StubResolver())
