import re


SKILL_DICTIONARY: dict[str, list[str]] = {
    "Python": [
        "python",
        "python programming",
    ],
    "C": [
        "c",
        "c language",
    ],
    "C++": [
        "c++",
        "cpp",
    ],
    "Java": [
        "java",
    ],
    "JavaScript": [
        "javascript",
        "js",
    ],
    "TypeScript": [
        "typescript",
        "ts",
    ],
    "HTML": [
        "html",
    ],
    "CSS": [
        "css",
    ],
    "React": [
        "react",
        "react.js",
        "reactjs",
    ],
    "Node.js": [
        "node.js",
        "nodejs",
    ],
    "Flask": [
        "flask",
    ],
    "Django": [
        "django",
    ],
    "FastAPI": [
        "fastapi",
    ],
    "SQL": [
        "sql",
    ],
    "MySQL": [
        "mysql",
    ],
    "PostgreSQL": [
        "postgresql",
        "postgres",
    ],
    "MongoDB": [
        "mongodb",
        "mongo db",
    ],
    "Git": [
        "git",
    ],
    "GitHub": [
        "github",
    ],
    "Docker": [
        "docker",
    ],
    "Machine Learning": [
        "machine learning",
        "ml",
    ],
    "Deep Learning": [
        "deep learning",
        "dl",
    ],
    "Natural Language Processing": [
        "natural language processing",
        "nlp",
    ],
    "Computer Vision": [
        "computer vision",
    ],
    "PyTorch": [
        "pytorch",
    ],
    "TensorFlow": [
        "tensorflow",
    ],
    "Scikit-learn": [
        "scikit-learn",
        "sklearn",
    ],
    "Pandas": [
        "pandas",
    ],
    "NumPy": [
        "numpy",
    ],
    "OpenCV": [
        "opencv",
        "cv2",
    ],
}

from resume.skill_extraction.models import SkillMatch


def _compile_patterns() -> dict[str, list[re.Pattern]]:
    patterns = {}

    for skill, aliases in SKILL_DICTIONARY.items():
        patterns[skill] = []

        for alias in aliases:
            pattern = re.compile(
                rf"(?<!\w){re.escape(alias)}(?!\w)",
                re.IGNORECASE,
            )
            patterns[skill].append(pattern)

    return patterns


_COMPILED_PATTERNS = _compile_patterns()


def extract_dictionary_skills(
    text: str,
    source_section: str,
) -> list[SkillMatch]:

    matches: list[SkillMatch] = []

    for skill, patterns in _COMPILED_PATTERNS.items():

        for pattern in patterns:

            match = pattern.search(text)

            if not match:
                continue

            matches.append(
                SkillMatch(
                    skill=skill,
                    matched_text=match.group(0),
                    source_section=source_section,
                    method="dictionary",
                    confidence=1.0,
                )
            )

            # One match is enough for this skill in this section.
            break

    return matches