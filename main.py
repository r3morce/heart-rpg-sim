import argparse
import logging

from module.yaml_loader import get_all_players
from module.combat import run_combat_simulation, CombatSimulator
from module.config import load_config

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument(
    "--debug",
    action="store_true",
    default=False,
    help="Enable debug mode and debug logging",
)

args = parser.parse_args()
DEBUG = args.debug


if DEBUG:
    logging.getLogger().setLevel(logging.DEBUG)
    logging.debug("Debug mode enabled")


def main():
    # Load configuration
    config = load_config()
    logging.info(f"Configuration loaded: {config.number_of_fights:,} fights")
    
    # Load all players and NPCs
    players = get_all_players()
    
    # Load NPCs using combat simulator's method
    simulator = CombatSimulator()
    npcs = simulator.load_npcs()
    
    logging.info(f"Loaded {len(players)} players and {len(npcs)} NPCs")
    
    # Start combat simulation with config
    results = run_combat_simulation(players, npcs, config)
    
    if hasattr(results, 'total_fights'):
        logging.info(f"Simulation completed: {results.total_fights:,} fights processed")


if __name__ == "__main__":
    main()
