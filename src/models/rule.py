from dataclasses import dataclass

@dataclass
class Rule:
    id: int
    name: str
    category: str
    description: str
