import pygame
from main import Grass
import sys

pygame.init()
BLACK = (0, 0, 0)
GRAY = (20, 20, 20)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Les règlages de base (vitesse du joueur + set-up affichage + set-up frame-rate)
SPEED = 0.4 # Je pense qu'il faudrait le mêtre dans la classe héro dans   -->   def __init__(self):
x, y = 1080, 720
screen = pygame.display.set_mode((x, y))
pygame.display.set_caption("Friends Royal")
pygame.display.set_icon(pygame.image.load('./images/personages/Humain_type_1.png').convert())
screen.fill(WHITE)
clock = pygame.time.Clock()


class Zombies ():

    """ intialisation de classe : image, pv et taille """
    def __init__(self) :
       image = pygame.image.load('./images/personages/Zombie_type_1.png') 
       image = pygame.transform.scale(image, (100, 100))
       self.x = 0
       self.y = 0
       self.pos = [self.x, self.y]
       self.size = 100
       screen.blit(int(self.pos[0]-self.size[0]/2), int(self.pos[1]-self.size[1]/2))
       self.pv = 30
       self.pv_maxi = 30
       self.rotated = pygame.image.load('./images/personages/Zombie_type_1.png')

    def nbrPV (self) : 
        if self.pv > self.pv_maxi :
            self.pv = self.pv_maxi
        elif self.pv < 0 :
            self.pv = 0

    def spawn(self) :
        self.x = 0
        self.y = 0
        #self.spawn = image() # <------------ là j'ai pas compris
        self.spawn = (self.x, self.y)

    def deplacement (self) :
        if self.x > 540 and self.y > 360 :
            self.x += 2 
            self.y += 1
        if self.x < 540 and self.y < 360 :
            self.x -= 2 
            self.y -= 1

    def degatZomb (self) :
        if """ le zombie est touché """ :
            self.pv -= 10
    
def main() :
    '''Fonction principale'''
    grass = Grass()
    while True : # False = le jeu s'arrête
        dt = clock.tick(144) # IMPORTANT : FPS du jeu
        screen.fill(WHITE)
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                pygame.quit()
                sys.exit()
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP] or pressed[pygame.K_z] :
            grass.bas(dt)
        if pressed[pygame.K_DOWN] or pressed[pygame.K_s] :
            grass.haut(dt)
        if pressed[pygame.K_LEFT] or pressed[pygame.K_q] :
            grass.gauche(dt)
        if pressed[pygame.K_RIGHT] or pressed[pygame.K_d] :
            grass.droite(dt)
        # Affiche ton sprite ici.
        pygame.display.flip()

if __name__ == '__main__' :
    main()