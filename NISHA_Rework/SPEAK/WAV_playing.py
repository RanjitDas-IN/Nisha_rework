import sounddevice as sd
import soundfile as sf


# Load an audio file
filename = "Nisha_voice_pakes\de-DE-FlorianMultilingualNeural.wav"
data, samplerate = sf.read(filename)

# Play the audio
sd.play(data, samplerate)
sd.wait()  # Wait until playback finishes

