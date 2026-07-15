#!/usr/bin/env python3
import json
import sys
from pathlib import Path


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <type>", file=sys.stderr)
        sys.exit(1)

    search_type = sys.argv[1].lower()
    moves_dir = Path(__file__).parent / "res" / "moves"

    results = []
    for json_file in sorted(moves_dir.glob("**/*.json")):
        try:
            data = json.loads(json_file.read_text())
        except (json.JSONDecodeError, OSError):
            continue

        move_type = data.get("type", "")
        if search_type in move_type.lower():
            effect = data.get("effect", {})
            results.append({
                "name": data.get("name", ""),
                "class": data.get("class", ""),
                "power": data.get("power", 0),
                "accuracy": data.get("accuracy", 0),
                "pp": data.get("pp", 0),
                "effect_type": effect.get("type", "") if isinstance(effect, dict) else "",
            })

    if not results:
        print(f"No moves found with type containing '{search_type}'.")
        return

    print(f"{'Move':<30} {'Class':<20} {'Power':<8} {'Accuracy':<10} {'PP':<6} {'Effect'}")
    print("-" * 110)
    for move in results:
        move_id = "MOVE_" + move["name"].upper().replace(" ", "_").replace("-", "_")
        print(f"{move_id:<30} {move['class']:<20} {move['power']:<8} {move['accuracy']:<10} {move['pp']:<6} {move['effect_type']}")


if __name__ == "__main__":
    main()
