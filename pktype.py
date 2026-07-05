#!/usr/bin/env python3
import json
import sys
from pathlib import Path


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <type>", file=sys.stderr)
        sys.exit(1)

    search_type = sys.argv[1].upper()
    pokemon_dir = Path(__file__).parent / "res" / "pokemon"

    print(f"{'Name':<30} {'Type1':<20} {'Type2'}")
    print("-" * 60)

    seen = set()
    for json_file in sorted(pokemon_dir.glob("*/data.json")):
        try:
            data = json.loads(json_file.read_text())
        except (json.JSONDecodeError, OSError):
            continue

        types = data.get("types", [])
        if any(search_type in t.upper() for t in types):
            name = "SPECIES_" + json_file.parent.name.upper().replace(" ", "_")
            if name in seen:
                continue
            seen.add(name)
            type1 = types[0] if len(types) > 0 else ""
            type2 = types[1] if len(types) > 1 and types[1] != types[0] else ""
            print(f"{name:<30} {type1:<20} {type2}")


if __name__ == "__main__":
    main()
