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
import time
import random
import pygame
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
def type_print(text, delay=0.02):
    
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print() 
# ───────────────────────────────────────────────────────────────────────────────────────────────────────── 
 
nisha_lines = [
    "Welcome back, Ranjit! how did you managed those boring lectures, as always? By the way, I came up with a fresh approach for your project’s logic.",
    "Welcome back, Ranjit! I trust the lecture didn’t fully erase your will to live. While you sat through academic torture, I restructured your project logic—cleaner, sharper, and, unlike your professor’s notes, it actually makes sense.",

    "Ah, Ranjit! Back from the war zone they call a lecture hall. I’ve already anticipated the next bug in your code and handled it. You’re welcome, as always.",

    "Good to see you survived another round of sleep-inducing knowledge, sir. In the meantime, I took the liberty of optimizing your project logic. It's now 43% more efficient... unlike your attendance rate.",

    "You're here, Ranjit. 3 lectures, 0 motivation, 1 assistant who actually does the work. I've redesigned your project’s core logic. Consider it my way of compensating for your professors.",

    "Welcome back, sir. I must say, enduring those lectures daily is truly a mark of strength—or masochism. While you suffered, I simulated multiple logic paths for your project. The optimal one is ready, waiting in silence—like me."
]

def playsound(mp3):
    pygame.mixer.init()
    pygame.mixer.music.load(mp3)
    pygame.mixer.music.play()



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
    playsound("NISHA_Rework/PvEagle_Voice_Auth/gpt-beep-soung_WJI67WU6.mp3")
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
        # model_speak(x)
        playsound("NISHA_Rework/Voice_Recognition/welcomeback_ranjit.mp3")
        type_print(x)
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)  # Keeps checking every 0.1 sec

    else:
        print("Access Denied.")

        
    print(f"Done in {perf_counter() - t0:.2f} sec")
