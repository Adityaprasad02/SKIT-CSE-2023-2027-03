from ml_service.service import MLService


def test_ml_service_scores_resume_text():
    service = MLService()

    result = service.score("Python and Git", "Required: Python and Docker")

    assert result["score"] == 50.0
    assert "python" in result["matched_required"]
    assert "docker" in result["missing_required"]


def test_ml_service_gap_and_rank_accept_benchmark_objects():
    service = MLService()
    benchmark = {
        "benchmark_id": "ml-v1",
        "role": "ML Engineer",
        "required_skills": [
            {"skill_id": "python", "importance": 1.0, "required": True},
            {"skill_id": "pytorch", "importance": 0.8, "required": False},
        ],
    }

    gap = service.gap("Python developer", benchmark)
    ranking = service.rank("Python developer", [benchmark])

    assert gap["score"] == 55.56
    assert gap["missing_skills"][0]["skill_id"] == "pytorch"
    assert ranking["rankings"][0]["role"] == "ML Engineer"
