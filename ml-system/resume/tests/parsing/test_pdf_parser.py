from unittest.mock import MagicMock, patch

import pytest

from resume.parsing.pdf_parser import (
    extract_text_from_pdf,
    extract_lines_from_pdf,
)


# =========================================
# extract_text_from_pdf() Tests
# =========================================

@patch("resume.parsing.pdf_parser.pymupdf.open")
def test_extract_text_from_pdf(mock_open):

    page1 = MagicMock()
    page1.get_text.return_value = "First page"

    page2 = MagicMock()
    page2.get_text.return_value = "Second page"

    document = MagicMock()
    document.__iter__.return_value = [page1, page2]

    mock_open.return_value = document

    result = extract_text_from_pdf("resume.pdf")

    assert result == "First page\n\nSecond page"

    document.close.assert_called_once()


@patch("resume.parsing.pdf_parser.pymupdf.open")
def test_extract_text_from_pdf_ignores_empty_pages(mock_open):

    page1 = MagicMock()
    page1.get_text.return_value = "First page"

    page2 = MagicMock()
    page2.get_text.return_value = "   "

    document = MagicMock()
    document.__iter__.return_value = [page1, page2]

    mock_open.return_value = document

    result = extract_text_from_pdf("resume.pdf")

    assert result == "First page"

    document.close.assert_called_once()


@patch("resume.parsing.pdf_parser.pymupdf.open")
def test_extract_text_from_pdf_no_readable_text(mock_open):

    page = MagicMock()
    page.get_text.return_value = "   "

    document = MagicMock()
    document.__iter__.return_value = [page]

    mock_open.return_value = document

    with pytest.raises(RuntimeError, match="No readable text found"):
        extract_text_from_pdf("empty.pdf")

    document.close.assert_called_once()


@patch("resume.parsing.pdf_parser.pymupdf.open")
def test_extract_text_from_pdf_open_failure(mock_open):

    mock_open.side_effect = Exception("Invalid PDF")

    with pytest.raises(RuntimeError, match="Failed to parse PDF"):
        extract_text_from_pdf("broken.pdf")


# =========================================
# extract_lines_from_pdf() Tests
# =========================================

@patch("resume.parsing.pdf_parser.pymupdf.open")
def test_extract_lines_from_pdf(mock_open):

    page = MagicMock()

    page.get_text.return_value = {
        "blocks": [
            {
                "lines": [
                    {
                        "spans": [
                            {
                                "text": "Python Developer",
                                "size": 16.0,
                                "flags": 16,
                                "font": "Arial Bold",
                            }
                        ]
                    }
                ]
            }
        ]
    }

    document = MagicMock()
    document.__iter__.return_value = [page]

    mock_open.return_value = document

    result = extract_lines_from_pdf("resume.pdf")

    assert len(result) == 1

    line = result[0]

    assert line.text == "Python Developer"
    assert line.page_number == 1
    assert line.font_size == 16.0
    assert line.is_bold is True
    assert line.is_italic is False
    assert line.line_index == 0

    document.close.assert_called_once()


@patch("resume.parsing.pdf_parser.pymupdf.open")
def test_extract_lines_from_pdf_skips_non_text_blocks(mock_open):

    page = MagicMock()

    page.get_text.return_value = {
        "blocks": [
            {
                "image": "image-data"
            },
            {
                "lines": [
                    {
                        "spans": [
                            {
                                "text": "Education",
                                "size": 14.0,
                                "flags": 0,
                                "font": "Arial",
                            }
                        ]
                    }
                ]
            }
        ]
    }

    document = MagicMock()
    document.__iter__.return_value = [page]

    mock_open.return_value = document

    result = extract_lines_from_pdf("resume.pdf")

    assert len(result) == 1
    assert result[0].text == "Education"


@patch("resume.parsing.pdf_parser.pymupdf.open")
def test_extract_lines_from_pdf_skips_empty_lines(mock_open):

    page = MagicMock()

    page.get_text.return_value = {
        "blocks": [
            {
                "lines": [
                    {
                        "spans": [
                            {
                                "text": "   ",
                                "size": 12.0,
                                "flags": 0,
                                "font": "Arial",
                            }
                        ]
                    },
                    {
                        "spans": [
                            {
                                "text": "Python",
                                "size": 12.0,
                                "flags": 0,
                                "font": "Arial",
                            }
                        ]
                    }
                ]
            }
        ]
    }

    document = MagicMock()
    document.__iter__.return_value = [page]

    mock_open.return_value = document

    result = extract_lines_from_pdf("resume.pdf")

    assert len(result) == 1
    assert result[0].text == "Python"
    assert result[0].line_index == 0


@patch("resume.parsing.pdf_parser.pymupdf.open")
def test_extract_lines_from_pdf_no_readable_lines(mock_open):

    page = MagicMock()

    page.get_text.return_value = {
        "blocks": []
    }

    document = MagicMock()
    document.__iter__.return_value = [page]

    mock_open.return_value = document

    with pytest.raises(RuntimeError, match="No readable text found"):
        extract_lines_from_pdf("empty.pdf")

    document.close.assert_called_once()