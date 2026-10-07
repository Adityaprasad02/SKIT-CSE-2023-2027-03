import json
from pathlib import Path


class SkillHierarchy:

    def __init__(self, relationships_path: str | Path):

        relationships_path = Path(
            relationships_path
        )

        with relationships_path.open(
            "r",
            encoding="utf-8"
        ) as file:
            self.relationships = json.load(file)

    def get_parent(self, skill_id: str) -> str | None:

        relationship = self.relationships.get(
            skill_id
        )

        if relationship is None:
            return None

        return relationship.get("parent")

    def get_children(self, skill_id: str) -> list[str]:

        children = []

        for current_skill, relationship in (
            self.relationships.items()
        ):

            if relationship.get("parent") == skill_id:
                children.append(current_skill)

        return children

    def get_ancestors(self, skill_id: str) -> list[str]:

        ancestors = []

        current = self.get_parent(skill_id)

        while current is not None:

            ancestors.append(current)

            current = self.get_parent(current)

        return ancestors