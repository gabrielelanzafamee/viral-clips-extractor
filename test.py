import cv2
import face_recognition

input_video = "tmp/73A01d2E071F341C.mp4"

video = cv2.VideoCapture("tmp/73A01d2E071F341C.mp4")

fps = video.get(5)
width, height = int(video.get(3)), int(video.get(4))
size = (width, height)

while video.isOpened():
    ret, frame = video.read()

    if not ret:
        break

    im = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    cv2.imshow("Window", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
