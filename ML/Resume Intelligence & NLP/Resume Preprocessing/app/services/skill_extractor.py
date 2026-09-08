import re


SKILL_CATEGORIES = {
    "programming_languages": [
        "python",
        "java",
        "c",
        "c++",
        "c#",
        "kotlin",
        "javascript",
        "typescript",
        "go",
        "rust",
    ],

    "mobile_development": [
        "android",
        "android development",
        "navigation component",
        "mvvm",
        "mvc",
        "data binding",
        "view models",
        "live data",
        "coroutines",
        "retrofit",
    ],

    "computer_science": [
        "data structures",
        "algorithms",
        "oop",
        "oops",
        "problem solving",
        "object oriented programming",
    ],

    "tools_and_practices": [
        "git",
        "jira",
        "azure devops",
        "agile",
        "solid",
        "ci/cd",
        "restful api",
        "rest api",
    ],

    "other_technologies": [
        "sentry",
        "repository design pattern",
        "diffie-hellman",
        "upi",
    ],
}


def find_skill(text: str, skill: str) -> bool:
    """
    Check whether a skill exists in the text.
    """

    pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

    return bool(re.search(pattern, text, re.IGNORECASE))


def extract_skills(skills_text: str) -> dict:
    """
    Extract skills from the resume Skills section.
    """

    result = {}

    for category, skills in SKILL_CATEGORIES.items():

        found_skills = []

        for skill in skills:
            if find_skill(skills_text, skill):
                found_skills.append(skill)

        result[category] = found_skills

    return result