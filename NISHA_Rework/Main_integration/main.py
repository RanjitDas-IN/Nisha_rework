import sys,os
import ctypes
import threading
import time
import sdl2
import sdl2.sdlmixer
from tts_accelarator import speak_text as model_speak

# ──────────────────────────────────── Defining Path ───────────────────────────────────────────
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
# ───────────────────────────────────────────────────────────────────────────────


# ───────────────────────────────────── Importing ──────────────────────────────────────────


from Backend.chatbot import (colors,
                             ChatBot,
                             random)

from Initial_Authentication import voice_Auth
from Backend.real_time_nisha import RealtimeSearchEngine
# ──────────────────────────────────── Play MP3 file ───────────────────────────────────────────

# Setup SDL2 and SDL_mixer
def init_audio():
    sdl2.SDL_Init(sdl2.SDL_INIT_AUDIO)
    sdl2.sdlmixer.Mix_OpenAudio(44100, sdl2.AUDIO_S16LSB, 2, 512)
    sdl2.sdlmixer.Mix_AllocateChannels(1)

def playsound_loop(mp3, stop_event):
    init_audio()
    mp3_bytes = mp3.encode('utf-8')  # SDL expects bytes
    music = sdl2.sdlmixer.Mix_LoadMUS(mp3_bytes)

    if not music:
        raise RuntimeError("Failed to load music!")

    sdl2.sdlmixer.Mix_PlayMusic(music, -1)  # loop infinitely
    sdl2.sdlmixer.Mix_VolumeMusic(int(0.5 * sdl2.sdlmixer.MIX_MAX_VOLUME))  # 🛎️ Set volume to 30%

    while not stop_event.is_set():
        time.sleep(0.01)  # Even faster polling

    sdl2.sdlmixer.Mix_HaltMusic()
    sdl2.sdlmixer.Mix_FreeMusic(music)
    sdl2.sdlmixer.Mix_CloseAudio()
    sdl2.SDL_Quit()

# ───────────────────────────────────────────────────────────────────────────────


# ───────────────────────────────────── General Query ──────────────────────────────────────────
def general_query():
    global output_from_general_model
    print(f"\n\033[1m{random.choice(colors)}{x} \033[0m")
    output_from_general_model = ChatBot(x)


# ──────────────────────────────────── Main Function ──────────────────────────────────── 
# ───────────────────────────────────── General Query ──────────────────────────────────────────
def real_time_search_engine():
    global output_from_realtime_model
    output_from_realtime_model = RealtimeSearchEngine(x)


# ──────────────────────────────────── Main Function ──────────────────────────────────── 

if __name__ == "__main__":
    # voice_Auth()
    x=input("You: ")
    from Backend.Decision_making_model import (FirstLayerDMM)
    print(FirstLayerDMM(x))         #   ['general hello dear']
    from Backend.Decision_making_model import (category)
    if category == "general":
        general_query()
        print(output_from_general_model)

        stop_event = threading.Event()
        mp3_thread = threading.Thread(target=playsound_loop, args=(
            "NISHA_Rework/PvEagle_Voice_Auth/gpt-beep-soung_WJI67WU6.mp3", stop_event), daemon=True)
        mp3_thread.start()

        model_speak(output_from_general_model)

        stop_event.set()
        mp3_thread.join()


    elif category == "realtime" or "google" in category:
        real_time_search_engine()
        print(output_from_realtime_model)

        stop_event = threading.Event()
        mp3_thread = threading.Thread(target=playsound_loop, args=(
            "NISHA_Rework/PvEagle_Voice_Auth/gpt-beep-soung_WJI67WU6.mp3", stop_event), daemon=True)
        mp3_thread.start()

        model_speak(output_from_realtime_model)

        stop_event.set()
        mp3_thread.join()

    elif category == "system":
        print("Printing statement: This is a System Task")

    elif category == "open":
        print("Printing statement: This is a Open App")


    elif category == "close":
        print("Printing statement: This is a Close App")


    elif category == "play":
        print("Printing statement: This is a Play Command")


    elif "generate" in category:
        print("Printing statement: This is a Image Generation")


    elif category == "content":
        print("Printing statement: This is a Content Creation")



    elif  "youtube" in category:
        print("Printing statement: This is a YouTube Search")


    elif category == "reminder":
        print("Printing statement: This is a Reminder Task")


    else:
        
        print("Printing statement: This is a Unknown task")

