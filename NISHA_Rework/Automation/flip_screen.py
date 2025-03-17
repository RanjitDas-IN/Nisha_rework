import rotatescreen,time

screen = rotatescreen.get_primary_display()
print("Rotating Sir...")
screen.rotate_to(90) # Rotate 90 degrees clockwise
time.sleep(3)

screen.rotate_to(180)
time.sleep(3)



screen.rotate_to(270) # Rotate 90 degrees counterclockwise
time.sleep(3)
screen.rotate_to(0) # Rotates to 0 degrees, the default orientation
