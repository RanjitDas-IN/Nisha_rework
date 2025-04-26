""" Nohobo, Not Usefull, drop this library""" 

import os
import sys
import time
import pygame
import numpy as np
from clapDetector import ClapDetector

# Hide pygame support message
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
sys.stderr = open(os.devnull, 'w')

# ==== SETTINGS ====
INPUT_DEVICE_INDEX = -1  # Set your microphone index here if needed

# Energy detection settings (tuned for your room)
cooldown_frames = 25              # frames to ignore after detection
base_energy_threshold = 1_500_000 # hard floor for minimum energy
energy_boost_factor = 3.5         # boost over ambient noise
energy_history_size = 15          # frames to average
spike_ratio = 1.7                 # how sharp a spike must be

# ==== INIT ====
tc = ClapDetector(inputDevice=INPUT_DEVICE_INDEX, logLevel=0)
tc.initAudio()

print("Clap detection started (final version). Waiting for 2 claps...")

clap_count = 0
cooldown_counter = 0
energy_history = []

def playsound():
    pygame.mixer.init()
    try:
        pygame.mixer.music.load("NISHA_Rework/Nisha_voice_pakes/Voice_matched.mp3")
        pygame.mixer.music.play()
        print("Playing voice...")
    except Exception as e:
        print(f"Error playing sound: {e}")

try:
    while True:
        # Get audio buffer
        audioData = tc.getAudio()
        samples = np.frombuffer(audioData, dtype=np.int16)

        # Calculate simple energy
        energy = np.sum(samples.astype(float)**2) / len(samples)
        energy_history.append(energy)

        # Keep history size limited
        if len(energy_history) > energy_history_size:
            energy_history.pop(0)

        avg_energy = np.mean(energy_history) if energy_history else 0
        dynamic_threshold = max(avg_energy * energy_boost_factor, base_energy_threshold)

        # Skip if not a sudden spike
        if len(energy_history) >= 2:
            previous_energy = energy_history[-2]
            if energy < previous_energy * spike_ratio:
                time.sleep(1/60)
                continue

        # Detection logic
        if cooldown_counter > 0:
            cooldown_counter -= 1
        elif energy > dynamic_threshold:
            clap_count += 1
            print(f"Clap #{clap_count} detected! Energy: {int(energy)}")
            cooldown_counter = cooldown_frames

        if clap_count == 2:
            playsound()
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            break

        time.sleep(1 / 60)

except KeyboardInterrupt:
    print("\nInterrupted by user. Exiting...")

finally:
    tc.stop()
    sys.stderr = sys.__stderr__
