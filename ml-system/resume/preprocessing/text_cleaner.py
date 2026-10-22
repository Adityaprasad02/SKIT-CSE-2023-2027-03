import re
import unicodedata


def clean_text(text: str) -> str:
    """
    Clean general text extraction artifacts while preserving
    meaningful resume content and technical characters.

    This function intentionally does NOT:
    - lowercase text
    - remove punctuation
    - remove numbers
    - remove technical symbols such as +, #, or .
    """

    if not isinstance(text, str):
        raise TypeError("Input text must be a string.")

    # 1. Unicode normalization
    text = unicodedata.normalize("NFKC", text)

    # 2. Normalize line endings
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # 3. Replace non-breaking spaces with normal spaces
    text = text.replace("\u00A0", " ")

    # 4. Remove zero-width and invisible characters
    invisible_characters = [
        "\u200B",  # Zero-width space
        "\u200C",  # Zero-width non-joiner
        "\u200D",  # Zero-width joiner
        "\uFEFF",  # Zero-width no-break space
    ]

    for char in invisible_characters:
        text = text.replace(char, "")

    # 5. Remove excessive spaces and tabs within lines
    lines = []

    for line in text.split("\n"):
        line = re.sub(r"[ \t]+", " ", line)
        lines.append(line.strip())

    # 6. Limit consecutive empty lines
    cleaned_lines = []
    empty_line_count = 0

    for line in lines:
        if line == "":
            empty_line_count += 1
            if empty_line_count <= 1:
                cleaned_lines.append(line)
        else:
            empty_line_count = 0
            cleaned_lines.append(line)

    return "\n".join(cleaned_lines).strip()
