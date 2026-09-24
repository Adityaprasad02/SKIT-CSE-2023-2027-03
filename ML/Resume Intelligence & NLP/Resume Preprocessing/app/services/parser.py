from pathlib import Path

import pymupdf
from pypdf import PdfReader
from docx import Document


def _extract_pdf_blocks(page):
    """
    Extract useful text blocks from a PDF page.

    Each block contains its position and extracted text.
    """

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

    return valid_blocks


def _reconstruct_page_text(page):
    """
    Reconstruct the reading order of a PDF page.

    Handles:
    - normal single-column resumes
    - resumes containing full-width headers
    - two-column layouts
    - multi-column content

    The method uses block geometry instead of hardcoding
    any particular resume.
    """

    page_width = page.rect.width

    blocks = _extract_pdf_blocks(page)

    if not blocks:
        return ""

    # ---------------------------------------------------------
    # STEP 1: Identify blocks that span most of the page.
    # These are usually:
    # - name
    # - target role
    # - profile header
    # - full-width introductory text
    # ---------------------------------------------------------

    full_width_blocks = []
    content_blocks = []

    for block in blocks:

        width = block["x1"] - block["x0"]
        width_ratio = width / page_width

        if width_ratio >= 0.70:
            full_width_blocks.append(block)
        else:
            content_blocks.append(block)

    # ---------------------------------------------------------
    # If there are too few content blocks, treat the page
    # as a normal single-column page.
    # ---------------------------------------------------------

    if len(content_blocks) < 2:

        blocks.sort(
            key=lambda block: (
                block["y0"],
                block["x0"],
            )
        )

        return "\n".join(
            block["text"]
            for block in blocks
        )

    # ---------------------------------------------------------
    # STEP 2: Detect whether the remaining content is actually
    # arranged into columns.
    #
    # We examine the x positions of blocks and find a large
    # horizontal gap between groups.
    # ---------------------------------------------------------

    content_blocks.sort(
        key=lambda block: block["x0"]
    )

    x_positions = [
        block["x0"]
        for block in content_blocks
    ]

    largest_gap = 0
    split_index = None

    for i in range(len(x_positions) - 1):

        gap = x_positions[i + 1] - x_positions[i]

        if gap > largest_gap:
            largest_gap = gap
            split_index = i

    # ---------------------------------------------------------
    # If there is no meaningful horizontal separation,
    # use normal top-to-bottom reading order.
    # ---------------------------------------------------------

    if (
        split_index is None
        or largest_gap < page_width * 0.12
    ):

        ordered_blocks = sorted(
            blocks,
            key=lambda block: (
                block["y0"],
                block["x0"],
            )
        )

        return "\n".join(
            block["text"]
            for block in ordered_blocks
        )

    # ---------------------------------------------------------
    # STEP 3: Create left and right columns.
    # ---------------------------------------------------------

    split_x = (
        x_positions[split_index]
        + x_positions[split_index + 1]
    ) / 2

    left_column = []
    right_column = []

    for block in content_blocks:

        center_x = (
            block["x0"] + block["x1"]
        ) / 2

        if center_x < split_x:
            left_column.append(block)
        else:
            right_column.append(block)

    # ---------------------------------------------------------
    # Check whether the split is meaningful.
    # If one side contains almost everything, don't treat it
    # as a two-column layout.
    # ---------------------------------------------------------

    if (
        len(left_column) == 0
        or len(right_column) == 0
    ):

        ordered_blocks = sorted(
            blocks,
            key=lambda block: (
                block["y0"],
                block["x0"],
            )
        )

        return "\n".join(
            block["text"]
            for block in ordered_blocks
        )

    # ---------------------------------------------------------
    # STEP 4: Sort each column vertically.
    # ---------------------------------------------------------

    left_column.sort(
        key=lambda block: (
            block["y0"],
            block["x0"],
        )
    )

    right_column.sort(
        key=lambda block: (
            block["y0"],
            block["x0"],
        )
    )

    # ---------------------------------------------------------
    # STEP 5: Handle full-width blocks.
    #
    # Full-width blocks that appear before the columns
    # should come first.
    # ---------------------------------------------------------

    first_column_y = min(
        block["y0"]
        for block in content_blocks
    )

    header_blocks = []
    remaining_full_width = []

    for block in full_width_blocks:

        if block["y0"] <= first_column_y:
            header_blocks.append(block)
        else:
            remaining_full_width.append(block)

    header_blocks.sort(
        key=lambda block: (
            block["y0"],
            block["x0"],
        )
    )

    remaining_full_width.sort(
        key=lambda block: (
            block["y0"],
            block["x0"],
        )
    )

    # ---------------------------------------------------------
    # STEP 6: Build final reading order.
    #
    # Header
    # ↓
    # Left column
    # ↓
    # Right column
    # ↓
    # Any remaining full-width content
    # ---------------------------------------------------------

    ordered_blocks = []

    ordered_blocks.extend(header_blocks)
    ordered_blocks.extend(left_column)
    ordered_blocks.extend(right_column)
    ordered_blocks.extend(remaining_full_width)

    # ---------------------------------------------------------
    # STEP 7: Convert blocks into text.
    # ---------------------------------------------------------

    page_text = []

    for block in ordered_blocks:

        text = block["text"].strip()

        if text:
            page_text.append(text)

    return "\n".join(page_text)


def extract_pdf_text_layout_aware(file_path: str) -> str:
    """
    Extract PDF text while attempting to preserve
    the natural reading order of the resume.
    """

    document = pymupdf.open(file_path)

    pages = []

    for page in document:

        page_text = _reconstruct_page_text(page)

        if page_text.strip():
            pages.append(page_text)

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

    PDF:
        First attempts layout-aware extraction.
        Falls back to pypdf if necessary.

    DOCX:
        Extracts non-empty paragraphs.
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