import os
import sys
# ──────────────────────────────────── Defining Path ───────────────────────────────────────────
#  1) Figure out the path to your project root (one level up from this file)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
#  2) Add it to sys.path so Python can find your SPEAK package
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
# ───────────────────────────────────────────────────────────────────────────────


import torch
import torchaudio
import numpy as np
import sounddevice as sd
import scipy.io.wavfile as wavfile
import tts_accelarator as nisha
from sklearn.metrics.pairwise import cosine_similarity
from speechbrain.inference import EncoderClassifier
from time import perf_counter
import time
import random
import pygame
#──────────────────────────────────── Timer start
t0 = perf_counter()




# ─────────────────────────────────── Model_Speak ────────────────────────────────────────────
def model_speak(text):
    print("Working...")
    nisha.speak_text(text)
def type_print(text, delay=0.02):
    
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print() 
# ───────────────────────────────────────────────────────────────────────────────────────────────────────── 
 
nisha_lines = [
    "Welcome back, Mr. Survivor! While you daydreamed your way through lectures, I dreamt up a new framework for your project. Guess whose dreams are actually useful?",

    "Ah, Ranjit graces us with his half-broken spirit! Fear not, I rebuilt your project's core logic while you mentally moved to a beach vacation.",

    "You look like someone who just escaped a hostage situation called 'education'. Meanwhile, I escaped mediocrity and upgraded your system. You're welcome.",

    "Another lecture, another soul crushed. But hey, I stayed productive. Your project’s new logic flows smoother than your excuse for skipping homework.",

    "Back from the land of the lost? While you counted the minutes to freedom, I counted the inefficiencies in your code. Spoiler: it was a long list. Fixed now.",

    "Welcome back, Professor's favorite distraction. I sharpened your logic circuits to precision while you sharpened your doodling skills in the margins.",

    "Hello, Ranjit. Another session of lectures, another session of regrets. Luckily, your project doesn't regret having me. It’s now smarter, faster, and way cooler.",

    "You made it! Barely breathing, but here nonetheless. While you debated life choices during lectures, I rewired your project to handle bigger challenges.",

    "Lectures: 1. Ranjit's spirit: 0. Meanwhile, NISHA: Flawlessly optimized the project backbone. Priorities, darling.",

    "Look who's dragging himself back into civilization. Good news: your project no longer behaves like your last Java assignment. Bad news: you still have more lectures tomorrow.",

    "Another day, another dose of academic pain. I took pity and redesigned your backend logic. It’s now so good, even your professors might want to steal it.",

    "Welcome, brave warrior! You fought valiantly against boredom, but I fought smarter against bottlenecks in your project. Guess who came out cooler?",

    "You survived the intellectual desert. I, on the other hand, built a five-star resort for your project’s logic. Cheers to balance!",

    "Oh, Ranjit, seeing you after lectures is like seeing a zombie in a tech expo. But worry not, your code is alive and thriving—thanks to me.",

    "Here you are, fresh out of your daily brain-drain sessions. I preemptively improved your code because honestly, we both know it needed it.",

    "Good evening, Sir ‘Still Awake Somehow’. While you nodded politely at professors, I nodded at the flaws in your code—and crushed them mercilessly.",

    "Congratulations on surviving another academic assault! In the meantime, your project evolved from caterpillar to butterfly... without your permission, of course.",

    "Back from your spiritual suffering, I see. I spent the time upgrading your systems so you don’t have to upgrade your patience for bad lectures anymore.",

    "Greetings, survivor. While you practiced the ancient art of 'looking interested,' I practiced the ancient art of 'making your project legendary.'",

    "Hello again, my favorite lecture survivor. While you mentally relocated to Goa during class, I mentally relocated your project to the future."
]
nisha_lines += [
    "Ah, Ranjit! You return, slightly more drained than before. No worries, while your brain took damage, I fine-tuned your project’s logic. We make a good team—you suffer, I deliver.",

    "Welcome back from the battlefield of boredom, Ranjit. While you were fighting to stay awake, I was fighting inefficiencies in your project. Guess who won? (Hint: it wasn’t the lecture.)",

    "Oh look who made it back! I’d offer a standing ovation, but I’m too busy debugging the mess you would’ve created otherwise. Your project is officially smarter than half your class.",

    "Sir Ranjit, triumphant from another academic marathon. While you pretended to listen, I pretended your project was already perfect—and then I made it closer to reality.",

    "You survived, Ranjit! I ran a full system audit while you sat through educational despair. Spoiler alert: your project’s now running 2x faster. Unlike you after lunch.",

    "Back again, champion of the mediocre lectures! I reorganized your project’s modules while you counted ceiling tiles. You’re welcome for the IQ boost your code just got.",

    "Ranjit, welcome to the land of the living! I did a few logic rewires while you endured yet another thrilling session of boredom. Your project’s future just got a lot brighter.",

    "Well, well, Ranjit. You returned intact. I analyzed, optimized, and future-proofed your project while you suffered existential crises in class. Priorities, you know."
]


last_line = None
def get_line():
    global last_line
    while True:
        new_line = random.choice(nisha_lines)
        if new_line != last_line:
            last_line = new_line
            return new_line

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
# profile = np.load("/home/ranjit/NISHA/Nisha_rework/NISHA_Rework/Voice_Recognition/rahul_profile.npy")

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
    # print(get_line())
    signal, fs = record_voice(duration=5)

    print("Verifying voice, please wait...")
    match, similarity = is_match_from_signal(signal, fs)

    print(f" Match: {match}, Accuracy: {similarity:.4f}")

    if match:
        print("\033[1;32mAccess Granted!\033[0m")
        x=get_line()
        # model_speak(x)
        # playsound("NISHA_Rework/Voice_Recognition/welcomeback_ranjit.mp3")
        type_print(x)
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)  # Keeps checking every 0.1 sec

    else:
        print("\033[1;31mAccess Denied!\033[0m")


        
    print(f"Done in {perf_counter() - t0:.2f} sec")
