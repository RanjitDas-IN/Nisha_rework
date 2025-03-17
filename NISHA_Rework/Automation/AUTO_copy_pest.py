import subprocess
import pyautogui
import pyperclip
import time


def copy_to_clipboard(text):
    """Copies text to clipboard. NISHA"""
    pyperclip.copy(text)
    print(f"Copied to clipboard: {text}")

def paste_from_clipboard():
    """NISHA will Pastes clipboard content at the current cursor location."""
    pyautogui.hotkey("ctrl", "v")  # Simulate Ctrl + V
    print("Pasted from clipboard.")

def get_clipboard_data():
    """Gets the current clipboard content."""
    return pyperclip.paste()

def clear_clipboard():
    """Clears the clipboard by copying an empty string."""
    pyperclip.copy("")
    print("Clipboard cleared.")

# Example Usage
if __name__ == "__main__":

    # copy_to_clipboard("pyyyyyyyyyyyyyy")  # Copy text
    time.sleep(1)

    paste_from_clipboard()  # Paste the copied text
    time.sleep(1)

    print("Clipboard Data:", get_clipboard_data())  # Get clipboard content

    clear_clipboard()  # Clear clipboard


