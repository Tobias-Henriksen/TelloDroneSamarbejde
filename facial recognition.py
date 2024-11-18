import threading
import cv2
from deepface import DeepFace

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

counter = 0
face_match = False
lock = threading.Lock()

# Load and resize reference image
reference_img = cv2.imread("C:\\Users\\Dirie\\PycharmProjects\\tello drone\\IMG_20241118_112605705.jpg")
reference_img = cv2.resize(reference_img, (640, 480))

def check_face(frame):
    global face_match
    try:
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = DeepFace.verify(rgb_frame, reference_img.copy(), model_name="VGG-Face", detector_backend="opencv")
        with lock:
            face_match = result['verified']
    except ValueError:
        with lock:
            face_match = False

while True:
    ret, frame = cap.read()

    if ret:
        if counter % 30 == 0:  # Check every 30 frames
            try:
                threading.Thread(target=check_face, args=(frame.copy(),)).start()
            except ValueError:
                pass
        counter += 1

        with lock:
            if face_match:
                cv2.putText(frame, "MATCH!", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
            else:
                cv2.putText(frame, "NO MATCH!", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)

        cv2.imshow("video", frame)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()