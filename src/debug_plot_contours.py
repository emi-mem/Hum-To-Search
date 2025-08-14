from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parent.parent
SONGS = BASE / "data" / "songs"

def load_rel(slug): 
    p = SONGS / f"{slug}_rel.npy"
    if not p.exists():
        raise SystemExit(f"Missing: {p}")
    return np.load(p)

def resample(x, L=128):
    t1 = np.linspace(0,1,len(x)); t2 = np.linspace(0,1,L)
    return np.interp(t2, t1, x)

if __name__ == "__main__":
    a = input("Slug A (e.g. say-my-name): ").strip()
    b = input("Slug B (e.g. through-the-wire): ").strip()
    A = load_rel(a); B = load_rel(b)
    A2, B2 = resample(A), resample(B)

    plt.figure(figsize=(10,4))
    plt.plot(A2, label=a)
    plt.plot(B2, label=b, alpha=0.8)
    plt.legend()
    plt.title("Key-normalized contours (resampled)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

