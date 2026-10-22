import re
from dataclasses import dataclass

from resume.parsing.models import RawLine
from resume.preprocessing.text_cleaner import clean_text

BULLET_PREFIXES = ("•", "▸", "‣", "◦", "·", "-", "*", "○", "■")


@dataclass
class Line:
    """A cleaned line plus features derived purely from its own text/layout.
    No section-level judgment happens here — that's header_detector's job."""

    text: str
    page_number: int
    font_size: float
    is_bold: bool
    is_italic: bool
    line_index: int
    word_count: int
    caps_ratio: float  # fraction of alphabetic chars that are uppercase
    ends_with_punctuation: bool
    is_bullet: bool


def _strip_bullet(text: str) -> str:
    stripped = text.strip()
    if stripped and stripped[0] in BULLET_PREFIXES:
        return stripped[1:].strip()
    return stripped


def _caps_ratio(text: str) -> float:
    letters = [c for c in text if c.isalpha()]
    if not letters:
        return 0.0
    upper = sum(1 for c in letters if c.isupper())
    return upper / len(letters)


def segment_lines(raw_lines: list[RawLine]) -> list[Line]:
    """Clean each raw line's text and attach derived features that later
    stages (header_detector, section_classifier) read instead of matching
    against hardcoded strings."""

    lines: list[Line] = []

    for raw in raw_lines:
        text = clean_text(raw.text)

        if not text:
            continue

        is_bullet = text.strip()[0] in BULLET_PREFIXES if text.strip() else False
        display_text = _strip_bullet(text) if is_bullet else text

        if not display_text:
            continue

        word_count = len(re.findall(r"\S+", display_text))
        ends_with_punctuation = display_text.rstrip()[-1:] in ".,;:" if display_text.rstrip() else False

        lines.append(
            Line(
                text=display_text,
                page_number=raw.page_number,
                font_size=raw.font_size,
                is_bold=raw.is_bold,
                is_italic=raw.is_italic,
                line_index=raw.line_index,
                word_count=word_count,
                caps_ratio=_caps_ratio(display_text),
                ends_with_punctuation=ends_with_punctuation,
                is_bullet=is_bullet,
            )
        )

    return lines