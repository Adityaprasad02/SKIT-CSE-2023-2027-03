import re


def lowercase(text: str) -> str:
    return text.lower()


def strip_whitespace(text: str) -> str:
    return text.strip()


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text)


def normalize_punctuation(text: str) -> str:
    """
    Normalize punctuation that commonly varies in skill names.
    """
    text = text.replace("_", " ")
    text = text.replace("-", " ")

    return text


def normalize(text: str) -> str:

    if not isinstance(text, str):
        raise TypeError("Skill text must be a string")

    text = lowercase(text)
    text = normalize_punctuation(text)
    text = normalize_whitespace(text)
    text = strip_whitespace(text)

    return text