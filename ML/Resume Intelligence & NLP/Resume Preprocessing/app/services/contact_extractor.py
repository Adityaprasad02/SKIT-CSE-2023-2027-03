import re


def extract_email(text: str):
    """
    Extract email address from resume text.
    """

    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"

    match = re.search(pattern, text)

    return match.group(0) if match else None


def extract_phone(text: str):
    """
    Extract Indian phone number from resume text.
    """

    pattern = r"(?:\+91[\s-]?)?[6-9]\d{9}\b"

    match = re.search(pattern, text)

    return match.group(0) if match else None


def extract_linkedin(text: str):
    """
    Extract LinkedIn profile if available.
    """

    pattern = r"(?:https?://)?(?:www\.)?linkedin\.com/[A-Za-z0-9_/?=&%-]+"

    match = re.search(pattern, text, re.IGNORECASE)

    return match.group(0) if match else None


def extract_github(text: str):
    """
    Extract GitHub profile if available.
    """

    pattern = r"(?:https?://)?(?:www\.)?github\.com/[A-Za-z0-9_-]+"

    match = re.search(pattern, text, re.IGNORECASE)

    return match.group(0) if match else None


def extract_leetcode(text: str):
    """
    Extract LeetCode profile if available.
    """

    pattern = r"(?:https?://)?(?:www\.)?leetcode\.com/[A-Za-z0-9_-]+"

    match = re.search(pattern, text, re.IGNORECASE)

    return match.group(0) if match else None


def extract_location(text: str):
    """
    Extract location from the resume contact line.
    """

    lines = [line.strip() for line in text.split("\n") if line.strip()]

    if len(lines) < 2:
        return None

    second_line = lines[1]

    # Email usually marks the end of the location
    if "@" in second_line:
        location = second_line.split("@")[0]

        # Remove contact separators and trailing spaces
        location = re.split(r"\s*(?:⋄|\||•)\s*", location)[0]

        return location.strip()

    return second_line


def extract_name(text: str):
    """
    Extract the name from the first non-empty line.
    """

    lines = [line.strip() for line in text.split("\n") if line.strip()]

    if not lines:
        return None

    return lines[0]


def extract_contact_information(text: str) -> dict:
    """
    Extract contact information from resume text.
    """

    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "location": extract_location(text),
        "linkedin": extract_linkedin(text),
        "github": extract_github(text),
        "leetcode": extract_leetcode(text),
    }