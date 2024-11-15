import cv2
from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Key, Controller

# Inicialize a captura de vídeo
video = cv2.VideoCapture(0)  # Use 0 para a webcam interna, 1 para a externa
video.set(3, 1280)
video.set(4, 720)

# Inicialize o controlador do teclado
kb = Controller()

# Inicialize o detector de mãos
detector = HandDetector(detectionCon=1)

# Carregar imagens das setas
setaDir = cv2.imread('seta dir.PNG')
setaEsq = cv2.imread('seta esq.PNG')

# Estado inicial dos dedos
estadoAtual = [0, 0, 0, 0, 0]

while True:
    success, img = video.read()
    if not success:
        break

    hands, img = detector.findHands(img)

    if hands:
        estado = detector.fingersUp(hands[0])

        if estado != estadoAtual and estado == [0, 0, 0, 0, 1]:
            print('Passar slide')
            kb.press(Key.right)
            kb.release(Key.right)

        elif estado != estadoAtual and estado == [0, 1, 0, 0, 0]:
            print('Voltar slide')
            kb.press(Key.left)
            kb.release(Key.left)

        # Mostrar seta na imagem se os dedos estiverem na mesma posição
        if estado == [0, 0, 0, 0, 1]:
            img[50:216, 984:1230] = setaDir
        elif estado == [1, 0, 0, 0, 0]:
            img[50:216, 50:296] = setaEsq

        # Atualizar o estado atual
        estadoAtual = estado

    # Mostrar imagem com setas
    cv2.imshow('img', cv2.resize(img, (640, 420)))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
