import face_recognition
import cv2


ref_image = face_recognition.load_image_file("Face_Recognition\profilePic.jpg")  
ref_encoding = face_recognition.face_encodings(ref_image)[0]  


# video_capture = cv2.VideoCapture(0)  
video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)  #edit

while True:
    ret, frame = video_capture.read() 
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

  
  
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces([ref_encoding], face_encoding)
        label = "Unknown"

        if matches[0]:
            label = "Me: Ultimate creator"


        color = (0, 255, 0) if label == "Me: Ultimate creator" else (0, 0, 255) 
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        cv2.putText(frame, label, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

   
    cv2.imshow("Face Recognition", frame)

    # Exit on pressing 'c'
    if cv2.waitKey(1) & 0xFF == ord('c'):
        break

# Release webcam
video_capture.release()
cv2.destroyAllWindows()
