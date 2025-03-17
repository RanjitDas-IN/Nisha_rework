import pyautogui

# Get screen dimensions
screen_width, screen_height = pyautogui.size()

# Calculate center coordinates
center_x = screen_width // 2
center_y = screen_height // 2

# Move the mouse to the center
pyautogui.moveTo(center_x, center_y)

# Click the mouse
pyautogui.click()

print("Siccessfully clicked")