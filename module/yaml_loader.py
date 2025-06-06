import os
import yaml
from typing import List
from module.player import Player


def load_yaml_files(directory: str = "pc") -> List[Player]:
    players = []

    if not os.path.exists(directory):
        return players

    for filename in os.listdir(directory):
        if filename.endswith((".yaml", ".yml")):
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as file:
                    data = yaml.safe_load(file)
                    if data:  # Skip empty files
                        player = Player.from_dict(data)
                        players.append(player)
            except (yaml.YAMLError, KeyError, TypeError) as e:
                print(f"Error loading {filepath}: {e}")
                continue

    return players


def get_all_players() -> List[Player]:
    """Convenience function to load all players from the default pc/ directory."""
    return load_yaml_files()
