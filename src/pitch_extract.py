from pathlib import Path
import os
import numpy as np
import librosa

# --- Paths ---
BASE_DIR = Path(__file__).resolve().parent.parent   # project root
RECORDINGS_DIR = BASE_DIR / "data" / "recordings"
RECORDINGS_DIR.mkdir(parents=True, exist_ok=True)

# --- Find latest WAV recording ---
wav_files = sorted(RECORDINGS_DIR.glob("*.wav"), key=lambda p: p.stat().st_mtime)
if not wav_files:
    raise FileNotFoundError(f"No .wav files found in {RECORDINGS_DIR}. "
                            f"Run record.py first.")
latest_file = wav_files[-1]
print(f"Loading {latest_file} ...")

# --- Load audio ---
y, sr = librosa.load(str(latest_file), sr=44100)

# --- Extract F0 with PYIN ---
f0, voiced_flag, voiced_probs = librosa.pyin(
    y,
    fmin=librosa.note_to_hz('C2'),
    fmax=librosa.note_to_hz('C7'),
)

# --- Keep only voiced frames ---
f0 = np.asarray(f0)
voiced_flag = np.asarray(voiced_flag, dtype=bool)
f0_clean = np.where(voiced_flag, f0, np.nan)
f0_no_nans = f0_clean[~np.isnan(f0_clean)]

# --- Save pitch sequence next to the WAV ---
out_path = latest_file.with_name(latest_file.stem + "_pitches.npy")
np.save(out_path, f0_no_nans)
print(f"Extracted {len(f0_no_nans)} pitch values.")
print(f"Pitch data saved to {out_path}")
