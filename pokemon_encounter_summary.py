import json
import os
from collections import defaultdict

ENCOUNTERS_DIR = os.path.join(os.path.dirname(__file__), "..", "res", "field", "encounters")

# Methods with list-of-objects format (each item has a "species" key)
OBJECT_METHODS = [
    "land_encounters",
    "surf_encounters",
    "old_rod_encounters",
    "good_rod_encounters",
    "super_rod_encounters",
]

# Methods with list-of-strings format (each item is a species string directly)
STRING_METHODS = [
    "swarms",
    "day",
    "night",
    "radar",
]

ALL_METHODS = OBJECT_METHODS + STRING_METHODS

# pokemon_data[species][map_name] = set of methods
pokemon_data = defaultdict(lambda: defaultdict(set))

for filename in os.listdir(ENCOUNTERS_DIR):
    if not filename.endswith(".json"):
        continue

    map_name = filename.removeprefix("encounters_").removesuffix(".json")
    filepath = os.path.join(ENCOUNTERS_DIR, filename)

    with open(filepath, "r") as f:
        data = json.load(f)

    for method in OBJECT_METHODS:
        for entry in data.get(method, []):
            species = entry.get("species", "")
            if species and species != "SPECIES_NONE":
                pokemon_data[species][map_name].add(method)

    for method in STRING_METHODS:
        for species in data.get(method, []):
            if species and species != "SPECIES_NONE":
                pokemon_data[species][map_name].add(method)

records = []
for species, maps in pokemon_data.items():
    maps_serializable = {map_name: sorted(methods) for map_name, methods in maps.items()}
    all_methods_used = set(method for methods in maps.values() for method in methods)
    records.append({
        "name": species,
        "map_count": len(maps),
        "maps": maps_serializable,
        "method_count": len(all_methods_used),
    })

records.sort(key=lambda r: r["map_count"], reverse=True)

output_path = os.path.join(os.path.dirname(__file__), "..", "pokemon_encounter_summary.json")
with open(output_path, "w") as f:
    json.dump(records, f, indent=4)

print(f"Pokemon unici trovati: {len(records)}")
print(f"Output salvato in: {os.path.abspath(output_path)}")

# Build map -> list of species
map_data = defaultdict(set)
for record in records:
    for map_name in record["maps"]:
        map_data[map_name].add(record["name"])

txt_path = os.path.join(os.path.dirname(__file__), "..", "pokemon_encounter_by_map.txt")
with open(txt_path, "w") as f:
    for map_name in sorted(map_data.keys()):
        f.write("##################\n")
        f.write(f"{map_name}\n")
        f.write("##################\n")
        for species in sorted(map_data[map_name]):
            f.write(f"{species}\n")
        f.write("\n")

print(f"Output per mappa salvato in: {os.path.abspath(txt_path)}")
