import face_recognition
import cv2

# Load the image
image_path = "Face_Recognition\Firefly20240709212353.jpg"
# image_path = "Face_Recognition\profilePic.jpg"
image = cv2.imread(image_path)
image = cv2.resize(image,(600,600),interpolation=cv2.INTER_NEAREST)

# Convert BGR to RGB
rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


face_locations = face_recognition.face_locations(rgb_image)


for i, (top, right, bottom, left) in enumerate(face_locations):
    cv2.rectangle(rgb_image, (left, top), (right, bottom), (0, 255, 0), 2)  # Green box NISHA
    cv2.putText(rgb_image, f"Face {i+1}", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)


cv2.imshow("Face Detection", rgb_image)
cv2.waitKey(0)
cv2.destroyAllWindows()


print("Detected face locations:", face_locations)
print("Total number of faces:",len(face_locations))
