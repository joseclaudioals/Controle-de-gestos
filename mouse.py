import cv2
import mediapipe as mp
import pyautogui

# Inicializando Mediapipe
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Inicializando webcam
cap = cv2.VideoCapture(0)

# Inicializando Mediapipe Hands
with mp_hands.Hands(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            continue

        # Converte a imagem para RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # Faz a detecção
        results = hands.process(image)

        # Converte a imagem de volta para BGR para exibir
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Extrai a posição da ponta do dedo indicador
                index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                height, width, _ = image.shape
                x, y = int(index_finger_tip.x * width), int(index_finger_tip.y * height)

                # Move o cursor do mouse
                pyautogui.moveTo(x, y)

                # Desenha as marcações na mão
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Exibe a imagem
        cv2.imshow('Hand Tracking', image)

        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
