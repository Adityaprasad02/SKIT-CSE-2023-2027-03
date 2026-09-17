from resume.preprocessing.line_segmenter import Line
from resume.preprocessing.header_detector import (
    _estimate_body_font_size,
    detect_headers,
)


def create_line(
    text="Python Developer",
    font_size=12.0,
    is_bold=False,
    word_count=4,
    caps_ratio=0.2,
    ends_with_punctuation=False,
    is_bullet=False,
):
    return Line(
        text=text,
        page_number=1,
        font_size=font_size,
        is_bold=is_bold,
        is_italic=False,
        line_index=0,
        word_count=word_count,
        caps_ratio=caps_ratio,
        ends_with_punctuation=ends_with_punctuation,
        is_bullet=is_bullet,
    )


# =========================================
# _estimate_body_font_size() Tests
# =========================================

def test_estimate_body_font_size():

    lines = [
        create_line(
            font_size=12.0,
            is_bold=False,
            word_count=5,
        ),
        create_line(
            font_size=12.0,
            is_bold=False,
            word_count=6,
        ),
        create_line(
            font_size=14.0,
            is_bold=True,
            word_count=2,
        ),
    ]

    result = _estimate_body_font_size(lines)

    assert result == 12.0


def test_estimate_body_font_size_uses_median():

    lines = [
        create_line(font_size=10.0, word_count=5),
        create_line(font_size=12.0, word_count=5),
        create_line(font_size=14.0, word_count=5),
    ]

    result = _estimate_body_font_size(lines)

    assert result == 12.0


def test_estimate_body_font_size_fallback_to_all_sizes():

    lines = [
        create_line(
            font_size=12.0,
            is_bold=True,
            word_count=2,
        ),
        create_line(
            font_size=14.0,
            is_bold=True,
            word_count=2,
        ),
    ]

    result = _estimate_body_font_size(lines)

    assert result == 13.0


def test_estimate_body_font_size_no_valid_sizes():

    lines = [
        create_line(font_size=0.0),
        create_line(font_size=0.0),
    ]

    result = _estimate_body_font_size(lines)

    assert result == 0.0


# =========================================
# detect_headers() Tests
# =========================================

def test_detect_headers_detects_strong_header():

    lines = [
        create_line(
            text="This is normal body text",
            font_size=12.0,
            is_bold=False,
            word_count=6,
            caps_ratio=0.1,
            ends_with_punctuation=True,
        ),
        create_line(
            text="TECHNICAL SKILLS",
            font_size=14.0,
            is_bold=True,
            word_count=2,
            caps_ratio=1.0,
            ends_with_punctuation=False,
        ),
    ]

    result = detect_headers(lines)

    assert len(result) == 1
    assert result[0].line.text == "TECHNICAL SKILLS"
    assert result[0].score == 5


def test_detect_headers_requires_four_signals():

    lines = [
        create_line(
            text="This is normal body text",
            font_size=12.0,
            is_bold=False,
            word_count=6,
            caps_ratio=0.1,
            ends_with_punctuation=True,
        ),
        create_line(
            text="SKILLS",
            font_size=14.0,
            is_bold=True,
            word_count=1,
            caps_ratio=1.0,
            ends_with_punctuation=True,
        ),
    ]

    result = detect_headers(lines)

    assert len(result) == 1
    assert result[0].score == 4


def test_detect_headers_rejects_low_score():

    lines = [
        create_line(
            text="This is normal body text",
            font_size=12.0,
            is_bold=False,
            word_count=6,
            caps_ratio=0.1,
            ends_with_punctuation=True,
        ),
        create_line(
            text="Some normal text here",
            font_size=12.0,
            is_bold=False,
            word_count=4,
            caps_ratio=0.1,
            ends_with_punctuation=False,
        ),
    ]

    result = detect_headers(lines)

    assert result == []


def test_detect_headers_skips_bullets():

    lines = [
        create_line(
            text="This is normal body text",
            font_size=12.0,
            is_bold=False,
            word_count=6,
            caps_ratio=0.1,
            ends_with_punctuation=True,
        ),
        create_line(
            text="SKILLS",
            font_size=16.0,
            is_bold=True,
            word_count=1,
            caps_ratio=1.0,
            ends_with_punctuation=False,
            is_bullet=True,
        ),
    ]

    result = detect_headers(lines)

    assert result == []


def test_detect_headers_preserves_original_line():

    header = create_line(
        text="EDUCATION",
        font_size=16.0,
        is_bold=True,
        word_count=1,
        caps_ratio=1.0,
        ends_with_punctuation=False,
    )

    body = create_line(
        text="This is normal body text",
        font_size=12.0,
        is_bold=False,
        word_count=6,
        caps_ratio=0.1,
        ends_with_punctuation=True,
    )

    result = detect_headers([body, header])

    assert result[0].line is header