import pvcobra
import pyaudio
import numpy as np
import speech_recognition as sr

# Create Cobra instance
cobra = pvcobra.create(access_key='QDyLUe1AJZ6i4Ia4Q5IyWrcc4LdJI8l05cC8QzAgKMwFRqGHhfH4yQ==')

# Audio setup
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
FRAMES_PER_BUFFER = 512

# Initialize PyAudio
audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=FRAMES_PER_BUFFER)

# Speech recognizer
recognizer = sr.Recognizer()
mic = sr.Microphone(sample_rate=RATE)

# Function to get audio frame from stream
def get_frame():
    return np.frombuffer(stream.read(FRAMES_PER_BUFFER, exception_on_overflow=False), dtype=np.int16)

try:
    print("🎧 Listening with Cobra... (Press CTRL+C to stop)")
    while True:
        try:
            # Cobra VAD
            frame = get_frame()
            probability = cobra.process(frame)

            # If voice detected
            if probability > 0.85:
                print("🗣️ Voice detected! Trying to recognize speech...")

                with mic as source:
                    recognizer.adjust_for_ambient_noise(source, duration=0.2)
                    audio_data = recognizer.listen(source, timeout=3, phrase_time_limit=5)

                try:
                    text = recognizer.recognize_google(audio_data)
                    print("📝 You said:", text)
                except sr.UnknownValueError:
                    print("🤷 Couldn’t understand speech. Going back to VAD...")
                except sr.RequestError as e:
                    print(f"⚠️ API request error: {e}. Going back to VAD...")

        except Exception as e:
            print(f"🔥 Unexpected error: {e}. Recovering...")

except KeyboardInterrupt:
    print("\n🛑 Stopped by user.")

# Clean up
stream.stop_stream()
stream.close()
audio.terminate()
cobra.delete()
