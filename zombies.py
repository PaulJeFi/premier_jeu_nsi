import pygame
from main import Grass, deplace, convert_degrees, convert_radians, collisions
import sys
import math
import time
import random

pygame.init()
BLACK = (0, 0, 0)
GRAY = (20, 20, 20)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Les règlages de base (vitesse du joueur + set-up affichage + set-up frame-rate)
x, y = 1080, 720
screen = pygame.display.set_mode((x, y))
pygame.display.set_caption("Friends Royal")
pygame.display.set_icon(pygame.image.load('./images/personages/Humain_type_1.png').convert())
screen.fill(WHITE)
clock = pygame.time.Clock()

class Zombies(deplace) :

    """ intialisation de classe : image, pv et taille """
    def __init__(self, type=1) :
        self.size = 100
        self.SPEED = 0.25
        self.image = pygame.image.load(f'./images/personages/Zombie_type_{type}.png') 
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.image = pygame.transform.rotate(self.image, 180)
        self.spawn()
        self.pos = [self.x, self.y]
        self.size = 100
        screen.blit(self.image, (int(self.pos[0]-self.size/2), int(self.pos[1]-self.size/2)))
        self.pv = 30
        self.pv_maxi = 30
        self.rotated = self.image
        self.angle = 0
        self.rect = self.image.get_rect()

    def nbrPV (self) : 
        if self.pv > self.pv_maxi :
            self.pv = self.pv_maxi
        elif self.pv < 0 :
            self.pv = 0

    def spawn(self) :
        '''Fait naître les Zombies par la grâce de Térence. N'oublions pas sa supériorité totale.'''
        def spawn_x(the_x) :
            '''Faut pas le dire à Mr Mandic...'''
            the_x = random.randint(-1*x, 2*x)
            if 0-self.size <= the_x <= x+self.size :
                the_x = spawn_x(the_x)
            return the_x
        def spawn_y(the_y=0) :
            '''Faut pas le dire à Mr Mandic...'''
            the_y = random.randint(-1*y, 2*y)
            if 0-self.size <= the_y <= y+self.size :
                the_y = spawn_y(the_y)
            return the_y
        self.x, self.y = spawn_x(self), spawn_y(self)

    def deplacement (self, dt) :
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
        self.x -= dt*self.SPEED * self.vect[0]
        if collisions(self, Construct_Zombies().zombies) :
            print("bruh x")
            self.x += dt*self.SPEED * self.vect[0]
        self.y -= dt*self.SPEED * self.vect[1]
        if collisions(self, Construct_Zombies().zombies) :
            print("bruh y")
            self.x += dt*self.SPEED * self.vect[0]
        #pygame.draw.line(screen, WHITE, (self.x, self.y), (self.x+self.vect[0], self.y+self.vect[1]))
        '''line(surface, color, start_pos, end_pos, width)'''

    def deplacement_inverse(self, dt):
        l = math.sqrt((self.x - x/2)**2 + (self.y - y/2)**2 )
        self.vect = [1/l * (self.x - x/2), 1/l * (self.y - y/2)]
        self.x += dt*self.SPEED * self.vect[0]
        self.y += dt*self.SPEED * self.vect[0]

    def degatZomb (self) :
        if """ le zombie est touché """ :
            self.pv -= 1
    
    def display(self, dt) :
        self.deplacement(dt)
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

class Construct_Zombies() :

    '''Cette classe permet de gérer un ensemble de zombies'''
    def __init__(self, number=10) :
        self.zombies = [Zombies(1) for i in range(number)]
        self.zombie = Zombies(1)
        self.groupe = pygame.sprite.Group()

    def __add__(self, num) :
        self.groupe.clear()
        for i in range(num) :
            self.zombies.append(Zombies())
            self.groupe.add(self.zombie)

    def display(self, dt) :
        for zomb in self.zombies :
            self.groupe.remove(zomb)
            if not collisions(zomb, self.groupe) :
                zomb.display(dt)
            self.groupe.add(zomb)

    def haut(self, dt) :
        for zomb in self.zombies :
            zomb.haut(dt)

    def bas(self, dt) :
        for zomb in self.zombies :
            zomb.bas(dt)

    def gauche(self, dt) :
        for zomb in self.zombies :
            zomb.gauche(dt)

    def droite(self, dt) :
        for zomb in self.zombies :
            zomb.droite(dt)
    

def main() :
    '''Fonction principale'''
    grass = Grass()
    zombies = Construct_Zombies()
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
            zombies.bas(dt)
        if pressed[pygame.K_DOWN] or pressed[pygame.K_s] :
            grass.haut(dt)
            zombies.haut(dt)
        if pressed[pygame.K_LEFT] or pressed[pygame.K_q] :
            grass.gauche(dt)
            zombies.gauche(dt)
        if pressed[pygame.K_RIGHT] or pressed[pygame.K_d] :
            grass.droite(dt)
            zombies.droite(dt)
        # Affiche ton sprite ici.
        grass.display()
        zombies.display(dt)
        pygame.display.flip()
        #zombies.zombies.append(Zombies(3))

if __name__ == '__main__' :
    main()

