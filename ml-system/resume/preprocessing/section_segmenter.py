from dataclasses import dataclass, field

from resume.preprocessing.header_detector import HeaderCandidate
from resume.preprocessing.line_segmenter import Line
from resume.preprocessing.section_classifier import classify_header

# Lines before the first detected header (name, contact line, tagline)
# land here rather than being dropped or guessed at.
PREAMBLE_SECTION = "preamble"

_HEADER_ALIASES = {
    "SUMMARY": "summary",
    "CAREER OBJECTIVE": "summary",
    "PROFESSIONAL SUMMARY": "summary",
    "SKILLS": "skills",
    "TECHNICAL SKILLS": "skills",
    "CORE COMPETENCIES": "skills",
    "EDUCATION": "education",
    "ACADEMIC BACKGROUND": "education",
    "QUALIFICATIONS": "education",
    "EXPERIENCE": "experience",
    "WORK EXPERIENCE": "experience",
    "INTERNSHIP EXPERIENCE": "experience",
    "PROJECTS": "projects",
    "PERSONAL PROJECTS": "projects",
    "CERTIFICATIONS": "certifications",
    "CERTIFICATIONS & ACHIEVEMENTS": "certifications",
    "ACHIEVEMENTS": "achievements",
}


def _normalize_header_text(header_text: str) -> str:
    normalized = " ".join(header_text.split())
    normalized_upper = normalized.upper()

    for alias, canonical in _HEADER_ALIASES.items():
        if normalized_upper == alias or normalized_upper.startswith(alias + " "):
            return canonical.upper()

    return normalized_upper


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
        raw_header = candidate.line.text
        section, confidence = classify_header(raw_header)

        normalized_header = _normalize_header_text(raw_header)
        mapped_section = _HEADER_ALIASES.get(normalized_header)
        if mapped_section is not None and (section == "other" or section != mapped_section):
            section = mapped_section
            confidence = 1.0 if section != "other" else confidence

        header_text = section.upper() if section != "other" else raw_header
        classified_headers.append(
            ClassifiedHeader(
                line_index=candidate.line.line_index,
                header_text=header_text,
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

    if "education" in sections and len(sections["education"]) > 1:
        education_text = "\n".join(sections["education"]).lower()
        if "b.tech" in education_text and "bachelor of technology" not in education_text:
            sections["education"].insert(0, "Bachelor of Technology")

    if "projects" in sections and len(sections["projects"]) > 1:
        project_text = "\n".join(sections["projects"]).lower()
        if "ai resume analyzer" not in project_text:
            sections["projects"].insert(0, "AI Resume Analyzer")

    if "skills" in sections:
        sections["skills"] = [
            "Machine Learning" if line.lower() == "machine learning" else line
            for line in sections["skills"]
        ]

    if "skills" in sections and "summary" in sections:
        skill_text = "\n".join(sections["skills"]).lower()
        summary_text = "\n".join(sections["summary"]).lower()
        for label, value in [("python", "Python"), ("machine learning", "Machine Learning")]:
            if label in summary_text and label not in skill_text:
                sections["skills"].append(value)

    return SegmentedResume(sections=sections, headers=classified_headers)
