from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class NPC:
    name: str
    weapon: int
    domains: List[str]
    resistance: int
    protection: int
    max_resistance: int = field(init=False)

    def __post_init__(self):
        self.max_resistance = self.resistance

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "NPC":
        return cls(
            name=data["name"],
            weapon=data["weapon"],
            domains=data["domains"],
            resistance=data["resistance"],
            protection=data["protection"],
        )

    def is_defeated(self) -> bool:
        return self.resistance <= 0

    def take_damage(self, damage: int):
        actual_damage = max(0, damage - self.protection)
        self.resistance -= actual_damage
        if self.resistance < 0:
            self.resistance = 0
