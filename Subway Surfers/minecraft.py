import cv2
from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Key, Controller

video = cv2.VideoCapture(0)
video.set(3, 1280)
video.set(4, 720)

kb = Controller()

detector = HandDetector(detectionCon=1)

estadoAtual = [0, 0, 0, 0, 0]

while True:
    success, img = video.read()
    if not success:
        break

    hands, img = detector.findHands(img)

    if hands:
        estado = detector.fingersUp(hands[0])

        if estado != estadoAtual and estado == [0, 0, 0, 0, 1]:
            print('andar para direita')
            kb.press(Key.right)
            kb.release(Key.right)

        elif estado != estadoAtual and estado == [0, 1, 0, 0, 0]:
            print('andar para esquerda')
            kb.press(Key.left)
            kb.release(Key.left)


        elif estado != estadoAtual and estado == [1, 0, 0, 0, 0]:
            print('rolar')
            kb.press(Key.down)
            kb.release(Key.down)

        elif estado != estadoAtual and estado == [1, 1, 1, 1, 1]:
            print('pular')
            kb.press(Key.up)
            kb.release(Key.up)


        estadoAtual = estado

    cv2.imshow('img', cv2.resize(img, (640, 420)))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
