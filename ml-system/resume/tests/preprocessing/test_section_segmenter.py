from unittest.mock import patch

from resume.preprocessing.header_detector import HeaderCandidate
from resume.preprocessing.line_segmenter import Line
from resume.preprocessing.section_segmenter import (
    PREAMBLE_SECTION,
    SegmentedResume,
    segment_sections,
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
# SegmentedResume Tests
# =========================================

def test_section_text_returns_joined_lines():

    segmented = SegmentedResume(
        sections={
            "skills": [
                "Python",
                "Machine Learning",
                "Scikit-learn",
            ]
        }
    )

    result = segmented.section_text("skills")

    assert result == "Python\nMachine Learning\nScikit-learn"


def test_section_text_returns_empty_string_for_missing_section():

    segmented = SegmentedResume()

    result = segmented.section_text("experience")

    assert result == ""


# =========================================
# segment_sections() Tests
# =========================================

def test_segment_sections_empty_input():

    result = segment_sections([], [])

    assert result.sections == {}
    assert result.headers == []


def test_segment_sections_puts_lines_before_header_in_preamble():

    lines = [
        create_line("Aditya Singh", 0),
        create_line("aditya@example.com", 1),
    ]

    result = segment_sections(lines, [])

    assert result.sections[PREAMBLE_SECTION] == [
        "Aditya Singh",
        "aditya@example.com",
    ]


@patch("resume.preprocessing.section_segmenter.classify_header")
def test_segment_sections_creates_classified_section(mock_classify):

    mock_classify.return_value = ("skills", 0.91)

    header_line = create_line(
        "SKILLS",
        0,
        font_size=16.0,
        is_bold=True,
    )

    content_line = create_line(
        "Python",
        1,
    )

    candidates = [
        HeaderCandidate(
            line=header_line,
            score=5,
        )
    ]

    result = segment_sections(
        [header_line, content_line],
        candidates,
    )

    assert "skills" in result.sections
    assert result.sections["skills"] == ["Python"]

    mock_classify.assert_called_once_with("SKILLS")


@patch("resume.preprocessing.section_segmenter.classify_header")
def test_segment_sections_does_not_include_header_in_section_body(
    mock_classify
):

    mock_classify.return_value = ("education", 0.95)

    header_line = create_line(
        "EDUCATION",
        0,
        font_size=16.0,
        is_bold=True,
    )

    content_line = create_line(
        "B.Tech Computer Science",
        1,
    )

    candidates = [
        HeaderCandidate(
            line=header_line,
            score=5,
        )
    ]

    result = segment_sections(
        [header_line, content_line],
        candidates,
    )

    assert result.sections["education"] == [
        "B.Tech Computer Science"
    ]

    assert "EDUCATION" not in result.sections["education"]


@patch("resume.preprocessing.section_segmenter.classify_header")
def test_segment_sections_handles_multiple_sections(mock_classify):

    mock_classify.side_effect = [
        ("skills", 0.95),
        ("education", 0.93),
    ]

    skills_header = create_line(
        "SKILLS",
        1,
        font_size=16.0,
        is_bold=True,
    )

    skills_content = create_line(
        "Python",
        2,
    )

    education_header = create_line(
        "EDUCATION",
        3,
        font_size=16.0,
        is_bold=True,
    )

    education_content = create_line(
        "B.Tech Computer Science",
        4,
    )

    lines = [
        create_line("Aditya Singh", 0),
        skills_header,
        skills_content,
        education_header,
        education_content,
    ]

    candidates = [
        HeaderCandidate(
            line=skills_header,
            score=5,
        ),
        HeaderCandidate(
            line=education_header,
            score=5,
        ),
    ]

    result = segment_sections(
        lines,
        candidates,
    )

    assert result.sections[PREAMBLE_SECTION] == [
        "Aditya Singh"
    ]

    assert result.sections["skills"] == [
        "Python"
    ]

    assert result.sections["education"] == [
        "B.Tech Computer Science"
    ]


def test_segment_sections_sorts_lines_by_line_index():

    line_2 = create_line(
        "Second line",
        1,
    )

    line_1 = create_line(
        "First line",
        0,
    )

    result = segment_sections(
        [line_2, line_1],
        [],
    )

    assert result.sections[PREAMBLE_SECTION] == [
        "First line",
        "Second line",
    ]


@patch("resume.preprocessing.section_segmenter.classify_header")
def test_segment_sections_stores_classified_header_metadata(
    mock_classify
):

    mock_classify.return_value = (
        "projects",
        0.88,
    )

    header_line = create_line(
        "PROJECTS",
        0,
        font_size=16.0,
        is_bold=True,
    )

    candidates = [
        HeaderCandidate(
            line=header_line,
            score=5,
        )
    ]

    result = segment_sections(
        [header_line],
        candidates,
    )

    assert len(result.headers) == 1

    header = result.headers[0]

    assert header.line_index == 0
    assert header.header_text == "PROJECTS"
    assert header.section == "projects"
    assert header.confidence == 0.88