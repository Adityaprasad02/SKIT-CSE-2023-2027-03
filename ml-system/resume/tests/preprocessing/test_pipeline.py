from unittest.mock import patch

from resume.parsing.models import RawLine
from resume.preprocessing.contact_extractor import ContactInfo
from resume.preprocessing.header_detector import HeaderCandidate
from resume.preprocessing.line_segmenter import Line
from resume.preprocessing.pipeline import (
    PreprocessedResume,
    preprocess_resume,
)
from resume.preprocessing.section_segmenter import (
    ClassifiedHeader,
    SegmentedResume,
)


def create_raw_line(
    text,
    line_index,
    page_number=1,
    font_size=12.0,
    is_bold=False,
):
    return RawLine(
        text=text,
        page_number=page_number,
        font_size=font_size,
        is_bold=is_bold,
        is_italic=False,
        line_index=line_index,
    )


def create_line(
    text,
    line_index,
    page_number=1,
    font_size=12.0,
    is_bold=False,
):
    return Line(
        text=text,
        page_number=page_number,
        font_size=font_size,
        is_bold=is_bold,
        is_italic=False,
        line_index=line_index,
        word_count=len(text.split()),
        caps_ratio=1.0 if text.isupper() else 0.0,
        ends_with_punctuation=False,
        is_bullet=False,
    )


# =========================================
# PreprocessedResume Tests
# =========================================

def test_preprocessed_resume_creation():

    contact_info = ContactInfo(
        emails=["aditya@example.com"],
        phones=[],
        linkedin=[],
        github=[],
    )

    result = PreprocessedResume(
        full_text="Aditya Singh",
        sections={
            "skills": "Python\nMachine Learning"
        },
        contact_info=contact_info,
        detected_headers=["SKILLS"],
    )

    assert result.full_text == "Aditya Singh"

    assert result.sections == {
        "skills": "Python\nMachine Learning"
    }

    assert result.contact_info.emails == [
        "aditya@example.com"
    ]

    assert result.detected_headers == [
        "SKILLS"
    ]


# =========================================
# Pipeline Tests
# =========================================

@patch("resume.preprocessing.pipeline.extract_contact_info")
@patch("resume.preprocessing.pipeline.segment_sections")
@patch("resume.preprocessing.pipeline.detect_headers")
@patch("resume.preprocessing.pipeline.segment_lines")
@patch("resume.preprocessing.pipeline.parse_resume_structured")
def test_preprocess_resume_runs_pipeline(
    mock_parse,
    mock_segment_lines,
    mock_detect_headers,
    mock_segment_sections,
    mock_extract_contact,
):

    raw_lines = [
        create_raw_line("Aditya Singh", 0),
        create_raw_line("SKILLS", 1),
        create_raw_line("Python", 2),
    ]

    lines = [
        create_line("Aditya Singh", 0),
        create_line("SKILLS", 1, font_size=16.0, is_bold=True),
        create_line("Python", 2),
    ]

    header_candidate = HeaderCandidate(
        line=lines[1],
        score=5,
    )

    segmented_resume = SegmentedResume(
        sections={
            "preamble": ["Aditya Singh"],
            "skills": ["Python"],
        },
        headers=[
            ClassifiedHeader(
                line_index=1,
                header_text="SKILLS",
                section="skills",
                confidence=0.95,
            )
        ],
    )

    contact_info = ContactInfo(
        emails=[],
        phones=[],
        linkedin=[],
        github=[],
    )

    mock_parse.return_value = raw_lines

    mock_segment_lines.return_value = lines

    mock_detect_headers.return_value = [
        header_candidate
    ]

    mock_segment_sections.return_value = segmented_resume

    mock_extract_contact.return_value = contact_info

    result = preprocess_resume("resume.pdf")

    assert isinstance(result, PreprocessedResume)

    assert result.full_text == (
        "Aditya Singh\n"
        "SKILLS\n"
        "Python"
    )

    assert result.sections == {
        "preamble": "Aditya Singh",
        "skills": "Python",
    }

    assert result.contact_info == contact_info

    assert result.detected_headers == [
        "SKILLS"
    ]


