import winreg
import os
import time
from datetime import datetime
import threading
from playsound import playsound

def set_dark_mode(enable: bool):
    try:
        theme_value = 0 if enable else 1  # 0 = Dark, 1 = Light
        # Open registry keys
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, "AppsUseLightTheme", 0, winreg.REG_DWORD, theme_value)
            winreg.SetValueEx(key, "SystemUsesLightTheme", 0, winreg.REG_DWORD, theme_value)

        
        restart_explorer()
        
        print(f"Dark Mode {'Enabled' if enable else 'Disabled'}")
    except Exception as e:
        print(f"Failed to set theme: {e}")

def restart_explorer():
    os.system("taskkill /f /im explorer.exe & start explorer.exe")

def darkmood(OFF):
    if OFF.lower() == "off":
        playsound("Nisha_voice_pakes\darf_mood_OFF.mp3")
        set_dark_mode(False)  # Enable light mode 
    else:
        pass
def darkmood(OFF):
    if OFF.lower() == "on":
        playsound('Nisha_voice_pakes\Dark_mood_ON.mp3')
        set_dark_mode(True)  # Enable dark mode 
    else:
        pass

def auto_theme_switch():
    while True:
        hour = datetime.now().hour
        if 18 <= hour or hour < 6:  # Nighttime (6 PM - 6 AM)
            set_dark_mode(True)
        else:  # Daytime
            set_dark_mode(False)
        time.sleep(3600)  # every hour


threading.Thread(target=auto_theme_switch, daemon=True).start()



darkmood("oN")
darkmood("oFF")
