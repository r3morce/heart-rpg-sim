"""
Combat simulation system for Heart RPG.

This module handles combat mechanics, statistics tracking, and battle resolution
between Player Characters (PCs) and Non-Player Characters (NPCs).
"""

import os
import yaml
import random
import copy
from typing import List, Dict, Tuple
from dataclasses import dataclass

from module.yaml_loader import get_all_players
from module.npc import NPC
from module.player import Player
from module.config import SimulationConfig


@dataclass
class CombatStats:
    """Tracks statistics for a single combat encounter."""
    
    # Combat metrics
    rounds: int = 0
    pc_defeats: int = 0
    npc_defeats: int = 0
    total_damage_to_pcs: int = 0
    total_damage_to_npcs: int = 0

    # Per-character tracking dictionaries
    pc_individual_stats: Dict[str, Dict[str, int]] = None
    npc_individual_stats: Dict[str, Dict[str, int]] = None
    pc_damage_received: Dict[str, Dict[str, int]] = None
    pc_fallouts: Dict[str, Dict[str, int]] = None

    def __post_init__(self):
        """Initialize tracking dictionaries if not provided."""
        if self.pc_individual_stats is None:
            self.pc_individual_stats = {}
        if self.npc_individual_stats is None:
            self.npc_individual_stats = {}
        if self.pc_damage_received is None:
            self.pc_damage_received = {}
        if self.pc_fallouts is None:
            self.pc_fallouts = {}


