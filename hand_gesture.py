# hand_gesture.py
import cv2
import mediapipe as mp

# Inicializando MediaPipe para detecção de mãos
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)  # Captura de uma mão
mp_drawing = mp.solutions.drawing_utils

# Captura de vídeo (webcam)
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Falha ao capturar imagem")
        break

    # Converte a imagem para RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Processa a imagem e detecta mãos
    result = hands.process(image_rgb)

    # Desenhar as landmarks das mãos
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Exibir o vídeo com as landmarks
    cv2.imshow("Captura de Mãos", image)

    if cv2.waitKey(5) & 0xFF == 27:  # Fechar com ESC
        break

cap.release()
cv2.destroyAllWindows()
