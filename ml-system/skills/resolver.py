from .normalization import SkillNormalizer
from .synonym_mapping import SynonymMapper
from .hierarchy import SkillHierarchy


class SkillResolver:

    def __init__(
        self,
        normalizer: SkillNormalizer,
        mapper: SynonymMapper,
        hierarchy: SkillHierarchy
    ):
        self.normalizer = normalizer
        self.mapper = mapper
        self.hierarchy = hierarchy

    def resolve(self, skill_text: str):

        normalized = self.normalizer.normalize(
            skill_text
        )

        canonical_id = self.mapper.map(
            normalized
        )

        if canonical_id is None:
            return None

        return {
            "original": skill_text,
            "normalized": normalized,
            "canonical_id": canonical_id,
            "ancestors": self.hierarchy.get_ancestors(
                canonical_id
            ),
        }