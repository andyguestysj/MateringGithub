from dataclasses import dataclass

@dataclass
class Character:
    id: int
    name: str
    character_class: str
    level: str
    description: str
