import pygame

'''
Permettra d'afficher l'écran de chargement.
'''
pygame.init()
pygame.mouse.set_visible(False) # Pour ne pas voir la souris

# Initialisation de base :
x, y = 1080, 720
screen = pygame.display.set_mode((x, y))
pygame.display.set_caption("Friends Royal")
pygame.display.set_icon(pygame.image.load('./images/personages/Humain_type_1.png').convert())

image = pygame.image.load('./images/intro/intro.png').convert() # Image de chargement

screen.blit(image, (0, 0))
for event in pygame.event.get() : # sans ça, rien ne s'affiche
    pass
pygame.display.flip()