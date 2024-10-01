# realizando um teste para entender o código 

import cv2
import mediapipe as mp
import pyautogui

# Inicialização do MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Captura de vídeo da webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    # Conversão para escala de cinza
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detecção da mão
    results = hands.process(gray)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Obtenha as coordenadas da ponta do dedo indicador
            index_finger_x = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
            index_finger_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y

            # Mapeie as coordenadas da mão para a posição do mouse na tela
            screen_width, screen_height = pyautogui.size()
            mouse_x = int(index_finger_x * screen_width)
            mouse_y = int(index_finger_y * screen_height)

            # Mova o mouse
            pyautogui.moveTo(mouse_x, mouse_y)

    # Exiba o vídeo com as marcações da mão
    cv2.imshow("Hand Tracking", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
