import cv2
import mediapipe as mp
import pyautogui

# Inicialize a captura de vídeo
cam = cv2.VideoCapture(0)

# Inicialize a malha facial do Mediapipe
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_w, screen_h = pyautogui.size()

# Variável para armazenar o estado do clique
clicking = False

while True:
    # Capture um frame da câmera
    success, frame = cam.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_frame)
    landmark_points = output.multi_face_landmarks
    frame_h, frame_w, _ = frame.shape

    if landmark_points:
        landmarks = landmark_points[0].landmark
        for id, landmark in enumerate(landmarks[474:478]):
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)
            if id == 1:
                screen_x = screen_w * landmark.x
                screen_y = screen_h * landmark.y
                pyautogui.moveTo(screen_x, screen_y)

        # Pontos de referência para o olho direito
        right_eye = [landmarks[133], landmarks[159]]
        for landmark in right_eye:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 255), -1)

        # Verifique a distância vertical entre dois pontos do olho direito
        if (right_eye[0].y - right_eye[1].y) < 0.004:
            if not clicking:
                pyautogui.mouseDown()
                clicking = True
        else:
            if clicking:
                pyautogui.mouseUp()
                clicking = False

    # Mostre o frame na tela
    cv2.imshow('Eye Controlled Mouse', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
