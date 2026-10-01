import pytest

from resume.parsing.models import RawLine
from resume.preprocessing.line_segmenter import (
    _strip_bullet,
    _caps_ratio,
    segment_lines,
)


# =========================================
# _strip_bullet() Tests
# =========================================

def test_strip_standard_bullet():

    result = _strip_bullet("• Python Developer")

    assert result == "Python Developer"


def test_strip_dash_bullet():

    result = _strip_bullet("- Machine Learning")

    assert result == "Machine Learning"


def test_strip_arrow_bullet():

    result = _strip_bullet("▸ Security Testing")

    assert result == "Security Testing"


def test_strip_bullet_with_surrounding_spaces():

    result = _strip_bullet("   •   Python   ")

    assert result == "Python"


def test_strip_bullet_preserves_normal_text():

    result = _strip_bullet("Python Developer")

    assert result == "Python Developer"


# =========================================
# _caps_ratio() Tests
# =========================================

def test_caps_ratio_all_uppercase():

    result = _caps_ratio("SKILLS")

    assert result == 1.0


def test_caps_ratio_all_lowercase():

    result = _caps_ratio("skills")

    assert result == 0.0


def test_caps_ratio_mixed_case():

    result = _caps_ratio("Skills")

    assert result == pytest.approx(1 / 6)


def test_caps_ratio_ignores_numbers_and_symbols():

    result = _caps_ratio("ABC 123!!")

    assert result == 1.0


def test_caps_ratio_no_letters():

    result = _caps_ratio("123 !!")

    assert result == 0.0


# =========================================
# segment_lines() Tests
# =========================================

def test_segment_lines_creates_line():

    raw_line = RawLine(
        text="Python Developer",
        page_number=1,
        font_size=14.0,
        is_bold=True,
        is_italic=False,
        line_index=0,
    )

    result = segment_lines([raw_line])

    assert len(result) == 1

    line = result[0]

    assert line.text == "Python Developer"
    assert line.page_number == 1
    assert line.font_size == 14.0
    assert line.is_bold is True
    assert line.is_italic is False
    assert line.line_index == 0


def test_segment_lines_skips_empty_text():

    raw_line = RawLine(
        text="    ",
        page_number=1,
        font_size=12.0,
        is_bold=False,
        is_italic=False,
        line_index=0,
    )

    result = segment_lines([raw_line])

    assert result == []


def test_segment_lines_detects_bullet():

    raw_line = RawLine(
        text="• Python",
        page_number=1,
        font_size=12.0,
        is_bold=False,
        is_italic=False,
        line_index=0,
    )

    result = segment_lines([raw_line])

    assert len(result) == 1
    assert result[0].is_bullet is True
    assert result[0].text == "Python"


def test_segment_lines_detects_non_bullet():

    raw_line = RawLine(
        text="Python Developer",
        page_number=1,
        font_size=12.0,
        is_bold=False,
        is_italic=False,
        line_index=0,
    )

    result = segment_lines([raw_line])

    assert result[0].is_bullet is False


def test_segment_lines_counts_words():

    raw_line = RawLine(
        text="Python Machine Learning",
        page_number=1,
        font_size=12.0,
        is_bold=False,
        is_italic=False,
        line_index=0,
    )

    result = segment_lines([raw_line])

    assert result[0].word_count == 3


def test_segment_lines_detects_punctuation():

    raw_line = RawLine(
        text="Python Developer.",
        page_number=1,
        font_size=12.0,
        is_bold=False,
        is_italic=False,
        line_index=0,
    )

    result = segment_lines([raw_line])

    assert result[0].ends_with_punctuation is True


def test_segment_lines_detects_no_punctuation():

    raw_line = RawLine(
        text="Python Developer",
        page_number=1,
        font_size=12.0,
        is_bold=False,
        is_italic=False,
        line_index=0,
    )

    result = segment_lines([raw_line])

    assert result[0].ends_with_punctuation is False


def test_segment_lines_calculates_caps_ratio():

    raw_line = RawLine(
        text="SKILLS",
        page_number=1,
        font_size=14.0,
        is_bold=True,
        is_italic=False,
        line_index=0,
    )

    result = segment_lines([raw_line])

    assert result[0].caps_ratio == 1.0


def test_segment_lines_preserves_multiple_lines():

    raw_lines = [
        RawLine(
            text="SKILLS",
            page_number=1,
            font_size=14.0,
            is_bold=True,
            is_italic=False,
            line_index=0,
        ),
        RawLine(
            text="Python",
            page_number=1,
            font_size=12.0,
            is_bold=False,
            is_italic=False,
            line_index=1,
        ),
    ]

    result = segment_lines(raw_lines)

    assert len(result) == 2
    assert result[0].text == "SKILLS"
    assert result[1].text == "Python"
    assert result[0].line_index == 0
    assert result[1].line_index == 1