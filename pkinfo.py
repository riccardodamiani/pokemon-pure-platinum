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
for level, move in data["learnset"]["by_level"]:
    print(f"Lv {level:3}: {move}")

print("\n=== LEARNSET BY TM ===")
for tm in data["learnset"]["by_tm"]:
    tm_path = f"res/items/data/{tm.lower()}.json"
    try:
        with open(tm_path) as f:
            tm_data = json.load(f)
        move = tm_data.get("teachesMove", "")
    except FileNotFoundError:
        move = ""
    print(f"  {tm:<6}  {move}")
