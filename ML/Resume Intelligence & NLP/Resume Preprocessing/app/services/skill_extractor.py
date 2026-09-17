import re


SKILL_ALIASES = {
    "python": "Python",
    "java": "Java",
    "c": "C",
    "c++": "C++",
    "c#": "C#",
    "kotlin": "Kotlin",
    "javascript": "JavaScript",
    "typescript": "TypeScript",

    "android": "Android",
    "android development": "Android Development",
    "navigation component": "Navigation Component",
    "mvvm": "MVVM",
    "mvc": "MVC",
    "data binding": "Data Binding",
    "view models": "View Models",
    "live data": "LiveData",
    "coroutines": "Coroutines",
    "retrofit": "Retrofit",

    "data structures": "Data Structures",
    "algorithms": "Algorithms",
    "oop": "Object-Oriented Programming",
    "oops": "Object-Oriented Programming",
    "object oriented programming": "Object-Oriented Programming",
    "problem solving": "Problem Solving",

    "git": "Git",
    "jira": "Jira",
    "azure devops": "Azure DevOps",
    "agile": "Agile",
    "solid": "SOLID",
    "ci/cd": "CI/CD",
    "restful api": "REST API",
    "rest api": "REST API",

    "sentry": "Sentry",
    "repository design pattern": "Repository Design Pattern",
    "diffie-hellman": "Diffie-Hellman",
    "upi": "UPI",
}


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
        "object oriented programming",
        "problem solving",
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
    Check whether a skill exists as a complete term.
    """

    pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

    return bool(re.search(pattern, text, re.IGNORECASE))


def extract_skills(skills_text: str) -> dict:
    """
    Extract and normalize skills from the Skills section.
    """

    result = {}

    for category, skills in SKILL_CATEGORIES.items():

        found_skills = set()

        for skill in skills:

            if find_skill(skills_text, skill):

                canonical_name = SKILL_ALIASES.get(
                    skill,
                    skill
                )

                found_skills.add(canonical_name)

        result[category] = sorted(found_skills)

    return result