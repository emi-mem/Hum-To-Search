from pathlib import Path
import json, hashlib
import numpy as np

BASE = Path(__file__).resolve().parent.parent
SONGS = BASE / "data" / "songs"

def fp_of_array(arr: np.ndarray) -> str:
    h = hashlib.sha1()
    h.update(str(len(arr)).encode("utf-8"))
    h.update(arr.tobytes())
    return h.hexdigest()

def backfill():
    metas = sorted(SONGS.glob("*.json"))
    if not metas:
        print("No song metadata found.")
        return
    updated = 0
    for mp in metas:
        with open(mp) as f:
            meta = json.load(f)
        if meta.get("fingerprint"):
            continue

        # Prefer raw MIDI sequence if present; else use rel contour
        seq_path = SONGS / meta.get("midi_seq_file", "")
        rel_path = SONGS / meta.get("rel_file", "")

        arr = None
        if seq_path.exists():
            arr = np.load(seq_path)
        elif rel_path.exists():
            arr = np.load(rel_path)
        else:
            print(f"⚠️  Missing arrays for {mp.name}; skip.")
            continue

        meta["fingerprint"] = fp_of_array(arr)
        with open(mp, "w") as f:
            json.dump(meta, f, indent=2)
        updated += 1
        print(f"Updated fingerprint: {meta.get('slug')}")

    print(f"\nDone. Updated {updated} entries.")

if __name__ == "__main__":
    backfill()

