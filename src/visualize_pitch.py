from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import librosa  # NEW

# --- Paths ---
BASE_DIR = Path(__file__).resolve().parent.parent   # project root
RECORDINGS_DIR = BASE_DIR / "data" / "recordings"
RECORDINGS_DIR.mkdir(parents=True, exist_ok=True)

# --- Find latest pitch file ---
pitch_files = sorted(RECORDINGS_DIR.glob("*_pitches.npy"), key=lambda p: p.stat().st_mtime)
if not pitch_files:
    raise FileNotFoundError(f"No *_pitches.npy files found in {RECORDINGS_DIR}. Run pitch_extract.py first.")
latest_pitch = pitch_files[-1]
print(f"Loading pitch data from {latest_pitch} ...")
pitches_hz = np.load(latest_pitch)  # these are in Hz

# --- Convert to MIDI (semitones). This gives nicer, note-based ticks ---
midi_vals = librosa.hz_to_midi(pitches_hz)

# --- Build a clean time axis (frame index is fine here) ---
time = np.arange(len(midi_vals))

# --- Choose tick marks at each semitone in the observed range (or every 2 to reduce clutter) ---
mmin = int(np.floor(np.nanmin(midi_vals)))
mmax = int(np.ceil(np.nanmax(midi_vals)))
tick_midis = np.arange(mmin, mmax + 1, 1)  # use step=2 if labels overlap
tick_labels = librosa.midi_to_note(tick_midis, octave=True)

# --- Plot in MIDI, label with note names ---
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(time, midi_vals, marker='o', markersize=2, linestyle='-')
ax.set_xlabel("Frame index")
ax.set_ylabel("Pitch (note)")
ax.set_title("Extracted Melody from Recording")
ax.set_yticks(tick_midis)
ax.set_yticklabels(tick_labels)
ax.grid(True)

# A right-side secondary axis showing Hz for reference
def m2h(m): return librosa.midi_to_hz(m)
def h2m(h): return librosa.hz_to_midi(h)
ax.secondary_yaxis('right', functions=(m2h, h2m)).set_ylabel("Hz")

plt.tight_layout()
plt.show()