@patch("resume.preprocessing.pipeline.extract_contact_info")
@patch("resume.preprocessing.pipeline.segment_sections")
@patch("resume.preprocessing.pipeline.detect_headers")
@patch("resume.preprocessing.pipeline.segment_lines")
@patch("resume.preprocessing.pipeline.parse_resume_structured")
def test_preprocess_resume_calls_all_pipeline_stages(
    mock_parse,
    mock_segment_lines,
    mock_detect_headers,
    mock_segment_sections,
    mock_extract_contact,
):

    raw_lines = [
        create_raw_line("Test", 0),
    ]

    lines = [
        create_line("Test", 0),
    ]

    segmented_resume = SegmentedResume(
        sections={
            "preamble": ["Test"],
        },
        headers=[],
    )

    contact_info = ContactInfo(
        emails=[],
        phones=[],
        linkedin=[],
        github=[],
    )

    mock_parse.return_value = raw_lines

    mock_segment_lines.return_value = lines

    mock_detect_headers.return_value = []

    mock_segment_sections.return_value = segmented_resume

    mock_extract_contact.return_value = contact_info

    preprocess_resume("resume.pdf")

    mock_parse.assert_called_once_with(
        "resume.pdf"
    )

    mock_segment_lines.assert_called_once_with(
        raw_lines
    )

    mock_detect_headers.assert_called_once_with(
        lines
    )

    mock_segment_sections.assert_called_once_with(
        lines,
        [],
    )

    mock_extract_contact.assert_called_once_with(
        "Test"
    )


@patch("resume.preprocessing.pipeline.extract_contact_info")
@patch("resume.preprocessing.pipeline.segment_sections")
@patch("resume.preprocessing.pipeline.detect_headers")
@patch("resume.preprocessing.pipeline.segment_lines")
@patch("resume.preprocessing.pipeline.parse_resume_structured")
def test_preprocess_resume_sorts_lines_by_line_index(
    mock_parse,
    mock_segment_lines,
    mock_detect_headers,
    mock_segment_sections,
    mock_extract_contact,
):

    raw_lines = []

    lines = [
        create_line("Third", 2),
        create_line("First", 0),
        create_line("Second", 1),
    ]

    segmented_resume = SegmentedResume(
        sections={
            "preamble": [
                "First",
                "Second",
                "Third",
            ]
        },
        headers=[],
    )

    contact_info = ContactInfo(
        emails=[],
        phones=[],
        linkedin=[],
        github=[],
    )

    mock_parse.return_value = raw_lines

    mock_segment_lines.return_value = lines

    mock_detect_headers.return_value = []

    mock_segment_sections.return_value = segmented_resume

    mock_extract_contact.return_value = contact_info

    result = preprocess_resume("resume.pdf")

    assert result.full_text == (
        "First\n"
        "Second\n"
        "Third"
    )


@patch("resume.preprocessing.pipeline.extract_contact_info")
@patch("resume.preprocessing.pipeline.segment_sections")
@patch("resume.preprocessing.pipeline.detect_headers")
@patch("resume.preprocessing.pipeline.segment_lines")
@patch("resume.preprocessing.pipeline.parse_resume_structured")
def test_preprocess_resume_converts_sections_to_strings(
    mock_parse,
    mock_segment_lines,
    mock_detect_headers,
    mock_segment_sections,
    mock_extract_contact,
):

    lines = [
        create_line("Python", 0),
        create_line("Machine Learning", 1),
    ]

    segmented_resume = SegmentedResume(
        sections={
            "skills": [
                "Python",
                "Machine Learning",
            ]
        },
        headers=[],
    )

    contact_info = ContactInfo(
        emails=[],
        phones=[],
        linkedin=[],
        github=[],
    )

    mock_parse.return_value = []

    mock_segment_lines.return_value = lines

    mock_detect_headers.return_value = []

    mock_segment_sections.return_value = segmented_resume

    mock_extract_contact.return_value = contact_info

    result = preprocess_resume("resume.pdf")

    assert result.sections["skills"] == (
        "Python\n"
        "Machine Learning"
    )

    assert isinstance(
        result.sections["skills"],
        str,
    )


@patch("resume.preprocessing.pipeline.extract_contact_info")
@patch("resume.preprocessing.pipeline.segment_sections")
@patch("resume.preprocessing.pipeline.detect_headers")
@patch("resume.preprocessing.pipeline.segment_lines")
@patch("resume.preprocessing.pipeline.parse_resume_structured")
def test_preprocess_resume_extracts_detected_header_text(
    mock_parse,
    mock_segment_lines,
    mock_detect_headers,
    mock_segment_sections,
    mock_extract_contact,
):

    lines = [
        create_line("SKILLS", 0),
        create_line("EDUCATION", 1),
    ]

    segmented_resume = SegmentedResume(
        sections={
            "skills": [],
            "education": [],
        },
        headers=[
            ClassifiedHeader(
                line_index=0,
                header_text="SKILLS",
                section="skills",
                confidence=0.95,
            ),
            ClassifiedHeader(
                line_index=1,
                header_text="EDUCATION",
                section="education",
                confidence=0.92,
            ),
        ],
    )

    contact_info = ContactInfo(
        emails=[],
        phones=[],
        linkedin=[],
        github=[],
    )

    mock_parse.return_value = []

    mock_segment_lines.return_value = lines

    mock_detect_headers.return_value = []

    mock_segment_sections.return_value = segmented_resume

    mock_extract_contact.return_value = contact_info

    result = preprocess_resume("resume.pdf")

    assert result.detected_headers == [
        "SKILLS",
        "EDUCATION",
    ]