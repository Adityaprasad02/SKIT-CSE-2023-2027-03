import pymupdf


def extract_text_from_pdf(file_path: str) -> str:

    document = None

    try:
        document = pymupdf.open(file_path)

        text_parts = []

        for page_number, page in enumerate(document, start=1):

            page_text = page.get_text("text").strip()

            if page_text:
                text_parts.append(page_text)

        extracted_text = "\n\n".join(text_parts)

        if not extracted_text.strip():
            raise ValueError(
                "No readable text found in the PDF."
            )

        return extracted_text.strip()

    except Exception as error:
        raise RuntimeError(
            f"Failed to parse PDF: {error}"
        )

    finally:
        if document is not None:
            document.close()