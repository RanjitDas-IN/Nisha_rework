import subprocess
import pyautogui
import time
import os

def open_notepad_and_type(text, typing_speed=0.1):
    app_name= 'notepad.exe'
    """To automate NISHA, Opens Notepad and types the given text with a typing effect."""
    subprocess.Popen(app_name)
    time.sleep(1)
    
    pyautogui.write(text, interval=typing_speed)
    time.sleep(3)
    os.system(f"taskkill /f /im {app_name} > nul 2>&1")
    print(f"{app_name} closed successfully.")


# Example usage
open_notepad_and_type("\rHello, Ranjit! NISHA is here! 😎", typing_speed=0.1)
