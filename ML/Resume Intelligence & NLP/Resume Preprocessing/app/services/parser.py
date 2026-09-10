from pathlib import Path

import fitz
from pypdf import PdfReader
from docx import Document


def extract_pdf_text_layout_aware(file_path: str) -> str:
    """
    Extract PDF text while preserving a more natural reading order.

    Uses PyMuPDF text blocks and their page coordinates.
    """

    document = fitz.open(file_path)

    pages = []

    for page in document:
        blocks = page.get_text("blocks")

        valid_blocks = []

        for block in blocks:
            if len(block) < 5:
                continue

            x0, y0, x1, y1, text = block[:5]

            text = text.strip()

            if not text:
                continue

            valid_blocks.append(
                {
                    "x0": x0,
                    "y0": y0,
                    "x1": x1,
                    "y1": y1,
                    "text": text,
                }
            )

        # Sort primarily from top to bottom,
        # then from left to right.
        valid_blocks.sort(
            key=lambda block: (
                round(block["y0"], 1),
                block["x0"],
            )
        )

        page_text = []

        for block in valid_blocks:
            page_text.append(block["text"])

        pages.append("\n".join(page_text))

    document.close()

    return "\n".join(pages)


def extract_pdf_text_fallback(file_path: str) -> str:
    """
    Fallback PDF extraction using pypdf.
    """

    reader = PdfReader(file_path)

    pages = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages.append(text)

    return "\n".join(pages)


def extract_docx_text(file_path: str) -> str:
    """
    Extract text from DOCX.
    """

    document = Document(file_path)

    paragraphs = []

    for paragraph in document.paragraphs:
        text = paragraph.text.strip()

        if text:
            paragraphs.append(text)

    return "\n".join(paragraphs)


def extract_text(file_path: str) -> str:
    """
    Extract text from PDF or DOCX.
    """

    extension = Path(file_path).suffix.lower()

    if extension == ".pdf":

        try:
            text = extract_pdf_text_layout_aware(file_path)

            if text.strip():
                return text

        except Exception:
            pass

        return extract_pdf_text_fallback(file_path)

    if extension == ".docx":
        return extract_docx_text(file_path)

    raise ValueError(
        "Unsupported file format. Please upload a PDF or DOCX file."
    )