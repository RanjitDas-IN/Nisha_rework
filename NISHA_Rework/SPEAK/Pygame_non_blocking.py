import pygame
import time

def print_fibonacci_with_type_effect():
    a, b = 0, 1
    for _ in range(7):
        print(a, end=' ', flush=True)
        time.sleep(0.5)  # Delay of 0.5 seconds between each print
        a, b = b, a + b

def playsound():
    pygame.mixer.init()
    pygame.mixer.music.load("NISHA_Rework/PvEagle_Voice_Auth/gpt-beep-soung_WJI67WU6.mp3")
    pygame.mixer.music.play()


playsound()
print_fibonacci_with_type_effect()
print_fibonacci_with_type_effect()

while pygame.mixer.music.get_busy():
    time.sleep(0.1)  # Keeps checking every 0.1 sec
