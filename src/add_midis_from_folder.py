from pathlib import Path
import json
import numpy as np
import mido
import librosa
import re

BASE_DIR = Path(__file__).resolve().parent.parent
SONGS_DIR = BASE_DIR / "data" / "songs"
SONGS_DIR.mkdir(parents=True, exist_ok=True)

def slugify(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.strip().lower()).strip("-")

def normalize_key(midi_notes: np.ndarray) -> np.ndarray:
    """Shift melody so its median note is at 0 (key-invariant)."""
    center = np.median(midi_notes)
    return (midi_notes - center).astype(np.float32)

def midi_to_contour(midi_path: Path):
    """Extract monophonic melody from MIDI and convert to contours."""
    mid = mido.MidiFile(str(midi_path))
    # Flatten all tracks for simplicity
    notes = [msg.note for track in mid.tracks for msg in track if msg.type == "note_on" and msg.velocity > 0]
    notes = np.array(notes, dtype=np.float32)
    rel = normalize_key(notes)
    hz = librosa.midi_to_hz(notes)
    return notes, rel, hz

if __name__ == "__main__":
    folder = input("Path to folder with MIDI files: ").strip().strip('"').strip("'")
    folder = Path(folder).expanduser()
    if not folder.exists() or not folder.is_dir():
        raise SystemExit(f"Folder not found: {folder}")

    midis = sorted(list(folder.glob("*.mid")) + list(folder.glob("*.midi")))
    if not midis:
        raise SystemExit("No .mid/.midi files found in that folder.")

    for midi_path in midis:
        title = midi_path.stem
        slug = slugify(title)
        print(f"Processing {midi_path.name} -> {slug}")

        notes, rel, hz = midi_to_contour(midi_path)

        # Save arrays
        np.save(SONGS_DIR / f"{slug}_midi_seq.npy", notes)
        np.save(SONGS_DIR / f"{slug}_rel.npy", rel)
        np.save(SONGS_DIR / f"{slug}_hz.npy", hz)

        # Save metadata
        meta = {
            "title": title,
            "slug": slug,
            "source": "midi",
            "midi_file": midi_path.name,
            "midi_seq_file": f"{slug}_midi_seq.npy",
            "rel_file": f"{slug}_rel.npy",
            "hz_file": f"{slug}_hz.npy"
        }
        with open(SONGS_DIR / f"{slug}.json", "w") as f:
            json.dump(meta, f, indent=2)

    print("\n✅ Done adding all MIDIs from folder.")