@dataclass
class SimulationResults:
    """Aggregates statistics across multiple combat simulations."""
    
    # Overall fight statistics
    total_fights: int = 0
    pc_victories: int = 0
    npc_victories: int = 0
    draws: int = 0
    average_rounds: float = 0.0
    total_rounds: int = 0

    # Aggregated per-character statistics
    pc_stats: Dict[str, Dict[str, int]] = None
    npc_stats: Dict[str, Dict[str, int]] = None
    pc_damage_taken: Dict[str, Dict[str, int]] = None
    pc_fallout_stats: Dict[str, Dict[str, int]] = None

    def __post_init__(self):
        """Initialize statistics dictionaries if not provided."""
        if self.pc_stats is None:
            self.pc_stats = {}
        if self.npc_stats is None:
            self.npc_stats = {}
        if self.pc_damage_taken is None:
            self.pc_damage_taken = {}
        if self.pc_fallout_stats is None:
            self.pc_fallout_stats = {}

    def add_fight_result(
        self, pc_won: bool, npc_won: bool, rounds: int, combat_stats: "CombatStats"
    ) -> None:
        """Add results from a single combat to the aggregated statistics."""
        self.total_fights += 1
        self.total_rounds += rounds

        # Track victory types
        if pc_won and not npc_won:
            self.pc_victories += 1
        elif npc_won and not pc_won:
            self.npc_victories += 1
        else:
            self.draws += 1

        self.average_rounds = self.total_rounds / self.total_fights

        self._aggregate_pc_stats(combat_stats)
        self._aggregate_npc_stats(combat_stats)
        self._aggregate_damage_stats(combat_stats)
        self._aggregate_fallout_stats(combat_stats)

    def _aggregate_pc_stats(self, combat_stats: "CombatStats") -> None:
        """Aggregate PC attack statistics."""
        for pc_name, stats in combat_stats.pc_individual_stats.items():
            if pc_name not in self.pc_stats:
                self.pc_stats[pc_name] = {"attacks": 0, "hits": 0, "damage": 0}

            self.pc_stats[pc_name]["attacks"] += stats["attacks"]
            self.pc_stats[pc_name]["hits"] += stats["hits"]
            self.pc_stats[pc_name]["damage"] += stats["damage"]

    def _aggregate_npc_stats(self, combat_stats: "CombatStats") -> None:
        """Aggregate NPC attack statistics."""
        for npc_name, stats in combat_stats.npc_individual_stats.items():
            if npc_name not in self.npc_stats:
                self.npc_stats[npc_name] = {"attacks": 0, "hits": 0, "damage": 0}

            self.npc_stats[npc_name]["attacks"] += stats["attacks"]
            self.npc_stats[npc_name]["hits"] += stats["hits"]
            self.npc_stats[npc_name]["damage"] += stats["damage"]

    def _aggregate_damage_stats(self, combat_stats: "CombatStats") -> None:
        """Aggregate PC damage received statistics."""
        for pc_name, damage_stats in combat_stats.pc_damage_received.items():
            if pc_name not in self.pc_damage_taken:
                self.pc_damage_taken[pc_name] = {
                    "blood": 0, "echo": 0, "mind": 0, "fortune": 0, "supplies": 0, "total": 0
                }

            for damage_type, amount in damage_stats.items():
                self.pc_damage_taken[pc_name][damage_type] += amount

    def _aggregate_fallout_stats(self, combat_stats: "CombatStats") -> None:
        """Aggregate PC fallout statistics."""
        for pc_name, fallout_stats in combat_stats.pc_fallouts.items():
            if pc_name not in self.pc_fallout_stats:
                self.pc_fallout_stats[pc_name] = {
                    "minor_fallouts": 0, "major_fallouts": 0, "deaths": 0
                }

            for stat_type, amount in fallout_stats.items():
                self.pc_fallout_stats[pc_name][stat_type] += amount

    def print_summary(self) -> None:
        """Print comprehensive simulation results."""
        self._print_fight_summary()
        self._print_pc_combat_stats()
        self._print_pc_damage_stats()
        self._print_pc_fallout_stats()
        self._print_npc_stats()

    def _print_fight_summary(self) -> None:
        """Print overall fight statistics."""
        print(f"\n=== SIMULATION SUMMARY ===")
        print(f"Total fights: {self.total_fights}")
        print(
            f"PC victories: {self.pc_victories} ({self.pc_victories / self.total_fights * 100:.1f}%)"
        )
        print(
            f"NPC victories: {self.npc_victories} ({self.npc_victories / self.total_fights * 100:.1f}%)"
        )
        print(f"Draws: {self.draws} ({self.draws / self.total_fights * 100:.1f}%)")
        print(f"Average rounds per fight: {self.average_rounds:.1f}")

    def _print_pc_combat_stats(self) -> None:
        """Print PC attack statistics."""
        print(f"\n=== PC STATISTICS ===")
        for pc_name, stats in self.pc_stats.items():
            attacks = stats["attacks"]
            hits = stats["hits"]
            damage = stats["damage"]

            hit_rate = (hits / attacks * 100) if attacks > 0 else 0
            avg_damage = damage / attacks if attacks > 0 else 0

            print(f"{pc_name}:")
            print(f"  Hit rate: {hit_rate:.1f}% ({hits:,}/{attacks:,})")
            print(f"  Average damage per attack: {avg_damage:.2f}")
            print(f"  Total damage dealt: {damage:,}")

    def _print_pc_damage_stats(self) -> None:
        """Print PC damage taken statistics."""
        print(f"\n=== PC DAMAGE TAKEN ===")
        for pc_name, damage_stats in self.pc_damage_taken.items():
            print(f"{pc_name}:")
            print(f"  Blood: {damage_stats['blood']:,}")
            print(f"  Echo: {damage_stats['echo']:,}")
            print(f"  Mind: {damage_stats['mind']:,}")
            print(f"  Fortune: {damage_stats['fortune']:,}")
            print(f"  Supplies: {damage_stats['supplies']:,}")
            print(f"  Total: {damage_stats['total']:,}")

    def _print_pc_fallout_stats(self) -> None:
        """Print PC fallout statistics."""
        print(f"\n=== PC FALLOUT STATISTICS ===")
        for pc_name, fallout_stats in self.pc_fallout_stats.items():
            print(f"{pc_name}:")
            print(f"  Minor fallouts: {fallout_stats['minor_fallouts']:,}")
            print(f"  Major fallouts: {fallout_stats['major_fallouts']:,}")
            print(f"  Deaths: {fallout_stats['deaths']:,}")

    def _print_npc_stats(self) -> None:
        """Print NPC attack statistics."""
        print(f"\n=== NPC STATISTICS ===")
        for npc_name, stats in self.npc_stats.items():
            attacks = stats["attacks"]
            hits = stats["hits"]
            damage = stats["damage"]

            hit_rate = (hits / attacks * 100) if attacks > 0 else 0
            avg_damage = damage / attacks if attacks > 0 else 0

            print(f"{npc_name}:")
            print(f"  Hit rate: {hit_rate:.1f}% ({hits:,}/{attacks:,})")
            print(f"  Average damage per attack: {avg_damage:.2f}")
            print(f"  Total damage dealt: {damage:,}")


