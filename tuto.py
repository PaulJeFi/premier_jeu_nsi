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
    grass = Grass()
    hero = Hero()
    arme = Arme()
    while True : # False = le jeu s'arrête
        dt = clock.tick(144) # IMPORTANT : FPS du jeu
        screen.fill(WHITE)
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                pygame.quit()
                sys.exit()
        if arme.weapon_equiped != arme.previous_weapon_equiped :
                arme.previous_weapon_equiped = arme.weapon_equiped
                arme.actualiser()
        arme.change(((1+x/2, 0)))
        grass.display()
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

def etape_2(Time=time.time()) :
    '''Fonction principale'''
    inventaire = Inventaire()
    grass = Grass()
    hero = Hero()
    arme = Arme()
    balles = Construct_munitions()
    zombie = zombies_new.Zombies()
    zombie.x = x-100
    zombie.y = y/2
    zombie.SPEED = 0.05
    while True : # False = le jeu s'arrête
        dt = clock.tick(144) # IMPORTANT : FPS du jeu
        screen.fill(WHITE)
        if arme.weapon_equiped != arme.previous_weapon_equiped :
                arme.previous_weapon_equiped = arme.weapon_equiped
                balles.weapon_stats_update(arme.actualiser())
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                pygame.quit()
                sys.exit()
        '''
            if event :
                balles.add(1000)
        '''
        arme.change(((1+x/2, 0)))
        grass.display()
        balles.display(dt, True, 1000)
        zombie.display(dt, True, 0)
        hero.display()
        arme.display()
        hero.GUI_display()
        if time.time()-Time <= 5 :
            text(screen, './courriernewbold.ttf', 30, 'Voici le premier zombie du jeu. Attention !', RED, (x/2-400, 100))
            zombie.x = x-100
            zombie.y = y/2
        else :
            if time.time()-Time >= 12 :
                return (zombie.x, zombie.y)
            text(screen, './courriernewbold.ttf', 30, 'Comme vous le voyez, il a l\'air peu sympatique.', RED, (x/2-450, 100))
            text(screen, './courriernewbold.ttf', 30, 'Attention, il se dirige vers vous.', RED, (x/2-300, 150))
            text(screen, './courriernewbold.ttf', 30, 'Voyons ce qu\'il vous veut !', RED, (x/2-200, 200))
        pygame.display.flip()

def etape3(zomb_coord, Time=time.time()) :
    grass = Grass()
    hero = Hero()
    arme = Arme()
    arme.actualiser()
    zombie = zombies_new.Zombies()
    zombie.x = zomb_coord[0]
    zombie.y = zomb_coord[1]
    zombie.SPEED = 0.05
    while True : # False = le jeu s'arrête
        dt = clock.tick(144) # IMPORTANT : FPS du jeu
        screen.fill(WHITE)
        if arme.weapon_equiped != arme.previous_weapon_equiped :
                arme.previous_weapon_equiped = arme.weapon_equiped
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                pygame.quit()
                sys.exit()

        pressed = pygame.key.get_pressed()
        # Ajustement de la valleur de la vitesse du joueur afin qu'il se déplace aussi vite en diagonal qu'en ligne droite
        if pressed[pygame.K_z] and pressed[pygame.K_q] or pressed[pygame.K_z] and pressed[pygame.K_d] or pressed[pygame.K_s] and pressed[pygame.K_q] or pressed[pygame.K_s] and pressed[pygame.K_d] or pressed[pygame.K_UP] and pressed[pygame.K_LEFT] or pressed[pygame.K_UP] and pressed[pygame.K_RIGHT] or pressed[pygame.K_DOWN] and pressed[pygame.K_LEFT] or pressed[pygame.K_DOWN] and pressed[pygame.K_RIGHT] :
                speed_hero = ((2)**1/2)/2*dt
        else :
            speed_hero = dt


        if pressed[pygame.K_UP] or pressed[pygame.K_z] :
            grass.bas(speed_hero)
            zombie.bas(speed_hero)

        if pressed[pygame.K_DOWN] or pressed[pygame.K_s] :
            grass.haut(speed_hero)
            zombie.haut(speed_hero)

        if pressed[pygame.K_LEFT] or pressed[pygame.K_q] :
            grass.gauche(speed_hero)
            zombie.gauche(speed_hero)

        if pressed[pygame.K_RIGHT] or pressed[pygame.K_d] :
            grass.droite(speed_hero)
            zombie.droite(speed_hero)

        arme.change(((1+x/2, 0)))
        grass.display()
        zombie.display(dt, True, 0)
        hero.display()
        arme.display()
        hero.GUI_display()

        text(screen, './courriernewbold.ttf', 30, '         Utilisez ZQSD pour vous déplacer.', RED, (x/2-450, 100))
        text(screen, './courriernewbold.ttf', 30, 'Attention, le zombie vous attaque.', RED, (x/2-300, 150))
        pygame.display.flip()


if __name__ == '__main__' :
    # Etape n°1
    etape_1()
    # Actualisation de l'arme
    arme = Arme()
    arme.previous_weapon_equiped = None
    # Etape n°2
    zomb = etape_2(time.time())
    # Actualisation de l'arme
    arme = Arme()
    arme.previous_weapon_equiped = None
    # Etape n°3
    etape3(zomb, time.time())