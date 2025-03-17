import face_recognition
import cv2
import time

start_time = time.perf_counter()

# Code to be timed
result = 0


# Load and resize the image for faster processing
image = face_recognition.load_image_file("Face_Recognition\profilePic.jpg")
small_image = cv2.resize(image, (0, 0), fx=0.25, fy=0.25)  # Reduce size by 75%

# Get face encodings using the 'cnn' model
encoding = face_recognition.face_encodings(small_image, model='cnn')[0]

print(encoding)
result = 0
for i in range(1000000):
    result += i

end_time = time.perf_counter()

execution_time = end_time - start_time
print(f"Execution time: {execution_time:.4f} seconds")