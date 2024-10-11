# integrated_hand_gesture_sling.py
import cv2
import mediapipe as mp
import pygame
import math

# Inicializando MediaPipe para detecção de mãos
mp_hands = mp.solutions.hands
hands = mp_hands_gesture hands(max_num_hands=2)  # Captura de uma mão
mp_drawing = mp.solutions.drawing_utils

# Captura de vídeo (webcam)
cap = cv2.VideoCapture(0)

# Inicializando o Pygame
pygame.init()

# Configuração da janela
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Posição inicial do pássaro
bird_pos = [400, 300]
sling_origin = [400, 300]  # Origem do estilingue
pulling = False  # Variável para saber se o jogador está "puxando" o estilingue

# Função para desenhar o estilingue
def draw_sling():
    if pulling:
        pygame.draw.line(screen, (0, 0, 0), sling_origin, bird_pos, 5)
    pygame.draw.circle(screen, (255, 0, 0), bird_pos, 20)

# Função para processar a posição da mão
def process_hand_position(hand_landmarks):
    global bird_pos, pulling
    # Pegando as coordenadas do dedo indicador (landmark 8) e polegar (landmark 4)
    index_finger = hand_landmarks.landmark[8]
    thumb = hand_landmarks.landmark[4]

    # Convertendo as coordenadas normalizadas para coordenadas de tela
    bird_pos = [int(index_finger.x * 800), int(index_finger.y * 600)]

    # Calcular a distância entre polegar e indicador para simular o "puxar"
    distance = math.hypot(thumb.x - index_finger.x, thumb.y - index_finger.y)

    if distance > 0.1:  # Definindo um limite para considerar o "puxar"
        pulling = True
    else:
        pulling = False

# Loop principal
while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Falha ao capturar imagem")
        break

    # Converte a imagem para RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Processa a imagem e detecta mãos
    result = hands.process(image_rgb)

    # Pygame loop
    screen.fill((255, 255, 255))

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Processar a posição da mão para controle do jogo
            process_hand_position(hand_landmarks)

            # Desenhar as landmarks das mãos na janela da câmera
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Desenhar estilingue no Pygame
    draw_sling()

    # Exibir o vídeo com as landmarks
    cv2.imshow("Captura de Mãos", image)

    if cv2.waitKey(5) & 0xFF == 27:  # Fechar com ESC
        break

    pygame.display.flip()
    clock.tick(60)

cap.release()
cv2.destroyAllWindows()
pygame.quit()
