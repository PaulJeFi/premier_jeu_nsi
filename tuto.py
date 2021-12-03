from main import Inventaire, Grass, Hero, Arme, Construct_munitions, Soin
import pygame
import functions
import zombies_new
import sys

# Définition de certaines couleurs
BLACK = (0, 0, 0)
GRAY = (20, 20, 20)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Initialisation de Pygame
x, y = 1080, 720 # dimensions de l'écran, en pixels
pygame.init()
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode((x, y))
pygame.display.set_caption("Friends Royal")
pygame.display.set_icon(pygame.image.load('./images/personages/Humain_type_1.png').convert())
screen.fill(WHITE)
clock = pygame.time.Clock()

def etape_1() :
    '''Fonction principale'''
    inventaire = Inventaire()
    grass = Grass()
    hero = Hero()
    arme = Arme()
    balles = Construct_munitions()
    while True : # False = le jeu s'arrête
        dt = clock.tick(144) # IMPORTANT : FPS du jeu
        screen.fill(WHITE)
        balles.weapon_stats_update(arme.arme_en_main)
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                pygame.quit()
                sys.exit()
            if event :
                balles.add(1000)
        arme.change(((1+x/2, 0)))
        grass.display()
        balles.display(dt, True, 1000)
        hero.display()
        arme.display()
        hero.GUI_display()
        pygame.display.flip()

if __name__ == '__main__' :
    etape_1()