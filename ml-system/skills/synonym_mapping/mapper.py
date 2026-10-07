from pathlib import Path
import json


class SynonymMapper:

    def __init__(
        self,
        mapping_path: str | Path,
        taxonomy=None
    ):

        mapping_path = Path(mapping_path)

        with mapping_path.open(
            "r",
            encoding="utf-8"
        ) as file:
            self.mappings = json.load(file)

        self.taxonomy = taxonomy

    def map(self, skill: str) -> str:

        skill = skill.lower().strip()

        canonical_id = self.mappings.get(
            skill
        )

        if canonical_id is not None:
            return canonical_id

        if self.taxonomy:
            canonical = self.taxonomy.get_by_name(skill)

            if canonical:
                return canonical.id

        return None