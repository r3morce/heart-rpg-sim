from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class PlayerAbilities:
    compel: bool = False
    delve: bool = False
    discern: bool = False
    endure: bool = False
    evade: bool = False
    hunt: bool = False
    kill: bool = False
    mend: bool = False
    sneak: bool = False


@dataclass
class PlayerDomains:
    cursed: bool = False
    desolate: bool = False
    haven: bool = False
    occult: bool = False
    religion: bool = False
    techology: bool = False
    warren: bool = False
    wild: bool = False


@dataclass
class PlayerResistance:
    blood: int = 0
    echo: int = 0
    mind: int = 0
    fortune: int = 0
    supplies: int = 0

    def __post_init__(self):
        # Ensure resistance values are between 0 and 12
        for field in ["blood", "echo", "mind", "fortune", "supplies"]:
            value = getattr(self, field)
            if value < 0:
                setattr(self, field, 0)
            elif value > 12:
                setattr(self, field, 12)


@dataclass
class Player:
    name: str
    player_class: str
    calling: str
    abilities: PlayerAbilities
    domains: PlayerDomains
    weapon: int
    resistance: PlayerResistance
    minor_fallouts: int = 0
    major_fallouts: int = 0
    
    def is_dead(self) -> bool:
        return self.major_fallouts >= 2

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Player":
        abilities_data = data.get("abilities", {})
        domains_data = data.get("domains", {})
        resistance_data = data.get("resistance", {})

        abilities = PlayerAbilities(**abilities_data)
        domains = PlayerDomains(**domains_data)
        resistance = PlayerResistance(**resistance_data)

        return cls(
            name=data["name"],
            player_class=data["class"],
            calling=data["calling"],
            abilities=abilities,
            domains=domains,
            weapon=data["weapon"],
            resistance=resistance,
        )
