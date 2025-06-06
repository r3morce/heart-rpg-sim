# Heart RPG Combat Simulator

A comprehensive combat simulation system for the Heart RPG tabletop game. This simulator runs thousands of combat encounters between Player Characters (PCs) and Non-Player Characters (NPCs) to analyze combat balance and character effectiveness.

## Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Simulation**:
   ```bash
   python main.py
   ```

3. **View Results**: The simulation will output detailed statistics after completing all fights.

## Project Structure

```
heart-rpg-sim/
├── main.py                 # Entry point - runs combat simulations
├── config.yaml             # Simulation configuration
├── requirements.txt        # Python dependencies
├── pc/                     # Player Character definitions
│   ├── daniel.yaml
│   ├── marc.yaml
│   └── player.yaml
├── npc/                    # Non-Player Character definitions
│   └── guard.yaml
└── module/                 # Core simulation modules
    ├── combat.py           # Combat mechanics and simulation
    ├── config.py           # Configuration loading
    ├── npc.py              # NPC class definition
    ├── player.py           # PC class definition
    └── yaml_loader.py      # YAML file loading utilities
```

## Configuration

Edit `config.yaml` to customize simulation parameters:

```yaml
simulation:
  number_of_fights: 10000      # Total simulations to run
  max_rounds_per_fight: 20     # Maximum rounds per combat
  verbose_output: false        # Print individual combat details
  show_detailed_results: true  # Print comprehensive statistics
```

## Character Definitions


## Adding New Characters

### Adding a PC
1. Create a new YAML file in the `pc/` directory
2. Define all required fields (name, class, calling, abilities, domains, weapon, resistance)
3. The simulator will automatically load it on next run

### Adding an NPC
1. Create a new YAML file in the `npc/` directory
2. Define required fields (name, weapon, domains, resistance, protection)
3. The simulator will automatically load it on next run

## Development

### Key Classes

- **`Player`**: PC with abilities, domains, resistances, and fallout tracking
- **`NPC`**: Simplified enemy with weapon, domains, resistance, and protection
- **`CombatSimulator`**: Handles combat logic and character interactions
- **`CombatStats`**: Tracks statistics for individual fights
- **`SimulationResults`**: Aggregates statistics across multiple simulations

### Combat Flow

1. Load PCs and NPCs from YAML files
2. For each simulation:
   - Reset character states
   - Run combat rounds until victory/defeat/timeout
3. Aggregate and display results

### Extending the System

To add new mechanics:
1. Update character classes in `module/player.py` or `module/npc.py`
2. Modify combat logic in `module/combat.py`
3. Add new statistics tracking as needed
4. Update YAML schemas for new character properties

## Dependencies

- **Python 3.8+**
- **PyYAML**: YAML file parsing
- **Standard Library**: random, copy, dataclasses, typing

## License

This project is for educational and game analysis purposes. Heart RPG is owned by its respective creators.
