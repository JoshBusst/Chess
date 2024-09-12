import pygame
from time import sleep

pygame.init()
window = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()
points = [(50, 50), (400, 400)]

def draw(rect):
    window.fill(0)
    window.blit(image, rect)
    pygame.display.update()

def move_animate(image, pos1, pos2, dt=1, numPoints=20):
    direction = (pygame.math.Vector2(pos2) - pos1)/numPoints
    points = [pygame.math.Vector2(pos1) + i*direction for i in range(numPoints)]
    frameRate = int(numPoints/dt)

    for i in range(numPoints):
        clock.tick(frameRate)
        image_rect = image.get_rect(center = points[i])
        draw(image_rect)


image = pygame.image.load('images/bR.png').convert_alpha()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    move_animate(image, points[0], points[1], 0.4, 20)

    points.append(points[0])
    points.pop(0)
