#!/usr/bin/env python3
"""
Usage: python encounter_rates.py <map_name>
Example: python encounter_rates.py lake_verity

Reads res/field/encounters/encounters_<map_name>.json and prints
encounter percentages for morning, day, night, plus swarm and radar tables.
"""

import json
import sys
import os
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ENCOUNTERS_DIR = os.path.join(SCRIPT_DIR, "res", "field", "encounters")

SLOT_PROBS = [15, 15, 10, 10, 10, 10, 8, 8, 5, 5, 2, 2]

# Surf and all fishing rods share the same 5-slot layout, no substitutions ever apply.
SURF_PROBS    = [60, 30, 5, 4, 1]
OLD_ROD_PROBS = [60, 30, 5, 4, 1]
GOOD_ROD_PROBS  = [40, 40, 15, 4, 1]
SUPER_ROD_PROBS = [40, 40, 15, 4, 1]


def aggregate(species_prob: dict[str, float]) -> list[tuple[str, float]]:
    """Return sorted list of (species, total_%) descending."""
    result = sorted(species_prob.items(), key=lambda x: -x[1])
    return result


def build_table(slots: list[str], probs: list[int]) -> dict[str, float]:
    totals: dict[str, float] = defaultdict(float)
    for species, prob in zip(slots, probs):
        totals[species] += prob
    return dict(totals)


def print_table(title: str, rows: list[tuple[str, float]]) -> None:
    print(f"\n{'='*40}")
    print(f"  {title}")
    print(f"{'='*40}")
    for species, pct in rows:
        bar = "#" * int(pct / 2)
        print(f"  {species:<30} {pct:5.1f}%  {bar}")


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <map_name>", file=sys.stderr)
        sys.exit(1)

    map_name = sys.argv[1]
    json_path = os.path.join(ENCOUNTERS_DIR, f"encounters_{map_name}.json")

    if not os.path.isfile(json_path):
        print(f"Error: file not found: {json_path}", file=sys.stderr)
        sys.exit(1)

    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    if "land_encounters" not in data:
        print("No land_encounters in this file.", file=sys.stderr)
        sys.exit(1)

    base_species = [slot["species"] for slot in data["land_encounters"]]

    if len(base_species) != 12:
        print(f"Warning: expected 12 land slots, got {len(base_species)}", file=sys.stderr)

    # --- Morning: base slots, no substitution ---
    morning_slots = base_species[:]

    # --- Day: slots 2 and 3 replaced by day[0] and day[1] ---
    day_slots = base_species[:]
    if "day" in data:
        day_slots[2] = data["day"][0]
        day_slots[3] = data["day"][1]

    # --- Night: slots 2 and 3 replaced by night[0] and night[1] ---
    night_slots = base_species[:]
    if "night" in data:
        night_slots[2] = data["night"][0]
        night_slots[3] = data["night"][1]

    print_table("MORNING", aggregate(build_table(morning_slots, SLOT_PROBS)))
    print_table("DAY / TWILIGHT", aggregate(build_table(day_slots, SLOT_PROBS)))
    print_table("NIGHT / LATE NIGHT", aggregate(build_table(night_slots, SLOT_PROBS)))

    # --- Swarm (replaces slots 0 and 1) ---
    if "swarms" in data:
        swarm_slots = base_species[:]
        swarm_slots[0] = data["swarms"][0]
        swarm_slots[1] = data["swarms"][1]
        # Swarms can combine with day/night substitutions too; show base swarm (morning) for simplicity
        print_table("SWARM (morning, if swarm active)", aggregate(build_table(swarm_slots, SLOT_PROBS)))

    # --- Radar (replaces slots 4, 5, 10, 11) ---
    if "radar" in data:
        radar_slots = base_species[:]
        radar = data["radar"]
        radar_slots[4] = radar[0]
        radar_slots[5] = radar[1]
        radar_slots[10] = radar[2]
        radar_slots[11] = radar[3]
        print_table("POKÉRADAR (morning, chain active)", aggregate(build_table(radar_slots, SLOT_PROBS)))

    # --- Surf (no substitutions) ---
    if "surf_encounters" in data and data.get("surf_rate", 0) > 0:
        surf_species = [slot["species"] for slot in data["surf_encounters"]]
        print_table(f"SURF (rate {data['surf_rate']}%)", aggregate(build_table(surf_species, SURF_PROBS)))

    # --- Fishing (no substitutions) ---
    for rod, probs, rate_key, enc_key in [
        ("OLD ROD",   OLD_ROD_PROBS,   "old_rod_rate",   "old_rod_encounters"),
        ("GOOD ROD",  GOOD_ROD_PROBS,  "good_rod_rate",  "good_rod_encounters"),
        ("SUPER ROD", SUPER_ROD_PROBS, "super_rod_rate", "super_rod_encounters"),
    ]:
        if enc_key in data and data.get(rate_key, 0) > 0:
            rod_species = [slot["species"] for slot in data[enc_key]]
            print_table(f"{rod} (rate {data[rate_key]}%)", aggregate(build_table(rod_species, probs)))

    print()


if __name__ == "__main__":
    main()
