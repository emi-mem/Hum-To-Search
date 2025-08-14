from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent.parent
SONGS_DIR = BASE_DIR / "data" / "songs"

if not SONGS_DIR.exists():
    print("No songs directory yet.")
    raise SystemExit()

metas = sorted(SONGS_DIR.glob("*.json"))
if not metas:
    print("No song metadata files found. Add entries first.")
    raise SystemExit()

for j in metas:
    with open(j) as f:
        meta = json.load(f)
    print(f"- {meta.get('title')} [{meta.get('source')}] -> {meta.get('rel_file')}")

