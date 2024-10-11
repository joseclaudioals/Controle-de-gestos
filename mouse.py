import cv2 
import mediapipe
import pyautogui
 

captura_de_video = cv2.VideoCapture(0)

while True:
        captura_de_video.isOpened()
        camera, frame = captura_de_video.read()
        videocinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        for(x, y, l,a) in videocinza:
            cv2.rectangle(frame, (x, y),(x + l, y + a), (255, 0, 0), 2)

        cv2.imshow("fecha", frame)

        if cv2.waitKey(1) == ord("f"):
            break

captura_de_video.release()
cv2.destroyAllWindows
