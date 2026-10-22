from dataclasses import dataclass, field

from resume.preprocessing.header_detector import HeaderCandidate
from resume.preprocessing.line_segmenter import Line
from resume.preprocessing.section_classifier import classify_header

# Lines before the first detected header (name, contact line, tagline)
# land here rather than being dropped or guessed at.
PREAMBLE_SECTION = "preamble"


@dataclass
class ClassifiedHeader:
    line_index: int
    header_text: str
    section: str
    confidence: float


@dataclass
class SegmentedResume:
    sections: dict[str, list[str]] = field(default_factory=dict)
    headers: list[ClassifiedHeader] = field(default_factory=list)

    def section_text(self, section: str) -> str:
        return "\n".join(self.sections.get(section, []))


def segment_sections(lines: list[Line], header_candidates: list[HeaderCandidate]) -> SegmentedResume:
    header_line_indices = {c.line.line_index: c for c in header_candidates}

    classified_headers: list[ClassifiedHeader] = []
    for candidate in header_candidates:
        section, confidence = classify_header(candidate.line.text)
        classified_headers.append(
            ClassifiedHeader(
                line_index=candidate.line.line_index,
                header_text=candidate.line.text,
                section=section,
                confidence=confidence,
            )
        )

    # line_index -> assigned section, in document order
    header_by_index = {h.line_index: h.section for h in classified_headers}

    sections: dict[str, list[str]] = {}
    current_section = PREAMBLE_SECTION

    for line in sorted(lines, key=lambda l: l.line_index):
        if line.line_index in header_line_indices:

            detected_section = header_by_index[line.line_index]

            if detected_section != "other":
                current_section = detected_section
                sections.setdefault(current_section, [])
                continue

            # If this is an unrecognized header/subheading,
            # keep it inside the current section
            sections.setdefault(current_section, [])
            sections[current_section].append(line.text)
            continue

        sections.setdefault(current_section, [])
        sections[current_section].append(line.text)

    return SegmentedResume(sections=sections, headers=classified_headers)
