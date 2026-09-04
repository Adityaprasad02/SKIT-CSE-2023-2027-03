import re


def clean_text(text: str) -> str:
    """
    Clean and normalize extracted resume text.
    """

    # Normalize line breaks
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Fix words broken across PDF line breaks.
    # Example: "latency re-\nduction" -> "latency reduction"
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)

    # Replace bullet characters with a normal space
    text = text.replace("•", " ")

    # Normalize tabs and multiple spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Remove unnecessary spaces around line breaks
    text = re.sub(r" *\n *", "\n", text)

    # Reduce excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Keep useful resume characters:
    # letters, numbers, spaces, and common punctuation
    text = re.sub(
        r"[^\w\s@.+#&()/,%:'\-]",
        "",
        text
    )

    # Remove spaces at the beginning and end of each line
    lines = [line.strip() for line in text.split("\n")]

    # Remove completely empty lines
    lines = [line for line in lines if line]

    return "\n".join(lines)


def preprocess_resume(text: str) -> str:
    """
    Complete resume preprocessing pipeline.
    """

    if not text or not text.strip():
        return ""

    return clean_text(text)