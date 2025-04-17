import torch
import torchaudio
import numpy as np
import os,sys
import sounddevice as sd
import random
from scipy.spatial.distance import cosine
from speechbrain.inference import EncoderClassifier
from time import perf_counter
import subprocess

#────────────────────────── Timer start ────────────────────────────────────────────────────
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
 
# Device
device = torch.device("cpu")

#────────────────────────── Load model ────────────────────────────────────────────────────
model = EncoderClassifier.from_hparams(
    source="speechbrain/spkrec-ecapa-voxceleb",
    run_opts={"device": device},
    savedir="pretrained_model_cache"
).to(device).eval()

# Quantize embedding part
model.mods.embedding_model = torch.quantization.quantize_dynamic(
    model.mods.embedding_model,
    {torch.nn.Linear},
    dtype=torch.qint8
)

#────────────────────────── Resamplers ────────────────────────────────────────────────────
resampler_48k = torchaudio.transforms.Resample(orig_freq=48000, new_freq=16000)
resampler_44k = torchaudio.transforms.Resample(orig_freq=44100, new_freq=16000)
resampler_others = lambda fs: torchaudio.transforms.Resample(orig_freq=fs, new_freq=16000)

# Get embedding directly from tensor
def get_embedding_from_signal(signal, fs):
    # Mono
    if signal.shape[0] > 1:
        signal = torch.mean(signal, dim=0, keepdim=True)

    # Resample
    if fs == 48000:
        signal = resampler_48k(signal)
    elif fs == 44100:
        signal = resampler_44k(signal)
    elif fs != 16000:
        signal = resampler_others(fs)(signal)

    with torch.no_grad():
        emb = model.encode_batch(signal.to(device)).squeeze()
    return emb.cpu().numpy()

#────────────────────────────────── Compare embeddings ────────────────────────────────────────────────────────────
def is_match_from_signal(signal, fs, profile_path="NISHA_Rework/Voice_Recognition/ranjit_profile.npy", threshold=0.25):
    profile_emb = np.load(profile_path)
    test_emb = get_embedding_from_signal(signal, fs)
    score = 1 - cosine(test_emb, profile_emb)
    return score >= threshold, score

#────────────────────────── Record from mic ──────────────────────────────────────────────────────────────────────────────
def record_voice(duration=3, sample_rate=16000):
    print(f"Nisha: 'Recording your voice for {duration} seconds...'")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()
    print("Nisha: 'Recording complete.'")

    # Convert to tensor and normalize
    recording = recording.squeeze()  # (samples,)
    recording = torch.from_numpy(recording).float().unsqueeze(0) / 32768.0  # normalize int16 to float32
    return recording, sample_rate

#────────────────────────────── Nisha Lines ─────────────────────────────────────────────────────────────────────
# Nisha random lines
nisha_lines = [
    "Yehh Boss Ranjit, it's you!",
    "Confirmed as Boss. Welcome back Ranjit!",
    "Welcome back, boss! Ready for action?",
    "Voice verified! What are we doing today?",
    "Boss Ranjit entered the arena!",
    "Mission start! Ranjit detected!",
    "Hey! It's you, Ranjit. Let's roll!",
    "Nisha here: Authentication successful, Boss!"
]
#───────────────────────────────────── Main ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    signal, fs = record_voice(duration=3)

    print("Nisha: 'Verifying your voice...'")
    match, similarity = is_match_from_signal(signal, fs)

    if match:
        print(f"Nisha: 'Access Granted! Accuracy: {similarity:.4f}'")
        x=random.choice(nisha_lines)
        model_speak(x)
        type_print(x)

        
    else:
        print(f"Nisha: 'Access Denied! Accuracy: {similarity:.4f}'")
#───────────────────────────────────── End Timer ──────────────────────────────────────────────────────────────

    print(f"Done in {perf_counter() - t0:.2f} sec")