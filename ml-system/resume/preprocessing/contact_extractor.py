import re
from dataclasses import dataclass

EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")
PHONE_PATTERN = re.compile(r"(?:\+\d{1,3}[\s\-]?)?\d{10}")
LINKEDIN_PATTERN = re.compile(r"(?:https?://)?(?:www\.)?linkedin\.com/in/[A-Za-z0-9\-_/]+", re.IGNORECASE)
GITHUB_PATTERN = re.compile(r"(?:https?://)?(?:www\.)?github\.com/[A-Za-z0-9\-_/]+", re.IGNORECASE)


@dataclass
class ContactInfo:
    emails: list[str]
    phones: list[str]
    linkedin: list[str]
    github: list[str]


def extract_contact_info(text: str) -> ContactInfo:
    """Regex extraction for structured, format-defined fields (emails,
    phone numbers, profile URLs). This is not the same class of problem
    as section-header classification — these patterns are defined by
    syntax, not by topic, so hardcoding the pattern is the correct
    approach here."""

    return ContactInfo(
        emails=sorted(set(EMAIL_PATTERN.findall(text))),
        phones=sorted(set(PHONE_PATTERN.findall(text))),
        linkedin=sorted(set(LINKEDIN_PATTERN.findall(text))),
        github=sorted(set(GITHUB_PATTERN.findall(text))),
    )
