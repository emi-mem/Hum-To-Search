from pathlib import Path
import sounddevice as sd
import wavio
from datetime import datetime

# --- Paths (works no matter where you run from) ---
BASE_DIR = Path(__file__).resolve().parent.parent   # project root
RECORDINGS_DIR = BASE_DIR / "data" / "recordings"
RECORDINGS_DIR.mkdir(parents=True, exist_ok=True)

# --- Settings ---
duration = 5        # seconds
sample_rate = 44100 # Hz
channels = 1        # mono

# --- Filename ---
filename = f"hum_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
file_path = RECORDINGS_DIR / filename

print("Recording will start in 5 seconds. Get ready!")
sd.sleep(2000)
print("Recording starts in 3...")
sd.sleep(1000)
print("Recording starts in 2...")
sd.sleep(1000)
print("Recording starts in 1...")
sd.sleep(1000)

print("Recording...")
recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=channels)
sd.wait()
print(f"Recording finished! Saving to {file_path}")

# Save as WAV (16-bit)
wavio.write(str(file_path), recording, sample_rate, sampwidth=2)
print("Done.")