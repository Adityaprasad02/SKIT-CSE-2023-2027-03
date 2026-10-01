import re


STOPWORDS = {
    "and",
    "or",
    "the",
    "a",
    "an",
    "with",
    "using",
    "used",
    "for",
    "of",
    "in",
    "on",
    "to",
    "from",
    "by",
    "as",
    "at",
    "is",
    "are",
    "was",
    "were",
}


TECHNICAL_TOKEN_PATTERN = re.compile(
    r"""
    [A-Za-z][A-Za-z0-9+#.\-/]*
    """,
    re.VERBOSE,
)


def _is_technical_token(token: str) -> bool:
    token_lower = token.lower()

    if token_lower in STOPWORDS:
        return False

    # Useful indicators of technical terms.
    return (
        any(char.isupper() for char in token)
        or any(char.isdigit() for char in token)
        or any(char in "+#./-" for char in token)
    )


def extract_phrase_candidates(text: str) -> list[str]:
    """
    Extract conservative technical phrase candidates.

    This does not decide that every candidate is definitely a skill.
    It produces candidates for later validation/ranking.
    """

    candidates: list[str] = []

    for line in text.splitlines():

        tokens = TECHNICAL_TOKEN_PATTERN.findall(line)

        current_phrase: list[str] = []

        for token in tokens:

            if _is_technical_token(token):
                current_phrase.append(token)

            else:
                if current_phrase:
                    candidates.append(" ".join(current_phrase))
                    current_phrase = []

        if current_phrase:
            candidates.append(" ".join(current_phrase))

    return candidates