from dataclasses import dataclass

from resume.parsing.parser import parse_resume_structured
from resume.preprocessing.contact_extractor import ContactInfo, extract_contact_info
from resume.preprocessing.header_detector import detect_headers
from resume.preprocessing.line_segmenter import segment_lines
from resume.preprocessing.section_segmenter import SegmentedResume, segment_sections


@dataclass
class PreprocessedResume:
    full_text: str
    sections: dict[str, str]
    contact_info: ContactInfo
    detected_headers: list[str]  # for debugging / QA, not for downstream logic


def preprocess_resume(file_path: str) -> PreprocessedResume:
    """End-to-end: file path -> structured, section-labeled resume.

    Pipeline stages:
      1. parse_resume_structured   raw text + layout metadata per line
      2. segment_lines             clean text, derive per-line features
      3. detect_headers            flag header-like lines (structural)
      4. segment_sections          classify headers semantically, bucket
                                    every line under its section
      5. extract_contact_info      regex-pull emails/phone/links
    """

    raw_lines = parse_resume_structured(file_path)
    lines = segment_lines(raw_lines)
    header_candidates = detect_headers(lines)
    segmented: SegmentedResume = segment_sections(lines, header_candidates)

    full_text = "\n".join(line.text for line in sorted(lines, key=lambda l: l.line_index))
    contact_info = extract_contact_info(full_text)

    sections = {name: segmented.section_text(name) for name in segmented.sections}

    return PreprocessedResume(
        full_text=full_text,
        sections=sections,
        contact_info=contact_info,
        detected_headers=[h.header_text for h in segmented.headers],
    )
