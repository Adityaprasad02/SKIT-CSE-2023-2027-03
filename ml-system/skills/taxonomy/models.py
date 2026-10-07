from dataclasses import dataclass, field


@dataclass
class Skill:
    id: str
    name: str
    category: str
    subcategory: str | None = None
    parent_id: str | None = None
    aliases: list[str] = field(default_factory=list)