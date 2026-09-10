import pymupdf

from resume.parsing.models import RawLine


def extract_text_from_pdf(file_path: str) -> str:
    """Plain-text extraction. Kept for backward compatibility / quick use
    cases that don't need layout info (e.g. full-text search indexing)."""

    document = None

    try:
        document = pymupdf.open(file_path)

        text_parts = []

        for page in document:
            page_text = page.get_text("text").strip()

            if page_text:
                text_parts.append(page_text)

        extracted_text = "\n\n".join(text_parts)

        if not extracted_text.strip():
            raise ValueError("No readable text found in the PDF.")

        return extracted_text.strip()

    except Exception as error:
        raise RuntimeError(f"Failed to parse PDF: {error}") from error

    finally:
        if document is not None:
            document.close()


def extract_lines_from_pdf(file_path: str) -> list[RawLine]:
    """Structured extraction: one RawLine per visual line, carrying font
    size / bold / italic flags pulled from the PDF's own layout data.

    Used by the preprocessing pipeline to detect section headers by how
    they look on the page, rather than by matching against a fixed list
    of expected header strings.
    """

    document = None

    try:
        document = pymupdf.open(file_path)

        lines: list[RawLine] = []
        line_index = 0

        for page_number, page in enumerate(document, start=1):
            page_dict = page.get_text("dict")

            for block in page_dict.get("blocks", []):
                if "lines" not in block:
                    continue  # image or non-text block

                for line in block["lines"]:
                    spans = line.get("spans", [])

                    line_text = "".join(span["text"] for span in spans).strip()

                    if not line_text:
                        continue

                    # Use the first span's font attributes as representative
                    # of the line. Mixed-formatting lines are rare in resumes
                    # and not worth the complexity of per-span splitting here.
                    first_span = spans[0]
                    font_flags = first_span.get("flags", 0)

                    # PyMuPDF span flags: bit 4 (16) = bold-ish (serif/bold),
                    # bit 1 (2) = italic. We also treat "Bold" in the font
                    # name as a signal since some fonts don't set the flag.
                    font_name = first_span.get("font", "")
                    is_bold = bool(font_flags & 2**4) or "bold" in font_name.lower()
                    is_italic = bool(font_flags & 2**1) or "italic" in font_name.lower()

                    lines.append(
                        RawLine(
                            text=line_text,
                            page_number=page_number,
                            font_size=round(first_span.get("size", 0.0), 1),
                            is_bold=is_bold,
                            is_italic=is_italic,
                            line_index=line_index,
                        )
                    )
                    line_index += 1

        if not lines:
            raise ValueError("No readable text found in the PDF.")

        return lines

    except Exception as error:
        raise RuntimeError(f"Failed to extract structured lines from PDF: {error}") from error

    finally:
        if document is not None:
            document.close()