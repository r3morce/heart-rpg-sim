import yaml
from typing import Dict, Any
from dataclasses import dataclass


@dataclass
class SimulationConfig:
    number_of_fights: int = 1000
    max_rounds_per_fight: int = 20
    verbose_output: bool = False
    show_detailed_results: bool = True

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SimulationConfig':
        simulation_data = data.get('simulation', {})
        return cls(
            number_of_fights=simulation_data.get('number_of_fights', 1000),
            max_rounds_per_fight=simulation_data.get('max_rounds_per_fight', 20),
            verbose_output=simulation_data.get('verbose_output', False),
            show_detailed_results=simulation_data.get('show_detailed_results', True)
        )


def load_config(config_path: str = 'config.yaml') -> SimulationConfig:
    """Load configuration from YAML file."""
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
            return SimulationConfig.from_dict(data)
    except (FileNotFoundError, yaml.YAMLError) as e:
        print(f"Error loading config from {config_path}: {e}")
        print("Using default configuration")
        return SimulationConfig()