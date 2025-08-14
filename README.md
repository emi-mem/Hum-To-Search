# 🎵 Hum-To-Search

> **Hum or sing a melody** → instantly match it against your local database of songs.  
A Python-powered, offline mini-Shazam built as a learning and portfolio project.

---

## ✨ Features

- 🎙 **Record audio** from your mic  
- 🎼 **Extract pitch** using `librosa.pyin`  
- 🔑 **Key-invariant** melody contour matching  
- 🖼 **Visualize melodies** with note names  
- 📂 **Build a song DB** from MIDI files (single or bulk import)  
- 🔍 **Search & match** with Dynamic Time Warping (tempo-normalized)  
- 🛠 **Fully local** — no servers, no APIs

---
## 🚀 Quick Start

### 1️⃣ Install

```bash
# optional: create a virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt
```
---

### 2️⃣ Record a hum

```bash
python src/record.py
```
🎤 Records ~10 seconds and saves a timestamped WAV in data/recordings/.

---

### 3️⃣ Extract & visualize (optional)

```bash
python src/pitch_extract.py
python src/visualize_pitch.py
```
📈 See your melody curve in Hz or as note names.

---

### 4️⃣ Add songs to your DB (from MIDI)

```bash
python src/add_song_from_midi.py
# Path to MIDI: /path/to/song.mid
# Song title: My Song
```
Folder of MIDIs:
```bash
python src/add_midis_from_folder.py
# Path to folder: /path/to/midis
```
List DB songs: 
```bash
python src/list_songs.py
```
---

5️⃣ Match your hum
```bash
python src/match.py
```

💡 Output looks like:
```markdown
=== Matches ===
1. Say My Name  (DTW: 0.4519)
2. Through The Wire  (DTW: 0.5237)
3. ...
```
❗❗❗ Lower DTW = more similar  ❗❗❗
❗❗❗ Ranked from TOP to BOTTOM ❗❗❗

---

🛠 How It Works (in 20 seconds)
Record audio → detect pitch (Hz) with librosa.pyin
Convert Hz → MIDI note numbers → subtract median (key-invariant)
Resample contours to fixed length (tempo normalization)
Compare with Dynamic Time Warping → smallest distance wins

---

📦 Requirements
From requirements.txt:
```nginx
librosa
numpy
sounddevice
wavio
mido
matplotlib
```

---

📌 Tips for Best Results
Hum 5–10s of the main hook 🎶
Quiet room = cleaner pitch detection
Use good MIDIs (main melody track)
Crop stored melody to the hook when possible
If distances are close, consider the top-3 results

---

⚠ Limitations
Not Shazam — this is a small-scale matcher for learning/demo
MIDI quality heavily affects results
Similar-shaped hooks can still confuse DTW

---

🗺 Roadmap
🎯 Auto-detect melody track from MIDI
✂ Visual/interactive hook cropping
🪄 Partial matching for short hums
🌐 Optional web UI for easier use

---

❓ FAQ
Q: Do I need internet?
A: Nope. 100% local.
Q: Can I use popular songs?
A: Yes — add them via MIDI files. Only the melody fingerprint is stored.
Q: Why did two songs swap places in ranking?
A: Usually the MIDI didn’t capture the exact vocal hook, or the shapes are very similar.

🎶 Hum it. Match it. Own it. 🎶
