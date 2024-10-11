# sling_game.py
import pygame
import math

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

running = True
while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Simular gesto (substitua isso pelo movimento capturado pela câmera)
    # Neste exemplo, estamos simplesmente usando o mouse como controle
    if pygame.mouse.get_pressed()[0]:
        bird_pos = list(pygame.mouse.get_pos())
        pulling = True
    else:
        pulling = False

    draw_sling()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
