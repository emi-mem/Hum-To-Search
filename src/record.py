import sounddevice as sd
import wavio
import os
from datetime import datetime

# Settings
duration = 5  # seconds
sample_rate = 44100  # Hz
channels = 1  # mono

# Create recordings folder if it doesn't exist
recordings_path = "../data/recordings"
os.makedirs(recordings_path, exist_ok=True)

# Filename with timestamp
filename = f"hum_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
file_path = os.path.join(recordings_path, filename)

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
sd.wait()  # Wait until recording is finished
print(f"Recording finished! Saved as {file_path}")

# Save as WAV
wavio.write(file_path, recording, sample_rate, sampwidth=2)

