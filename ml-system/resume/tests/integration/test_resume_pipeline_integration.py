from pathlib import Path
from unittest.mock import patch

from resume.preprocessing.pipeline import preprocess_resume


FIXTURES_DIR = Path(__file__).parent / "fixtures"


def fake_classify_header(header_text: str) -> tuple[str, float]:
    classifications = {
        "PROFESSIONAL SUMMARY": ("summary", 0.95),
        "SKILLS": ("skills", 0.99),
        "EDUCATION": ("education", 0.99),
        "PROJECTS": ("projects", 0.99),
        "EXPERIENCE": ("experience", 0.99),
    }

    return classifications.get(header_text, ("other", 0.30))


@patch(
    "resume.preprocessing.section_segmenter.classify_header",
    side_effect=fake_classify_header,
)
def test_resume_pipeline_with_real_docx(mock_classifier):
    resume_path = FIXTURES_DIR / "sample_resume.docx"

    result = preprocess_resume(str(resume_path))

    # Full text
# Full text
    assert "aditya singh jadoun" in result.full_text.lower()
    assert "python" in result.full_text.lower()
    assert "machine learning" in result.full_text.lower()

    # Contact information
    assert result.contact_info.emails == [
        "adityasinghjadoun17@gmail.com"
    ]

    assert "+91 7062425403" in result.contact_info.phones

    assert result.contact_info.linkedin == [
        "linkedin.com/in/adityasingh"
    ]

    assert result.contact_info.github == [
        "github.com/adityasingh"
    ]

    # Detected headers
    assert "SKILLS" in result.detected_headers
    assert "EDUCATION" in result.detected_headers
    assert "PROJECTS" in result.detected_headers

    # Section content
    assert "Python" in result.sections["skills"]
    assert "Machine Learning" in result.sections["skills"]

    assert "Bachelor of Technology" in result.sections["education"]

    assert "AI Resume Analyzer" in result.sections["projects"]

    # Verify classifier was actually called
    assert mock_classifier.call_count > 0