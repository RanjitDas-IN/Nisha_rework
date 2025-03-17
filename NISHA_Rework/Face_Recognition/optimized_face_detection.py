import face_recognition
import cv2
import threading


ref_image = face_recognition.load_image_file("Face_Recognition/profilePic.jpg",)

ref_encoding = face_recognition.face_encodings(ref_image)[0]


video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
frame_skip = 2
frame_count = 0


face_locations = []
face_encodings = []
lock = threading.Lock()

def process_frame(frame):
    global face_locations, face_encodings
    
    small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
    rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
    
    detected_faces = face_recognition.face_locations(rgb_frame, model='hog')
    encodings = face_recognition.face_encodings(rgb_frame, detected_faces)
    
    with lock:
        face_locations = detected_faces
        face_encodings = encodings

while True:
    ret, frame = video_capture.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    if frame_count % frame_skip == 0:
        threading.Thread(target=process_frame, args=(frame,)).start()

    with lock:
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces([ref_encoding], face_encoding)
            label = "Unknown"
            if matches[0]:
                label = "Boss"
            
            # Scale back to original frame size
            top, right, bottom, left = top * 2, right * 2, bottom * 2, left * 2
            
            color = (0, 255, 0) if label == "Boss" else (0, 0, 255)
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.putText(frame, label, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    
    frame_count += 1
    cv2.imshow("Face Recognition", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('c'):
        break


if __name__=="__main__":
    video_capture.release()
    cv2.destroyAllWindows()
