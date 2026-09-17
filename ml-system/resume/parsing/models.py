from dataclasses import dataclass


@dataclass
class RawLine:
    """A single line of text plus the layout signals we need downstream.

    These fields are populated purely from document structure (font size,
    boldness, position) — never from what the text says. That's what lets
    header_detector.py work without a hardcoded keyword list.

    Lives here (not in pdf_parser.py) so docx_parser.py doesn't have to
    depend on the PDF parser just to get this class.
    """
    text: str
    page_number: int
    font_size: float
    is_bold: bool
    is_italic: bool
    line_index: int  # position of this line within the whole document