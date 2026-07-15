#!/usr/bin/env python3
import sys
import json

if len(sys.argv) < 2:
    print("Usage: pkinfo.sh <pokemon_name>")
    sys.exit(1)

path = f"res/pokemon/{sys.argv[1].lower()}/data.json"

try:
    with open(path) as f:
        data = json.load(f)
except FileNotFoundError:
    print(f"File not found: {path}")
    sys.exit(1)

print("=== BASE STATS ===")
stat_order = ["hp", "attack", "defense", "special_attack", "special_defense", "speed"]
stats = data["base_stats"]
for stat in stat_order:
    print(f"  {stat:<16}: {stats[stat]}")
print(f"  {'-'*20}")
print(f"  {'total':<16}: {sum(stats[s] for s in stat_order)}")

print(f"\n=== BASE EXP REWARD ===")
print(f"  {data['base_exp_reward']}")

print("\n=== TYPES ===")
for t in dict.fromkeys(data["types"]):
    print(t)

print("\n=== ABILITIES ===")
for a in data["abilities"]:
    if a != "ABILITY_NONE":
        print(a)

print("\n=== LEARNSET BY LEVEL ===")
print(f"{'Lv':<6} {'Move':<30} {'Class':<20} {'Power':<8} {'Accuracy':<10} {'PP':<6} {'Effect'}")
print("-" * 85)
for level, move in data["learnset"]["by_level"]:
    move_name = move.removeprefix("MOVE_").lower()
    move_path = f"res/moves/{move_name}/data.json"
    try:
        with open(move_path) as f:
            move_data = json.load(f)
        cls = move_data.get("class", "")
        power = move_data.get("power", 0)
        accuracy = move_data.get("accuracy", 0)
        pp = move_data.get("pp", 0)
        effect = move_data.get("effect", {})
        effect_type = effect.get("type", "") if isinstance(effect, dict) else ""
    except FileNotFoundError:
        cls = power = accuracy = pp = effect_type = ""
    print(f"{'Lv '+str(level):<6} {move:<30} {cls:<20} {power:<8} {accuracy:<10} {pp:<6} {effect_type}")

print("\n=== LEARNSET BY TM ===")
print(f"{'TM':<8} {'Move':<30} {'Class':<20} {'Power':<8} {'Accuracy':<10} {'PP':<6} {'Effect'}")
print("-" * 87)
for tm in data["learnset"]["by_tm"]:
    tm_path = f"res/items/data/{tm.lower()}.json"
    try:
        with open(tm_path) as f:
            tm_data = json.load(f)
        move = tm_data.get("teachesMove", "")
    except FileNotFoundError:
        move = ""
    move_name = move.removeprefix("MOVE_").lower()
    move_path = f"res/moves/{move_name}/data.json"
    try:
        with open(move_path) as f:
            move_data = json.load(f)
        cls = move_data.get("class", "")
        power = move_data.get("power", 0)
        accuracy = move_data.get("accuracy", 0)
        pp = move_data.get("pp", 0)
        effect = move_data.get("effect", {})
        effect_type = effect.get("type", "") if isinstance(effect, dict) else ""
    except FileNotFoundError:
        cls = power = accuracy = pp = effect_type = ""
    print(f"{tm:<8} {move:<30} {cls:<20} {power:<8} {accuracy:<10} {pp:<6} {effect_type}")
