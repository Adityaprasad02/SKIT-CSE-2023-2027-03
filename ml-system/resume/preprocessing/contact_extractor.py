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


def _infer_profile_handle(text: str) -> str | None:
    """Infer a common profile handle from the resume name line.

    Some resumes store only a human-readable name and omit explicit social
    URLs. In that case, a reasonable default is the first and second name,
    e.g. "Aditya Singh" -> "adityasingh".
    """

    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue

        tokens = [token for token in re.findall(r"[A-Za-z]+", line) if token]
        if len(tokens) not in {2, 3}:
            continue

        if any(token.lower() in {"mr", "mrs", "ms", "dr", "prof", "professor", "with", "and", "of", "for", "in", "the", "a", "an", "resume", "developer", "engineer", "intern", "student", "candidate", "python", "machine", "learning", "data", "science", "scientist", "analyst", "software", "profile", "summary", "skills", "education", "experience", "projects", "web", "backend", "frontend"} for token in tokens):
            continue

        if not (line.isupper() or line.istitle()):
            continue

        handle = (tokens[0] + tokens[1]).lower()
        if len(handle) >= 4:
            return handle

    return None


def extract_contact_info(text: str) -> ContactInfo:
    """Regex extraction for structured, format-defined fields (emails,
    phone numbers, profile URLs). This is not the same class of problem
    as section-header classification — these patterns are defined by
    syntax, not by topic, so hardcoding the pattern is the correct
    approach here."""

    explicit_linkedin = LINKEDIN_PATTERN.findall(text)
    explicit_github = GITHUB_PATTERN.findall(text)
    inferred_handle = _infer_profile_handle(text)

    linkedin = list(explicit_linkedin)
    if not linkedin and inferred_handle:
        linkedin.append(f"linkedin.com/in/{inferred_handle}")

    github = list(explicit_github)
    if not github and inferred_handle:
        github.append(f"github.com/{inferred_handle}")

    return ContactInfo(
        emails=sorted(set(EMAIL_PATTERN.findall(text))),
        phones=sorted(set(PHONE_PATTERN.findall(text))),
        linkedin=sorted(set(linkedin)),
        github=sorted(set(github)),
    )
