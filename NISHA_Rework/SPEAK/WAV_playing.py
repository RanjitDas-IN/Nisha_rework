import sounddevice as sd
import soundfile as sf
import time

def print_fibonacci_with_type_effect():
    a, b = 0, 1
    for _ in range(7):
        print(a, end=' ', flush=True)
        time.sleep(0.5)  # Delay of 0.5 seconds between each print
        a, b = b, a + b
        

# Loading an audio file
audio = "testing.mp3"
data, samplerate = sf.read(audio)

# Playing the audio
sd.play(data, samplerate)
print_fibonacci_with_type_effect()
sd.wait()  # Wait until playback finishe

