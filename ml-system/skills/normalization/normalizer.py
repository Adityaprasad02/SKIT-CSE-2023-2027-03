from .rules import normalize


class SkillNormalizer:

    def normalize(self, skill_text: str) -> str:
        return normalize(skill_text)