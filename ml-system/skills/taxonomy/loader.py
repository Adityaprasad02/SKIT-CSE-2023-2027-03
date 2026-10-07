import json
from pathlib import Path

from .models import Skill


class Taxonomy:

    def __init__(self, skills: list[Skill]):
        self.skills = skills

        self.by_id = {
            skill.id: skill
            for skill in skills
        }

        self.by_name = {
            skill.name.lower(): skill
            for skill in skills
        }

    def get_by_id(self, skill_id: str) -> Skill | None:
        return self.by_id.get(skill_id)

    def get_by_name(self, name: str) -> Skill | None:
        return self.by_name.get(name.lower())

    def all_skills(self) -> list[Skill]:
        return self.skills


def load_taxonomy(path: str | Path) -> Taxonomy:

    path = Path(path)

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    skills = [
        Skill(**skill_data)
        for skill_data in data["skills"]
    ]

    return Taxonomy(skills)