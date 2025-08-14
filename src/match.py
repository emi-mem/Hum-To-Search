from pathlib import Path
import json
import numpy as np
import librosa

BASE_DIR = Path(__file__).resolve().parent.parent
RECORDINGS_DIR = BASE_DIR / "data" / "recordings"
SONGS_DIR = BASE_DIR / "data" / "songs"

def load_latest_wav():
    wavs = sorted(RECORDINGS_DIR.glob("*.wav"), key=lambda p: p.stat().st_mtime)
    if not wavs:
        raise FileNotFoundError("No .wav files found. Record something first!")
    return str(wavs[-1])

def extract_rel_from_wav(wav_path, sr=44100):
    y, _ = librosa.load(wav_path, sr=sr)
    f0, vflag, _ = librosa.pyin(
        y,
        fmin=librosa.note_to_hz("C2"),
        fmax=librosa.note_to_hz("C7")
    )
    f0 = np.asarray(f0)
    vflag = np.asarray(vflag, dtype=bool)
    f0 = np.where(vflag, f0, np.nan)
    f0 = f0[~np.isnan(f0)]
    midi = librosa.hz_to_midi(f0)
    center = np.median(midi)
    return midi - center  # key-invariant

def load_db():
    entries = []
    for meta_path in SONGS_DIR.glob("*.json"):
        with open(meta_path) as f:
            meta = json.load(f)
        rel_file = SONGS_DIR / meta["rel_file"]
        if rel_file.exists():
            rel = np.load(rel_file)
            entries.append({"title": meta["title"], "slug": meta["slug"], "rel": rel})
    if not entries:
        raise FileNotFoundError("No songs in the database.")
    return entries

def resample_len(x, length):
    idx_src = np.linspace(0, 1, num=len(x))
    idx_tgt = np.linspace(0, 1, num=length)
    return np.interp(idx_tgt, idx_src, x).astype(np.float32)

def zscore(x):
    mu = np.mean(x)
    sd = np.std(x) + 1e-8
    return (x - mu) / sd

def dtw_distance(a, b):
    A, B = a[:, None], b[:, None]
    D, wp = librosa.sequence.dtw(X=A.T, Y=B.T, metric="euclidean")
    return D[-1, -1] / max(1, len(wp))

def run_match(top_k=5, length=128):
    wav = load_latest_wav()
    print(f"Using recording: {wav}")
    q_rel = extract_rel_from_wav(wav)
    q_rel = resample_len(q_rel, length)
    q_rel = zscore(q_rel)

    entries = load_db()
    results = []
    for e in entries:
        s_rel = resample_len(e["rel"], length)
        s_rel = zscore(s_rel)
        dist = dtw_distance(q_rel, s_rel)
        results.append({"title": e["title"], "distance": dist})

    results.sort(key=lambda r: r["distance"])
    return results[:top_k]

if __name__ == "__main__":
    matches = run_match()
    print("\n=== Matches ===")
    for i, m in enumerate(matches, 1):
        print(f"{i}. {m['title']}  (DTW distance: {m['distance']:.4f})")
