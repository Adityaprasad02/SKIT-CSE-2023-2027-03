from pathlib import Path
from unittest.mock import patch

import pytest

from resume.parsing.parser import (
    _validate,
    parse_resume,
    parse_resume_structured,
)


# =========================================
# _validate() Tests
# =========================================

def test_validate_existing_pdf(tmp_path):
    file = tmp_path / "resume.pdf"
    file.touch()

    result = _validate(str(file))

    assert result == file


def test_validate_existing_docx(tmp_path):
    file = tmp_path / "resume.docx"
    file.touch()

    result = _validate(str(file))

    assert result == file


def test_validate_file_not_found():
    with pytest.raises(FileNotFoundError):
        _validate("nonexistent_resume.pdf")


def test_validate_unsupported_format(tmp_path):
    file = tmp_path / "resume.txt"
    file.touch()

    with pytest.raises(ValueError):
        _validate(str(file))


# =========================================
# parse_resume() Tests
# =========================================

@patch("resume.parsing.parser.extract_text_from_pdf")
def test_parse_resume_routes_pdf(mock_extract, tmp_path):

    file = tmp_path / "resume.pdf"
    file.touch()

    mock_extract.return_value = "PDF resume text"

    result = parse_resume(str(file))

    assert result == "PDF resume text"

    mock_extract.assert_called_once_with(str(file))


@patch("resume.parsing.parser.extract_text_from_docx")
def test_parse_resume_routes_docx(mock_extract, tmp_path):

    file = tmp_path / "resume.docx"
    file.touch()

    mock_extract.return_value = "DOCX resume text"

    result = parse_resume(str(file))

    assert result == "DOCX resume text"

    mock_extract.assert_called_once_with(str(file))


# =========================================
# parse_resume_structured() Tests
# =========================================

@patch("resume.parsing.parser.extract_lines_from_pdf")
def test_parse_resume_structured_routes_pdf(mock_extract, tmp_path):

    file = tmp_path / "resume.pdf"
    file.touch()

    mock_extract.return_value = []

    result = parse_resume_structured(str(file))

    assert result == []

    mock_extract.assert_called_once_with(str(file))


@patch("resume.parsing.parser.extract_lines_from_docx")
def test_parse_resume_structured_routes_docx(mock_extract, tmp_path):

    file = tmp_path / "resume.docx"
    file.touch()

    mock_extract.return_value = []

    result = parse_resume_structured(str(file))

    assert result == []

    mock_extract.assert_called_once_with(str(file))