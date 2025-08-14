from pathlib import Path
import json
import re
import hashlib
import numpy as np
import mido
import librosa

BASE_DIR = Path(__file__).resolve().parent.parent
SONGS_DIR = BASE_DIR / "data" / "songs"
SONGS_DIR.mkdir(parents=True, exist_ok=True)

def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.strip().lower()).strip("-")

def midi_to_melody_midinotes(midi_path: Path) -> np.ndarray:
    """
    Very simple heuristic: collect note_on events with velocity > 0
    from the longest track (often melody-like).
    """
    mid = mido.MidiFile(str(midi_path))
    track = max(mid.tracks, key=lambda t: len(t))
    notes = []
    for msg in track:
        if msg.type == "note_on" and msg.velocity > 0:
            notes.append(msg.note)  # MIDI note number (int)
    return np.array(notes, dtype=np.float32)

def normalize_key_from_midi_notes(midi_notes: np.ndarray) -> np.ndarray:
    # center by median to remove key (semitone offsets)
    center = np.median(midi_notes)
    rel = midi_notes - center
    return rel.astype(np.float32)

def melody_fingerprint(arr: np.ndarray) -> str:
    """Stable content fingerprint (sha1) for duplicate detection."""
    h = hashlib.sha1()
    # include length for extra stability
    h.update(str(len(arr)).encode("utf-8"))
    h.update(arr.tobytes())
    return h.hexdigest()

def load_existing_fingerprints():
    fps = {}
    for meta_path in SONGS_DIR.glob("*.json"):
        try:
            with open(meta_path) as f:
                meta = json.load(f)
            if "fingerprint" in meta:
                fps[meta["slug"]] = meta["fingerprint"]
        except Exception:
            pass
    return fps

if __name__ == "__main__":
    # --- Input path (strip quotes, expand ~) ---
    midi_input = input("Path to MIDI file: ").strip().strip('"').strip("'")
    midi_path = Path(midi_input).expanduser()
    if not midi_path.exists():
        raise SystemExit(f"MIDI not found: {midi_path}")

    # --- Title/slug ---
    title = input("Song title: ").strip()
    if not title:
        raise SystemExit("No title provided.")
    slug = slugify(title)

    # --- Extract melody ---
    midi_notes = midi_to_melody_midinotes(midi_path)
    if len(midi_notes) == 0:
        raise SystemExit("No notes found—try a different MIDI file.")
    rel = normalize_key_from_midi_notes(midi_notes)
    hz = librosa.midi_to_hz(midi_notes)

    # --- Compute fingerprint for duplicate-by-content check ---
    fp = melody_fingerprint(midi_notes)

    # --- Duplicate checks ---
    meta_path = SONGS_DIR / f"{slug}.json"
    rel_path  = SONGS_DIR / f"{slug}_rel.npy"
    hz_path   = SONGS_DIR / f"{slug}_hz.npy"
    seq_path  = SONGS_DIR / f"{slug}_midi_seq.npy"

    # 1) Same slug (title duplicate)
    if meta_path.exists() or rel_path.exists() or hz_path.exists() or seq_path.exists():
        resp = input(f"⚠️  An entry named '{slug}' already exists. Overwrite? (y/N): ").strip().lower()
        if resp != "y":
            raise SystemExit("Canceled. (Tip: use a different title if you want a separate entry.)")

    # 2) Same content (fingerprint duplicate) under any slug
    existing_fps = load_existing_fingerprints()
    dup_slugs = [s for s, existing_fp in existing_fps.items() if existing_fp == fp and s != slug]
    if dup_slugs:
        resp = input(f"⚠️  This melody matches existing entry/entries {dup_slugs}. Add anyway? (y/N): ").strip().lower()
        if resp != "y":
            raise SystemExit("Canceled to avoid duplicate content.")

    # --- Save files ---
    np.save(seq_path, midi_notes)
    np.save(rel_path, rel)
    np.save(hz_path, hz.astype(np.float32))

    meta = {
        "title": title,
        "slug": slug,
        "source": "midi",
        "midi_file": midi_path.name,
        "midi_seq_file": seq_path.name,
        "rel_file": rel_path.name,
        "hz_file": hz_path.name,
        "fingerprint": fp,  # NEW: used for content-duplicate detection
        "notes": "Key-normalized semitone offsets from MIDI note numbers.",
    }
    with open(meta_path, "w") as f:
        json.dump(meta, f, indent=2)

    print(f"✅ Added MIDI-based entry for {title} -> data/songs/ (slug: {slug})")
