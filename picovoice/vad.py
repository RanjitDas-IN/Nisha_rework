#Use case
# ✅ Detect human voice using Cobra
# ✅ Then capture what was said using speech-to-text
# ✅ Then print it as text


# workflow:
# Microphone audio
#    │
#    ▼
# [Cobra VAD] — is someone speaking? (probability > 0.8?)
#    │
#    ▼
# Yes → Activate [Speech Recognition]
#    │
#    ▼
# Transcribe → Print text



# Example Output 
# Cobra VAD is running. Press CTRL+C to stop.
# Voice probability: 0.05
# Voice probability: 0.07
# Voice probability: 0.82  ← someone is probably speaking
# Voice probability: 0.90
# Voice probability: 0.10


import pvcobra
import pyaudio #to capture audio from your microphone.
import numpy as np #to process raw audio bytes into numeric arrays.

ACCESS_KEY = 'QDyLUe1AJZ6i4Ia4Q5IyWrcc4LdJI8l05cC8QzAgKMwFRqGHhfH4yQ=='

cobra = pvcobra.create(access_key=ACCESS_KEY)

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
FRAMES_PER_BUFFER = 512

audio = pyaudio.PyAudio()

stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=FRAMES_PER_BUFFER)


def get_next_audio_frame():
    audio_data = stream.read(FRAMES_PER_BUFFER, exception_on_overflow=False)
    audio_frame = np.frombuffer(audio_data, dtype=np.int16)
    return audio_frame


try: 
    print("Cobra VAD is running. press CTRL+C to stop.")
    while True:
        audio_frame = get_next_audio_frame()
        voice_probability= cobra.process(audio_frame)
        print(f"Voice probability: {voice_probability:.2f}")

except KeyboardInterrupt:
    print("Stoping Cobra VAD...")


stream.stop_stream()
stream.close()
audio.terminate()
cobra.delete()