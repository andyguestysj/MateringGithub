from dataclasses import dataclass

@dataclass
class Monster:
    id: int
    name: str
    challenge_rating: str
    description: str
