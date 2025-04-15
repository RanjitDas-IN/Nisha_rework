import subprocess
import sounddevice as sd
import soundfile as sf

# Define paths
def pipertts(text:str):
    piper_exe = r"C:\Users\ranji\Downloads\piper_windows_amd64\piper\piper.exe" # Update the path if necessaryy
    model_file = r"C:\Users\ranji\Downloads\piper_windows_amd64\piper\en_US-amy-medium.onnx" 
    output_wav = "output.wav"

    # Run Piper AI

    command = f'echo {text} | "{piper_exe}" --model "{model_file}" --output_file "{output_wav}"'

    subprocess.run(command, shell=True)

    print(f"Speech saved to {output_wav}")


    data, samplerate = sf.read(output_wav)

    # Play the audio
    sd.play(data, samplerate)
    sd.wait()  # Wait until playback finishes

if __name__== '__main__':
    pipertts("Dark Mood On")
    s= """Take same time as Edge TTS jenny neural but faster than other voices"""