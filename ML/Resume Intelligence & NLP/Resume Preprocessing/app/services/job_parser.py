import re


def clean_job_description(text: str) -> str:
    """
    Clean and normalize a job description.
    """

    if not text or not text.strip():
        return ""

    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Normalize spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove unnecessary spaces around line breaks
    text = re.sub(r" *\n *", "\n", text)

    return text.strip()


def parse_job_description(text: str) -> dict:
    """
    Parse a job description into basic structured information.
    """

    cleaned_text = clean_job_description(text)

    return {
        "raw_text": text,
        "cleaned_text": cleaned_text,
        "length": len(cleaned_text),
        "lines": [
            line.strip()
            for line in cleaned_text.split("\n")
            if line.strip()
        ]
    }