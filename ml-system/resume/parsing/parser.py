from pathlib import Path

from .pdf_parser import extract_text_from_pdf
from .docx_parser import extract_text_from_docx


SUPPORTED_FORMATS = [".pdf", ".docx"]


def parse_resume(file_path: str) -> str:

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Resume file not found: {file_path}"
        )

    file_extension = path.suffix.lower()

    if file_extension not in SUPPORTED_FORMATS:
        raise ValueError(
            f"Unsupported file format: {file_extension}. "
            f"Supported formats: {SUPPORTED_FORMATS}"
        )

    if file_extension == ".pdf":
        return extract_text_from_pdf(file_path)

    if file_extension == ".docx":
        return extract_text_from_docx(file_path)