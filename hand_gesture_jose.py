import cv2
import mediapipe as mp
import pyautogui
import time

# Inicializa o Mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

# Configura a captura de vídeo
cap = cv2.VideoCapture(0)

# Espera para a câmera estabilizar
time.sleep(2)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Converte a imagem para RGB
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    # Desenha as mãos detectadas
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Obtenha as posições dos dedos indicador e do meio
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            index_finger_base = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
            middle_finger_base = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]

            # Converte para coordenadas da tela
            h, w, _ = frame.shape
            index_x, index_y = int(index_finger_tip.x * w), int(index_finger_tip.y * h)
            middle_x, middle_y = int(middle_finger_tip.x * w), int(middle_finger_tip.y * h)

            # Move o mouse
            pyautogui.moveTo(index_x, index_y)

            # Verifica se os dedos estão abaixados
            if middle_finger_tip.y > middle_finger_base.y:  # Dedo do meio abaixado
                pyautogui.click(button='right')  # Clique direito

            if index_finger_tip.y > index_finger_base.y and middle_finger_tip.y > middle_finger_base.y:  # Ambos os dedos abaixados
                pyautogui.click(button='left')  # Clique esquerdo

    # Exibe a imagem
    cv2.imshow('Mouse Virtual', frame)

    # Sai se a tecla 'q' for pressionada
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

# Libera os recursos
cap.release()
cv2.destroyAllWindows()