class CombatSimulator:
    def __init__(self):
        self.pcs: List[Player] = []
        self.npcs: List[NPC] = []
        self.stats = CombatStats()

    def load_npcs(self, directory: str = "npc") -> List[NPC]:
        """Load all NPC YAML files from the specified directory."""
        npcs = []

        if not os.path.exists(directory):
            return npcs

        for filename in os.listdir(directory):
            if filename.endswith((".yaml", ".yml")):
                filepath = os.path.join(directory, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as file:
                        data = yaml.safe_load(file)
                        if data:
                            npc = NPC.from_dict(data)
                            npcs.append(npc)
                except (yaml.YAMLError, KeyError, TypeError) as e:
                    print(f"Error loading {filepath}: {e}")
                    continue

        return npcs

    def setup_combat(self, pcs: List[Player] = None, npcs: List[NPC] = None):
        """Initialize combat with provided PCs and NPCs, or load from files."""
        if pcs is not None:
            self.pcs = pcs

        if npcs is not None:
            self.npcs = npcs

        self.stats = CombatStats()

    def pc_attack(self, pc: Player, npc: NPC) -> int:
        """Calculate attack success from PC to NPC using d10 system."""
        dice_to_roll = []

        # Base d10 roll
        dice_to_roll.append(random.randint(1, 10))

        # Bonus die for kill ability
        if pc.abilities.kill:
            dice_to_roll.append(random.randint(1, 10))

        # Bonus die for matching domain
        has_matching_domain = False
        for domain_name, has_domain in vars(pc.domains).items():
            if has_domain and domain_name in npc.domains:
                has_matching_domain = True
                break

        if has_matching_domain:
            dice_to_roll.append(random.randint(1, 10))

        # Take highest roll
        highest_roll = max(dice_to_roll)

        # Hit on 6-10
        if highest_roll >= 6:
            # Successful hit - deal weapon damage
            if pc.weapon <= 0:
                weapon_damage = 1  # Minimum damage on successful hit
            else:
                weapon_damage = random.randint(1, pc.weapon)

            # Critical hit on roll of 10 - add +2 to weapon damage
            if highest_roll == 10:
                weapon_damage += 2

            return weapon_damage
        else:
            # Miss
            return 0

    def npc_attack(self, npc: NPC, pc: Player) -> Dict[str, int]:
        """Calculate damage from NPC to PC across resistance types."""
        # Roll d10 for NPC attack - hits on 1-5
        npc_roll = random.randint(1, 10)

        if npc_roll <= 5:
            # NPC hits - deal weapon damage
            if npc.weapon <= 0:
                base_damage = 1  # Minimum damage on successful hit
            else:
                base_damage = random.randint(1, npc.weapon)

            # Critical hit on roll of 1 - double damage
            if npc_roll == 1:
                base_damage *= 2
        else:
            # NPC misses
            base_damage = 0

        # Distribute damage across resistance types
        resistance_types = ["blood", "echo", "mind", "fortune", "supplies"]
        damage_distribution = {}

        if base_damage > 0:
            # Simple distribution: focus on one random resistance type
            target_resistance = random.choice(resistance_types)
            damage_distribution[target_resistance] = base_damage
        else:
            # Miss - no damage to any resistance type
            for resistance_type in resistance_types:
                damage_distribution[resistance_type] = 0

        return damage_distribution

    def apply_pc_damage(self, pc: Player, damage_dist: Dict[str, int]):
        """Apply damage to PC's resistance, checking for fallouts."""
        pc_name = pc.name
        if pc_name not in self.stats.pc_damage_received:
            self.stats.pc_damage_received[pc_name] = {
                "blood": 0,
                "echo": 0,
                "mind": 0,
                "fortune": 0,
                "supplies": 0,
                "total": 0,
            }

        if pc_name not in self.stats.pc_fallouts:
            self.stats.pc_fallouts[pc_name] = {
                "minor_fallouts": 0,
                "major_fallouts": 0,
                "deaths": 0,
            }

        for resistance_type, damage in damage_dist.items():
            current_value = getattr(pc.resistance, resistance_type)
            new_value = min(12, current_value + damage)
            setattr(pc.resistance, resistance_type, new_value)

            # Track damage received by type
            self.stats.pc_damage_received[pc_name][resistance_type] += damage
            self.stats.pc_damage_received[pc_name]["total"] += damage

            # Check for fallout at 12 stress
            if new_value >= 12:
                # Minor fallout - reset resistance to 0
                setattr(pc.resistance, resistance_type, 0)
                pc.minor_fallouts += 1
                self.stats.pc_fallouts[pc_name]["minor_fallouts"] += 1

                # Check for major fallout (every 2 minor fallouts)
                if pc.minor_fallouts % 2 == 0:
                    pc.major_fallouts += 1
                    self.stats.pc_fallouts[pc_name]["major_fallouts"] += 1

                    # Major fallout - clear all stress
                    pc.resistance.blood = 0
                    pc.resistance.echo = 0
                    pc.resistance.mind = 0
                    pc.resistance.fortune = 0
                    pc.resistance.supplies = 0

                    # Check for death (at 2 major fallouts)
                    if pc.is_dead():
                        self.stats.pc_fallouts[pc_name]["deaths"] += 1

    def is_pc_defeated(self, pc: Player) -> bool:
        """Check if PC is defeated (dead from 2 major fallouts)."""
        return pc.is_dead()

    def combat_round(self):
        """Execute one round of combat."""
        self.stats.rounds += 1

        # PCs attack NPCs
        active_pcs = [pc for pc in self.pcs if not self.is_pc_defeated(pc)]
        active_npcs = [npc for npc in self.npcs if not npc.is_defeated()]

        for pc in active_pcs:
            if active_npcs:
                target_npc = random.choice(active_npcs)
                damage = self.pc_attack(pc, target_npc)

                # Track individual PC statistics
                pc_name = pc.name
                if pc_name not in self.stats.pc_individual_stats:
                    self.stats.pc_individual_stats[pc_name] = {
                        "attacks": 0,
                        "hits": 0,
                        "damage": 0,
                    }

                self.stats.pc_individual_stats[pc_name]["attacks"] += 1
                if damage > 0:
                    self.stats.pc_individual_stats[pc_name]["hits"] += 1
                self.stats.pc_individual_stats[pc_name]["damage"] += damage

                target_npc.take_damage(damage)
                self.stats.total_damage_to_npcs += damage

                if target_npc.is_defeated():
                    self.stats.npc_defeats += 1
                    active_npcs.remove(target_npc)

        # NPCs attack PCs
        for npc in active_npcs:
            if active_pcs:
                target_pc = random.choice(active_pcs)
                damage_dist = self.npc_attack(npc, target_pc)
                self.apply_pc_damage(target_pc, damage_dist)

                total_damage = sum(damage_dist.values())

                # Track individual NPC statistics
                npc_name = npc.name
                if npc_name not in self.stats.npc_individual_stats:
                    self.stats.npc_individual_stats[npc_name] = {
                        "attacks": 0,
                        "hits": 0,
                        "damage": 0,
                    }

                self.stats.npc_individual_stats[npc_name]["attacks"] += 1
                if total_damage > 0:
                    self.stats.npc_individual_stats[npc_name]["hits"] += 1
                self.stats.npc_individual_stats[npc_name]["damage"] += total_damage

                self.stats.total_damage_to_pcs += total_damage

                if self.is_pc_defeated(target_pc):
                    self.stats.pc_defeats += 1

    def is_combat_over(self) -> bool:
        """Check if combat should end."""
        active_pcs = [pc for pc in self.pcs if not self.is_pc_defeated(pc)]
        active_npcs = [npc for npc in self.npcs if not npc.is_defeated()]

        return len(active_pcs) == 0 or len(active_npcs) == 0

    def reset_characters(self, original_pcs: List[Player], original_npcs: List[NPC]):
        """Reset all characters to their original state for a new fight."""
        # Deep copy to reset resistance values
        self.pcs = copy.deepcopy(original_pcs)
        self.npcs = copy.deepcopy(original_npcs)
        self.stats = CombatStats()

    def simulate_single_combat(
        self,
        pcs: List[Player] = None,
        npcs: List[NPC] = None,
        max_rounds: int = 20,
        verbose: bool = True,
    ) -> tuple[bool, bool, int]:
        """Run a single combat simulation and return results."""
        self.setup_combat(pcs, npcs)

        if not self.pcs or not self.npcs:
            return False, False, 0

        if verbose:
            print("=== COMBAT BEGINS ===")

        while not self.is_combat_over() and self.stats.rounds < max_rounds:
            self.combat_round()

        if verbose:
            self.print_combat_results()

        # Determine winners
        active_pcs = [pc for pc in self.pcs if not self.is_pc_defeated(pc)]
        active_npcs = [npc for npc in self.npcs if not npc.is_defeated()]

        pc_won = len(active_pcs) > 0 and len(active_npcs) == 0
        npc_won = len(active_npcs) > 0 and len(active_pcs) == 0

        return pc_won, npc_won, self.stats.rounds

    def simulate_multiple_combats(
        self,
        pcs: List[Player] = None,
        npcs: List[NPC] = None,
        config: SimulationConfig = None,
    ) -> SimulationResults:
        """Run multiple combat simulations and collect statistics."""
        if config is None:
            config = SimulationConfig()

        # Load characters if not provided
        if pcs is None:
            pcs = get_all_players()
        if npcs is None:
            npcs = self.load_npcs()

        if not pcs or not npcs:
            print("No PCs or NPCs found for simulation!")
            return SimulationResults()

        # Store original character states
        original_pcs = copy.deepcopy(pcs)
        original_npcs = copy.deepcopy(npcs)

        results = SimulationResults()

        print(f"Running {config.number_of_fights:,} combat simulations...")

        for fight_num in range(config.number_of_fights):
            if (fight_num + 1) % 1000 == 0:
                print(f"Completed {fight_num + 1:,} fights...")

            # Reset characters for new fight
            self.reset_characters(original_pcs, original_npcs)

            # Run single combat
            pc_won, npc_won, rounds = self.simulate_single_combat(
                self.pcs, self.npcs, config.max_rounds_per_fight, config.verbose_output
            )

            results.add_fight_result(pc_won, npc_won, rounds, self.stats)

        if config.show_detailed_results:
            results.print_summary()

        return results

    def print_combat_results(self):
        """Print final combat statistics."""
        print(f"\n=== COMBAT RESULTS ===")
        print(f"Rounds fought: {self.stats.rounds}")
        print(f"PCs defeated: {self.stats.pc_defeats}")
        print(f"NPCs defeated: {self.stats.npc_defeats}")
        print(f"Total damage to PCs: {self.stats.total_damage_to_pcs}")
        print(f"Total damage to NPCs: {self.stats.total_damage_to_npcs}")

        active_pcs = [pc for pc in self.pcs if not self.is_pc_defeated(pc)]
        active_npcs = [npc for npc in self.npcs if not npc.is_defeated()]

        if active_pcs and not active_npcs:
            print("PCs VICTORY!")
        elif active_npcs and not active_pcs:
            print("NPCs VICTORY!")
        else:
            print("DRAW!")

        print(f"\nSurviving PCs: {len(active_pcs)}")
        for pc in active_pcs:
            print(
                f"  {pc.name}: Blood {pc.resistance.blood}, Echo {pc.resistance.echo}, "
                f"Mind {pc.resistance.mind}, Fortune {pc.resistance.fortune}, "
                f"Supplies {pc.resistance.supplies}"
            )

        print(f"\nSurviving NPCs: {len(active_npcs)}")
        for npc in active_npcs:
            print(f"  {npc.name}: {npc.resistance}/{npc.max_resistance} resistance")


def run_combat_simulation(
    pcs: List[Player] = None, npcs: List[NPC] = None, config: SimulationConfig = None
):
    """Main function to run combat simulation."""
    simulator = CombatSimulator()

    if config and config.number_of_fights > 1:
        return simulator.simulate_multiple_combats(pcs, npcs, config)
    else:
        # Single combat for backwards compatibility
        pc_won, npc_won, rounds = simulator.simulate_single_combat(pcs, npcs)
        return pc_won, npc_won, rounds


if __name__ == "__main__":
    run_combat_simulation()
