from docx import Document


def extract_text_from_docx(file_path: str) -> str:

    try:
        document = Document(file_path)

        text_parts = []


        for paragraph in document.paragraphs:
            text = paragraph.text.strip()

            if text:
                text_parts.append(text)

        for table in document.tables:
            for row in table.rows:

                row_text = []

                for cell in row.cells:
                    cell_text = cell.text.strip()

                    if cell_text:
                        row_text.append(cell_text)

                if row_text:
                    text_parts.append(" | ".join(row_text))

        extracted_text = "\n".join(text_parts)

        if not extracted_text.strip():
            raise ValueError(
                "No readable text found in the DOCX file."
            )

        return extracted_text.strip()

    except Exception as error:
        raise RuntimeError(
            f"Failed to parse DOCX: {error}"
        )