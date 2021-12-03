from main import Inventaire, Grass, Hero, Arme, Construct_munitions, Soin
import pygame
import functions
import zombies_new
import sys
import time

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
pygame.font.init()

def text(screen, font, size, string, color, pos) :
    '''Permet d'afficher un texte de façon simplifiée'''
    textsurface = pygame.font.Font(font, size).render(string, False, color)
    screen.blit(textsurface, pos)

def etape_1(Time=time.time()) :
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
        if time.time()-Time <= 5 :
            text(screen, './courriernewbold.ttf', 30, 'Bienvenue dans le camp d\'entrainement du jeu.', RED, (x/2-400, 100))
        else :
            if time.time()-Time >= 15 :
                return None
            text(screen, './courriernewbold.ttf', 30, 'Ici, vous apprendrez comment survivre efficacement', RED, (x/2-450, 100))
            text(screen, './courriernewbold.ttf', 30, 'face aux zombies.', RED, (x/2-150, 150))
        pygame.display.flip()

if __name__ == '__main__' :
    etape_1()