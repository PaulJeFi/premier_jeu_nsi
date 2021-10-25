import pygame
from main import Grass, deplace, convert_degrees, convert_radians, SPEED
import sys
import math
import time

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


class Zombies(deplace) :

    """ intialisation de classe : image, pv et taille """
    def __init__(self) :
        self.size = 100
        self.image = pygame.image.load('./images/personages/Zombie_type_1.png') 
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.image = pygame.transform.rotate(self.image, 180)
        self.x = x/2-100
        self.y = y/2-100
        self.pos = [self.x, self.y]
        self.size = 100
        screen.blit(self.image, (int(self.pos[0]-self.size/2), int(self.pos[1]-self.size/2)))
        self.pv = 30
        self.pv_maxi = 30
        self.rotated = self.image
        self.angle = 0

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
        '''Le déplacement de l'IA'''
        #############################################
        # Old code d'Anatole. J'ai pas tout compris.#
        # if self.x > 540 and self.y > 360 :        #
        #    self.x += 2                            #
        #    self.y += 1                            #
        #if self.x < 540 and self.y < 360 :         #
        #    self.x -= 2                            #
        #    self.y -= 1                            #
        #############################################
        
        '''
        Un code naïf serait le suivant :

        if self.x > x/2 :
            self.x -= 1
        elif self.x < x/2 :
            self.x += 1
        if self.y > y/2 :
            self.y -= 1
        elif self.y < y/2 :
            self.y += 1
        
        Mais le problème est que le zombie ne se déplace pas DIRECTEMENT vers le
        centre, mais vers les axes centraux, donc au final vers le centre.
        If faut donc utiliser des VECTEURS.
        '''
        l = math.sqrt((self.x - x/2)**2 + (self.y - y/2)**2 )
        self.vect = [1/l * (self.x - x/2), 1/l * (self.y - y/2)]
        self.x -= SPEED * self.vect[0]
        self.y -= SPEED * self.vect[1]
        #pygame.draw.line(screen, WHITE, (self.x, self.y), (self.x+self.vect[0], self.y+self.vect[1]))
        '''line(surface, color, start_pos, end_pos, width)'''

    def degatZomb (self) :
        if """ le zombie est touché """ :
            self.pv -= 1
    
    def display(self) :
        self.deplacement()
        self.change()
        screen.blit(self.rotated, (self.x-self.size/2, self.y-self.size/2))

    def change(self) :
        '''Tourne le zombie pour qu'il ragarde le centre'''
        if self.x-x/2 != 0 :
            self.angle = math.atan((self.y-y/2)/(self.x-x/2))
            self.angle = convert_degrees(self.angle)
            if self.x < x/2 :
                self.angle = 180-self.angle
            else :
                self.angle = -self.angle
            self.rotated = pygame.transform.rotate(self.image, self.angle)

def main() :
    '''Fonction principale'''
    grass = Grass()
    zombie = Zombies()
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
            zombie.bas(dt)
        if pressed[pygame.K_DOWN] or pressed[pygame.K_s] :
            grass.haut(dt)
            zombie.haut(dt)
        if pressed[pygame.K_LEFT] or pressed[pygame.K_q] :
            grass.gauche(dt)
            zombie.gauche(dt)
        if pressed[pygame.K_RIGHT] or pressed[pygame.K_d] :
            grass.droite(dt)
            zombie.droite(dt)
        # Affiche ton sprite ici.
        grass.display()
        zombie.display()
        pygame.display.flip()
        print(zombie.x, zombie.y)

if __name__ == '__main__' :
    main()

