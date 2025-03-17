# from multiple_face_detection import *
from multiple_face_detection import (known_faces,
                                     known_names,
                                     video_capture,
                                     frame_skip,
                                     frame_count,
                                     face_locations,
                                     face_encodings,
                                     lock,
                                     process_frame,
                                     ret, 
                                     frame,
                                     face_recognition,
                                     cv2
                                     )



if __name__=="__main__":
    video_capture.release()
    cv2.destroyAllWindows()