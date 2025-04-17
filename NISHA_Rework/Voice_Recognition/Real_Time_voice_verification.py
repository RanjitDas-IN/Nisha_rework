import os
import sys
import torch
import torchaudio
import numpy as np
import sounddevice as sd
import scipy.io.wavfile as wavfile
from sklearn.metrics.pairwise import cosine_similarity
from speechbrain.inference import EncoderClassifier
from time import perf_counter
import random
#──────────────────────────────────── Timer start
t0 = perf_counter()


# ──────────────────────────────────── Defining Path ───────────────────────────────────────────
#  1) Figure out the path to your project root (one level up from this file)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
#  2) Add it to sys.path so Python can find your SPEAK package
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
# ─────────────────────────────────── Model_Speak ────────────────────────────────────────────

from SPEAK.Mouth import *

def model_speak(text):
    print("Working...")
    speak_text(text)
def type_print(text, delay=0.0999):
    import time
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print() 
# ───────────────────────────────────────────────────────────────────────────────────────────────────────── 
 
nisha_lines = [
    "Yehh Boss Ranjit, it's you!",
    "Confirmed, Boss. Welcome back!",
    "Welcome back, boss! Ready for action?",
    "Voice verified! What are we doing today?",
    "Boss Ranjit entered the arena!",
    "Mission start! Ranjit detected!",
    "Hey! It's you, Ranjit. Let's roll!",
    "Nisha here: Authentication successful, Boss!"
]


# Device setup
device = torch.device("cpu")

# Preload model
model = EncoderClassifier.from_hparams(
    source="speechbrain/spkrec-ecapa-voxceleb",
    run_opts={"device": device},
    savedir="pretrained_model_cache"
).to(device).eval()

# Pre-create common resamplers
resampler_48k = torchaudio.transforms.Resample(48000, 16000)
resampler_44k = torchaudio.transforms.Resample(44100, 16000)
resampler_others = lambda fs: torchaudio.transforms.Resample(fs, 16000)

# Preload profile once
profile = np.load("NISHA_Rework/Voice_Recognition/ranjit_profile.npy")

# Embedding extractor from signal directly
def get_embedding_from_tensor(signal, fs):
    if signal.shape[0] > 1:
        signal = signal.mean(dim=0, keepdim=True)

    if fs == 48000:
        signal = resampler_48k(signal)
    elif fs == 44100:
        signal = resampler_44k(signal)
    elif fs != 16000:
        signal = resampler_others(fs)(signal)

    with torch.inference_mode():
        emb = model.encode_batch(signal.to(device)).squeeze()
    return emb.cpu().numpy()

# Matching logic
def is_match_from_signal(signal, fs, threshold=0.25):
    emb = get_embedding_from_tensor(signal, fs)
    score = cosine_similarity(emb.reshape(1, -1), profile.reshape(1, -1))[0][0]
    return score >= threshold, score

# Record from mic into RAM
def record_voice(duration=5, sample_rate=16000):
    print(f"Recording {duration} seconds voice...")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()
    print("Recording completed.")

    # Convert to torch tensor format
    recording = recording.squeeze()  # remove channel dim
    recording = torch.from_numpy(recording).float().unsqueeze(0) / 32768.0  # normalize int16 to float32
    return recording, sample_rate

# Main execution
if __name__ == "__main__":
    signal, fs = record_voice(duration=5)

    print("Verifying voice, please wait...")
    match, similarity = is_match_from_signal(signal, fs)

    print(f" Match: {match}, Accuracy: {similarity:.4f}")

    if match:
        print("Access Granted!")
        x=random.choice(nisha_lines)
        model_speak(x)
        type_print(x)

    else:
        print("Access Denied.")

    print(f"Done in {perf_counter() - t0:.2f} sec")