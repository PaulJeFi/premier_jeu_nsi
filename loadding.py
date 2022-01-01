import pygame

'''
Permettra d'afficher l'écran de chargement.
'''
pygame.init()
pygame.mouse.set_visible(False) # Pour ne pas voir la souris

# Initialisation de base :
x, y = 1080, 720
screen = pygame.display.set_mode((x, y))
pygame.display.set_caption("The lessived")
pygame.display.set_icon(pygame.image.load('./images/Icone.png').convert())
image = pygame.image.load('./images/intro/lessive.png').convert() # Image de chargement
image = pygame.transform.scale(image, (1080, 720))

screen.blit(image, (0, 0))
for event in pygame.event.get() : # sans ça, rien ne s'affiche
    pass
pygame.display.flip()