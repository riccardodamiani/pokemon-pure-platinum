#!/usr/bin/env python3

import json
import mimetypes
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

WIKI_DIR              = Path(__file__).parent
CHANGES_FILE          = WIKI_DIR / "changes.json"
POKEMON_DIR           = (WIKI_DIR / ".." / "res" / "pokemon").resolve()
MOVES_DIR             = (WIKI_DIR / ".." / "res" / "moves").resolve()
ITEMS_DIR             = (WIKI_DIR / ".." / "res" / "items" / "data").resolve()
ITEMS_ICONS_DIR       = (WIKI_DIR / ".." / "res" / "items" / "icons").resolve()
TRAINERS_DATA_DIR     = (WIKI_DIR / ".." / "res" / "trainers" / "data").resolve()
TRAINERS_CLASSES_DIR  = (WIKI_DIR / ".." / "res" / "trainers" / "classes").resolve()
PORT                  = 5000

_SKIP_MOVES = {"none"}


def _move_info(move_const: str) -> "dict | None":
    """Return {name, type, class, power, accuracy} for a MOVE_XXX constant."""
    folder = move_const.removeprefix("MOVE_").lower()
    path   = MOVES_DIR / folder / "data.json"
    if not path.exists():
        return None
    d = json.loads(path.read_text(encoding="utf-8"))
    return {
        "slug":     folder,
        "name":     d.get("name"),
        "type":     d.get("type"),
        "class":    d.get("class"),
        "power":    d.get("power"),
        "accuracy": d.get("accuracy"),
    }


def _resolve_learnset(learnset: dict) -> dict:
    by_level = []
    for entry in learnset.get("by_level", []):
        level, move_const = entry[0], entry[1]
        info = _move_info(move_const)
        if info:
            by_level.append({"level": level, **info})

    by_tm = []
    for tm in learnset.get("by_tm", []):
        item_path = ITEMS_DIR / f"{tm.lower()}.json"
        if not item_path.exists():
            continue
        item = json.loads(item_path.read_text(encoding="utf-8"))
        move_const = item.get("teachesMove", "")
        if not move_const:
            continue
        info = _move_info(move_const)
        if info:
            by_tm.append({"tm": tm, **info})

    by_tutor = []
    for move_const in learnset.get("by_tutor", []):
        info = _move_info(move_const)
        if info:
            by_tutor.append(info)

    egg_moves = []
    for move_const in learnset.get("egg_moves", []):
        info = _move_info(move_const)
        if info:
            egg_moves.append(info)

    return {
        "by_level":  by_level,
        "by_tm":     by_tm,
        "by_tutor":  by_tutor,
        "egg_moves": egg_moves,
    }

_SKIP = {"bad_egg", "egg", "none"}
_SKIP_TRAINERS = {"none"}


def _trainer_class_folder(class_const: str) -> str:
    return class_const.removeprefix("TRAINER_CLASS_").lower()


class WikiHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path
        if   path == "/":                        self._serve_file("index.html")
        elif path == "/changes":                 self._serve_file("changes.html")
        elif path == "/pokemon":                 self._serve_file("pokemon.html")
        elif path == "/moves":                   self._serve_file("moves.html")
        elif path == "/items":                   self._serve_file("items.html")
        elif path == "/trainers":                self._serve_file("trainers.html")
        elif path == "/api/changes":             self._api_changes()
        elif path == "/api/pokemon":             self._api_pokemon_list()
        elif path.startswith("/api/pokemon/"):   self._api_pokemon_detail(path[13:])
        elif path == "/api/moves":               self._api_moves_list()
        elif path.startswith("/api/moves/"):     self._api_moves_detail(path[11:])
        elif path == "/api/items":               self._api_items_list()
        elif path.startswith("/api/items/"):     self._api_items_detail(path[11:])
        elif path == "/api/trainers":            self._api_trainers_list()
        elif path.startswith("/api/trainers/"):  self._api_trainers_detail(path[14:])
        elif path.startswith("/trainer-icon/"):  self._trainer_icon(path[14:])
        elif path.startswith("/item-icon/"):     self._item_icon(path[11:])
        elif path.startswith("/sprites/"):
            parts = path[9:].split("/", 1)
            self._sprite(parts[0], parts[1]) if len(parts) == 2 else self._err(400)
        else:
            self._err(404)

    # ── helpers ──────────────────────────────────────────────────────────────

    def _safe(self, name: str) -> bool:
        return ".." not in name and "/" not in name and "\\" not in name

    def _send(self, status: int, content_type: str, body: bytes):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _err(self, code: int):
        msg = str(code).encode()
        self._send(code, "text/plain", msg)

    def _json(self, data):
        self._send(200, "application/json", json.dumps(data).encode())

    def _serve_file(self, name: str):
        p = WIKI_DIR / name
        if not p.exists():
            return self._err(404)
        mime = mimetypes.guess_type(str(p))[0] or "application/octet-stream"
        self._send(200, mime, p.read_bytes())

    # ── routes ────────────────────────────────────────────────────────────────

    def _api_changes(self):
        if not CHANGES_FILE.exists():
            return self._err(404)
        self._json(json.loads(CHANGES_FILE.read_text(encoding="utf-8")))

    def _api_pokemon_list(self):
        result = []
        for folder in sorted(POKEMON_DIR.iterdir()):
            if not folder.is_dir() or folder.name in _SKIP:
                continue
            data_file = folder / "data.json"
            if not data_file.exists():
                continue
            d = json.loads(data_file.read_text(encoding="utf-8"))
            result.append({
                "name":       folder.name,
                "types":      d.get("types", []),
                "base_stats": d.get("base_stats", {}),
                "has_female": (folder / "female_front.png").exists(),
            })
        self._json(result)

    def _api_pokemon_detail(self, name: str):
        if not self._safe(name):
            return self._err(400)
        folder    = POKEMON_DIR / name
        data_file = folder / "data.json"
        if not data_file.exists():
            return self._err(404)
        d = json.loads(data_file.read_text(encoding="utf-8"))
        d["has_female"]        = (folder / "female_front.png").exists()
        d["learnset_resolved"] = _resolve_learnset(d.get("learnset", {}))
        self._json(d)

    def _sprite(self, name: str, gender: str):
        if not self._safe(name) or gender not in ("male", "female"):
            return self._err(400)
        path = POKEMON_DIR / name / f"{gender}_front.png"
        if not path.exists():
            return self._err(404)
        self._send(200, "image/png", path.read_bytes())

    def _api_moves_list(self):
        result = []
        for folder in sorted(MOVES_DIR.iterdir()):
            if not folder.is_dir() or folder.name in _SKIP_MOVES:
                continue
            data_file = folder / "data.json"
            if not data_file.exists():
                continue
            d = json.loads(data_file.read_text(encoding="utf-8"))
            result.append({
                "name":    folder.name,
                "display": d.get("name", folder.name),
                "type":    d.get("type"),
                "class":   d.get("class"),
                "power":   d.get("power"),
                "accuracy":d.get("accuracy"),
                "pp":      d.get("pp"),
                "description": "".join(d.get("description", [])).replace("\n", " ").strip(),
            })
        self._json(result)

    def _api_moves_detail(self, name: str):
        if not self._safe(name):
            return self._err(400)
        data_file = MOVES_DIR / name / "data.json"
        if not data_file.exists():
            return self._err(404)
        d = json.loads(data_file.read_text(encoding="utf-8"))
        self._json(d)

    def _api_items_list(self):
        result = []
        for item_file in sorted(ITEMS_DIR.glob("*.json")):
            slug = item_file.stem
            d = json.loads(item_file.read_text(encoding="utf-8"))
            result.append({
                "slug":        slug,
                "name":        d.get("name", slug),
                "description": "".join(d.get("description", [])).replace("\n", " ").strip(),
                "pocket":      d.get("fieldPocket"),
                "price":       d.get("price"),
                "has_icon":    (ITEMS_ICONS_DIR / f"{slug}.png").exists(),
            })
        self._json(result)

    def _api_items_detail(self, slug: str):
        if not self._safe(slug):
            return self._err(400)
        item_file = ITEMS_DIR / f"{slug}.json"
        if not item_file.exists():
            return self._err(404)
        d = json.loads(item_file.read_text(encoding="utf-8"))
        d["slug"]     = slug
        d["has_icon"] = (ITEMS_ICONS_DIR / f"{slug}.png").exists()
        self._json(d)

    def _item_icon(self, slug: str):
        if not self._safe(slug):
            return self._err(400)
        path = ITEMS_ICONS_DIR / f"{slug}.png"
        if not path.exists():
            path = ITEMS_ICONS_DIR / "none.png"
        if not path.exists():
            return self._err(404)
        self._send(200, "image/png", path.read_bytes())

    def _api_trainers_list(self):
        result = []
        for item_file in sorted(TRAINERS_DATA_DIR.glob("*.json")):
            slug = item_file.stem
            if slug in _SKIP_TRAINERS or slug.startswith("dummy_"):
                continue
            d = json.loads(item_file.read_text(encoding="utf-8"))
            class_const = d.get("class", "")
            class_folder = _trainer_class_folder(class_const)
            result.append({
                "slug":         slug,
                "name":         d.get("name", slug),
                "class":        class_const,
                "class_folder": class_folder,
                "has_icon":     (TRAINERS_CLASSES_DIR / class_folder / "front.png").exists(),
            })
        self._json(result)

    def _api_trainers_detail(self, slug: str):
        if not self._safe(slug):
            return self._err(400)
        item_file = TRAINERS_DATA_DIR / f"{slug}.json"
        if not item_file.exists():
            return self._err(404)
        d = json.loads(item_file.read_text(encoding="utf-8"))
        class_const  = d.get("class", "")
        class_folder = _trainer_class_folder(class_const)
        d["slug"]       = slug
        d["class_folder"] = class_folder
        d["has_icon"]   = (TRAINERS_CLASSES_DIR / class_folder / "front.png").exists()
        self._json(d)

    def _trainer_icon(self, class_folder: str):
        if not self._safe(class_folder):
            return self._err(400)
        path = TRAINERS_CLASSES_DIR / class_folder / "front.png"
        if not path.exists():
            return self._err(404)
        self._send(200, "image/png", path.read_bytes())

    def log_message(self, *_):  # suppress per-request stdout noise
        pass


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Pokemon Pure Platinum wiki server")
    parser.add_argument("-p", "--port", type=int, default=PORT, help="Port to listen on (default: %(default)s)")
    args = parser.parse_args()

    print(f"Usage: wiki.py [-p PORT]")
    print(f"  -p, --port  Port to listen on (default: {PORT})")
    print()
    server = HTTPServer(("localhost", args.port), WikiHandler)
    print(f"Wiki running at http://localhost:{args.port}  (Ctrl-C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
