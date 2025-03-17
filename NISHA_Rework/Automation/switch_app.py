import pygetwindow as gw
import sounddevice as sd
import soundfile as sf
import threading
import time

def playsound_async(filename):
    """Plays sound in a separate thread."""
    def play():
        data, samplerate = sf.read(filename)
        sd.play(data, samplerate)
        sd.wait()  # Wait until playback finishes

    threading.Thread(target=play, daemon=True).start()  # Run in background

def switch_to_app(app_name):
    """Switches to the given application."""
    windows = [win for win in gw.getWindowsWithTitle(app_name) if win.isMinimized or win.isMaximized or win.isActive]

    if windows:
        win = windows[0]
        win.minimize()  # Minimize first
        time.sleep(0.5)
        win.restore()  # Restore to focus
        print(f"Switched to {app_name}!")
    else:
        print(f"{app_name} is not open.")

def switch_between_apps():
    """Switches to Chrome, plays sound, then returns to VS Code after 2 seconds."""
    playsound_async(r'Nisha_voice_pakes\Switching_WAV.wav')  # Play sound while switching
    time.sleep(1)
    switch_to_app("Google Chrome")  # Switch to Chrome
    
    time.sleep(2)  # Wait for 2 seconds

    playsound_async(r'Nisha_voice_pakes\Return_to_WAV.wav')  # Play sound while switching back
    time.sleep(0.5)
    switch_to_app("Visual Studio Code")  # Switch back to VS Code

# Example usage
switch_between_apps()
time.sleep(2)