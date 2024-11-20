import cv2
import mediapipe as mp
import numpy as np
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from math import hypot

# Inicializar MediaPipe e Pycaw
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Inicializar Pycaw para controle de volume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
vol_range = volume.GetVolumeRange()  # Obter intervalo de volume
min_vol, max_vol = vol_range[0], vol_range[1]

# Abrir a câmera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Flip horizontal para melhor interação
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Obter coordenadas dos pontos 4 (dedão) e 8 (indicador)
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            h, w, _ = frame.shape
            thumb_pos = (int(thumb_tip.x * w), int(thumb_tip.y * h))
            index_pos = (int(index_tip.x * w), int(index_tip.y * h))

            # Desenhar marcadores
            cv2.circle(frame, thumb_pos, 10, (255, 0, 0), -1)
            cv2.circle(frame, index_pos, 10, (255, 0, 0), -1)
            cv2.line(frame, thumb_pos, index_pos, (255, 255, 255), 2)

            # Calcular distância entre os dois dedos
            distance = hypot(index_pos[0] - thumb_pos[0], index_pos[1] - thumb_pos[1])

            # Converter distância para escala de volume
            vol = np.interp(distance, [30, 300], [min_vol, max_vol])
            volume.SetMasterVolumeLevel(vol, None)

            # Exibir informações na tela
            vol_bar = np.interp(distance, [30, 300], [400, 150])
            cv2.rectangle(frame, (50, 150), (85, 400), (0, 255, 0), 2)
            cv2.rectangle(frame, (50, int(vol_bar)), (85, 400), (0, 255, 0), -1)

            cv2.putText(frame, f'Volume: {int(np.interp(vol, [min_vol, max_vol], [0, 100]))}%', 
                        (40, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Controle de Volume por Gestos", frame)

    # Sair ao pressionar 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

