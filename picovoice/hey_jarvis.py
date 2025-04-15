import pvporcupine
from pvrecorder import PvRecorder
import subprocess
import pyttsx3
import builtins  # To override the default print functions


ACCESS_KEY = 'QDyLUe1AJZ6i4Ia4Q5IyWrcc4LdJI8l05cC8QzAgKMwFRqGHhfH4yQ=='  

# Initialize pyttsx3 engine 
engine = pyttsx3.init()

def speak(text):
    """Use global pyttsx3 engine to avoid thread conflicts."""
    engine.say(text)
    engine.runAndWait()

# Custom print function that speaks when "Listening...." is printed
def custom_print(*args, **kwargs):
    builtins.print(*args, **kwargs)  #Call original print
    if "Listening....." in args:
        speak("Hellou Boss! At your servese")
        # speak("Intelligence sequence activated...")

#Override default print function
print = custom_print

#Initialize wake word detection
porcupine = pvporcupine.create(
    access_key=ACCESS_KEY,
    keywords=['jarvis']
)

recorder = PvRecorder(device_index=-1, frame_length=porcupine.frame_length)

try:
    recorder.start()
    print("Listening.....")  #This will print and speak "Listening"

    while True:
        pcm = recorder.read()  #Capture audio frame
        keyword_index = porcupine.process(pcm)  #Process the frame

        if keyword_index >= 0:
            print("Detected 'Jarvis'! Launching Nisha....")
            speak("Welcome back Sir, Neural network initialized! Boss, Nihsa is now fully operational.")
            subprocess.run(["python", r"/home/ranjit/NISHA/Nisha_rework/NISHA_Rework/Backend/chatbot.py"])
        
except KeyboardInterrupt:
    print("\nStopping....")
    recorder.stop()
finally:
    porcupine.delete()
    recorder.delete()

