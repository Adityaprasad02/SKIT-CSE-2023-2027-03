
import re
import unicodedata


def preprocess_resume(text: str) -> str:
    """
    Clean extracted resume text while preserving section
    headings, line breaks, and meaningful content.

    This function does not extract text from files;
    that responsibility belongs to parser.py.
    """

    if not isinstance(text, str):
        raise TypeError("Resume text must be a string.")

    if not text.strip():
        return ""

    # Normalize Unicode characters.
    text = unicodedata.normalize("NFKC", text)

    # Normalize common line-ending formats.
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove null bytes and other control characters,
    # while preserving newlines and tabs.
    text = "".join(
        char
        for char in text
        if char in "\n\t" or unicodedata.category(char)[0] != "C"
    )

    cleaned_lines = []

    for line in text.split("\n"):
        # Replace tabs with spaces.
        line = line.replace("\t", " ")

        # Normalize repeated whitespace within a line.
        line = re.sub(r"[ ]+", " ", line).strip()

        # Preserve non-empty lines, including headings.
        if line:
            cleaned_lines.append(line)

    # Use one newline between lines and remove leading/trailing space.
    return "\n".join(cleaned_lines).strip()
