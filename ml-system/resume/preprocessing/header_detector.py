import statistics
from dataclasses import dataclass

from resume.preprocessing.line_segmenter import Line

# Tunable, but these are structural thresholds (how much bigger than body
# text, how short, how capitalized) — not a list of expected words.
FONT_SIZE_MARGIN = 1.0      # header font must exceed body font by this much
MAX_HEADER_WORDS = 5
MIN_CAPS_RATIO = 0.7
SIGNALS_REQUIRED = 4        # out of 5 soft signals, see below


@dataclass
class HeaderCandidate:
    line: Line
    score: int  # 0-4, how many structural signals fired


def _estimate_body_font_size(lines: list[Line]) -> float:
    """Body text is the most common non-bold, multi-word font size in the
    document. Falls back to the overall median if nothing qualifies (e.g.
    a resume with no bold text at all)."""

    body_sizes = [
        line.font_size
        for line in lines
        if not line.is_bold and line.word_count >= 4 and line.font_size > 0
    ]

    if body_sizes:
        return statistics.median(body_sizes)

    all_sizes = [line.font_size for line in lines if line.font_size > 0]
    return statistics.median(all_sizes) if all_sizes else 0.0


def detect_headers(lines: list[Line]) -> list[HeaderCandidate]:
    """Flag lines that look like section headers based on how they're
    formatted relative to the rest of the document: bolder/larger than
    body text, short, high capitalization, no trailing punctuation.

    Deliberately does not check line text against any fixed vocabulary,
    so novel header phrasing ("Tech Arsenal", "What I Bring") is still
    caught here — classifying *which* section it maps to happens
    separately in section_classifier.py.

    Boldness is a *soft* signal, not a requirement: some resume templates
    render section headers via size/spacing alone without bold. Bullets
    remain a hard filter since we've never seen a bulleted line double as
    a section header.
    """

    body_font_size = _estimate_body_font_size(lines)
    candidates: list[HeaderCandidate] = []

    for line in lines:
        if line.is_bullet:
            continue

        score = 0

        if line.is_bold:
            score += 1
        if line.font_size > body_font_size + FONT_SIZE_MARGIN:
            score += 1
        if line.caps_ratio >= MIN_CAPS_RATIO:
            score += 1
        if line.word_count <= MAX_HEADER_WORDS:
            score += 1
        if not line.ends_with_punctuation:
            score += 1

        if score >= SIGNALS_REQUIRED:
            candidates.append(HeaderCandidate(line=line, score=score))

    return candidates