import pvporcupine
import subprocess
from pvrecorder import PvRecorder
import pyttsx3
import builtins  # To override the default print functions
ACCESS_KEY = "1VJE8mZDXiwMsmUtKDXb9LREGJo1gZQU19J3JlcW+aBf7aMgafgwiQ=="

#Initialize pyttsx3 engine globally
engine = pyttsx3.init()

def speak(text):
    """Use global pyttsx3 engine to avoid thread conflicts."""
    engine.say(text)
    engine.runAndWait()

# Custom print function that speaks when "Listening...." is printed
def custom_print(*args, **kwargs):
    builtins.print(*args, **kwargs)  #Call original print
    if "Listening....." in args:
        #speak("Hello Boss! At your service.")
        speak("Hello Boss!")

#Override default print function
print = custom_print

#Initialize wake word detection
porcupine = pvporcupine.create(
    access_key=ACCESS_KEY,
    keyword_paths=["Nisha_rework/picovoice/wakeup_en_windows_v3_0_0.ppn"]  #Custom wake word model
)

recorder = PvRecorder(device_index=-1, frame_length=porcupine.frame_length)

try:
    recorder.start()
    print("Listening.....")  #This will print and speak "Listening"

    while True:
        pcm = recorder.read()  #Capture audio frame
        keyword_index = porcupine.process(pcm)  #Process the frame

        if keyword_index >= 0:
            print("Detected wake word! Initializing Nisha...")
            # print("launching...")
            subprocess.run(["python", r"/home/ranjit/NISHA/Nisha_rework/NISHA_Rework/Backend/chatbot.py"])

            speak("Welcome back, Sir.")  


except KeyboardInterrupt:
    print("\nStopping....")
    recorder.stop()
