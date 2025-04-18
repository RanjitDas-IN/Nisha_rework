import os
import sys
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
sys.stderr = open(os.devnull, 'w')

import time
import pygame
from clapDetector import ClapDetector

# Initialize ClapDetector with logging off
tc = ClapDetector(inputDevice=-1, logLevel=0)
tc.initAudio()

# Notify user
print("Detecting...")

# Configuration
# thresholdBias = 6000
# lowcut=200               #< increase this to make claps detection more strict 
# highcut=3200     

# thresholdBias = 2000     # Picks up even softer claps. Still avoids tiny ambient noise like fans or keyboard taps.
# lowcut = 200              # Filters out deep background noise (like AC hums), while keeping clap impact intact.
# highcut = 8000           # Gives you the full "snap" of a clap, especially important for softer ones with higher pitch.

thresholdBias = 3000   # Allows for claps + voice without triggering on background
lowcut = 120           # Still cuts fan, floor, etc.
highcut = 7000         # Lets full clap & voice through, blocks hiss and static


clap_count = 0

def playsound():
    pygame.mixer.init()
    pygame.mixer.music.load("NISHA_Rework/Nisha_voice_pakes/Voice_matched.mp3")
    pygame.mixer.music.play()

try:
    while True:
        audioData = tc.getAudio()
        result = tc.run(thresholdBias=thresholdBias, lowcut=lowcut, highcut=highcut, audioData=audioData)
        if result:
            clap_count += 1
        # Default: play sound when exactly two claps detected
        if clap_count == 2:
            playsound()
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            break
        time.sleep(1/60)

except KeyboardInterrupt:
    pass
finally:
    tc.stop()
    # Optionally restore stderr
    sys.stderr = sys.__stderr__