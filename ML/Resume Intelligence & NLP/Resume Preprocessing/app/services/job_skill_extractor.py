import re


KNOWN_SKILLS = [
    "Python",
    "Java",
    "C",
    "C++",
    "Kotlin",
    "JavaScript",
    "TypeScript",

    "Android",
    "Android Development",
    "Navigation Component",
    "MVVM",
    "MVC",
    "Data Binding",
    "View Models",
    "LiveData",
    "Coroutines",
    "Retrofit",

    "Data Structures",
    "Algorithms",
    "OOP",
    "Object-Oriented Programming",
    "Problem Solving",

    "Git",
    "Jira",
    "Azure DevOps",
    "Agile",
    "SOLID",
    "CI/CD",
    "REST API",

    "Docker"
]


def extract_job_skills(job_description: str) -> list[str]:
    """
    Extract known technical skills mentioned
    in a job description.
    """

    if not job_description or not job_description.strip():
        return []

    found_skills = []

    for skill in KNOWN_SKILLS:

        # Handle REST APIs / REST API
        skill_pattern = skill

        if skill.lower() == "rest api":
            skill_pattern = r"rest(?:ful)?\s+apis?"

        else:
            skill_pattern = re.escape(skill)

        pattern = r"(?<!\w)" + skill_pattern + r"(?!\w)"

        if re.search(
            pattern,
            job_description,
            re.IGNORECASE
        ):
            found_skills.append(skill)

    return sorted(set(found_skills))