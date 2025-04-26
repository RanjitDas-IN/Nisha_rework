import sys,os
from tts_accelarator import speak_text as model_speak

# ──────────────────────────────────── Defining Path ───────────────────────────────────────────
#  1) Figure out the path to your project root (one level up from this file)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
#  2) Add it to sys.path so Python can find your SPEAK package
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
# ───────────────────────────────────────────────────────────────────────────────


# ──────────────────────────────────── Play MP3 file ───────────────────────────────────────────

def playsound(mp3):
    # import pygame
    pygame.mixer.init() # type: ignore
    pygame.mixer.music.load(mp3)    # type: ignore
    pygame.mixer.music.play()   # type: ignore
 # Keeps checking every 0.1 sec

# ───────────────────────────────────────────────────────────────────────────────



# ──────────────────────────────────── Importing Voice Model Created, Trained & Optimised by Me ───────────────────────────────────────────


# ──────────────────────────────────── Voice Auth function ───────────────────────────────────────────
def voice_Auth():
    from Voice_Recognition.Real_Time_voice_verification import record_voice, is_match_from_signal, random, nisha_lines, type_print, playsound, time
    signal, fs = record_voice(duration=5)

    print("Verifying voice, please wait...")
    match, similarity = is_match_from_signal(signal, fs)

    print(f" Match: {match}, Accuracy: {similarity:.4f}")
    if match:
        print("\nAccess Granted!")
        x=random.choice(nisha_lines)
        model_speak(x)

    else:
        print("\nAccess Denied.\n\n")
        
        print("Retrying........")
        import pygame
        # playsound("NISHA_Rework/Main_integration/not_detected.mp3")
        while pygame.mixer.music.get_busy():# type: ignore
            time.sleep(0.1) 
        voice_Auth()

# ──────────────────────────────────── # ──────────────────────────────────── # ──────────────────────────────────── 




# ──────────────────────────────────── Main Function ──────────────────────────────────── 

if __name__ == "__main__":
    voice_Auth()


