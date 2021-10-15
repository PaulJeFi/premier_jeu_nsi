import pygame

pygame.init()
pygame.mouse.set_visible(False)

WHITE = (255, 255, 255)


SPEED = 10
x, y = 1080, 720
screen = pygame.display.set_mode((x, y))
pygame.display.set_caption("Friends Royal")
pygame.display.set_icon(pygame.image.load('./images/personages/Humain_type_1.png').convert())

image = pygame.image.load('./images/intro/intro.png').convert()

screen.blit(image, (0, 0))
for event in pygame.event.get() :
    pass
pygame.display.flip()