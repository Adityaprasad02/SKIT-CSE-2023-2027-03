from pathlib import Path

from .models import RawLine
from .pdf_parser import extract_lines_from_pdf, extract_text_from_pdf
from .docx_parser import extract_lines_from_docx, extract_text_from_docx


SUPPORTED_FORMATS = [".pdf", ".docx"]


def _validate(file_path: str) -> Path:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Resume file not found: {file_path}")

    if path.suffix.lower() not in SUPPORTED_FORMATS:
        raise ValueError(
            f"Unsupported file format: {path.suffix.lower()}. "
            f"Supported formats: {SUPPORTED_FORMATS}"
        )

    return path


def parse_resume(file_path: str) -> str:
    """Plain-text extraction. Use this when you just need raw text
    (e.g. full-text search)."""

    path = _validate(file_path)

    if path.suffix.lower() == ".pdf":
        return extract_text_from_pdf(file_path)

    return extract_text_from_docx(file_path)


def parse_resume_structured(file_path: str) -> list[RawLine]:
    """Layout-aware extraction. Use this for anything downstream that needs
    to reason about document structure — section detection, header
    classification, etc. This is the entry point the preprocessing
    pipeline (resume/preprocessing/pipeline.py) consumes."""

    path = _validate(file_path)

    if path.suffix.lower() == ".pdf":
        return extract_lines_from_pdf(file_path)

    return extract_lines_from_docx(file_path)