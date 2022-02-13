import pygame, sys

pygame.init()
size = width, height = 320, 240
speed = [0, 1]
black = 0, 0, 0

screen = pygame.display.set_mode(size)
ball = pygame.image.load('intro_ball.gif')
ballRect = ball.get_rect()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    ballRect = ballRect.move(speed)
    if ballRect.left < 0 or ballRect.right > width:
        speed[0] = -speed[0]
    if ballRect.top < 0 or ballRect.bottom > height:
        speed[1] = -speed[1]

    screen.fill('#eaeaea')
    screen.blit(ball, ballRect)
    pygame.display.update()