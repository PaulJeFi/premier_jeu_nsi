import pygame
import sys
import math

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

SPEED = 5
x, y = 1080, 720
screen = pygame.display.set_mode((x, y))
pygame.display.set_caption("Friends Royal")
pygame.display.set_icon(pygame.image.load('images/personages/Humain_type1.png').convert())
screen.fill(WHITE)

def convert_degrees(angle) :
    '''Convertit un angle en radians en degrés.'''
    return angle*180/math.pi

class Grass() :
    def __init__(self) :
        self.size = 1100
        self.image = pygame.image.load('images/tuilles_de_terrain/grass.png')
        self.image_1 = [0, 0]
        self.image_2 = [0, self.size]
        self.image_3 = [self.size, self.size]
        self.image_4 = [self.size, 0]
        self.image_5 = [self.size, -self.size]
        self.image_6 = [0, -self.size]
        self.image_7 = [-self.size, -self.size]
        self.image_8 = [-self.size, 0]
        self.image_9 = [-self.size, self.size]
        self.images = [self.image_1, self.image_2, self.image_3, self.image_4,
        self.image_5, self.image_6, self.image_7, self.image_8, self.image_9]
        for Image in self.images :
            screen.blit(self.image, (Image[0], Image[1]))

    def droite(self) :
        for Image in self.images :
            self.replacer(Image)
            Image[0] -= SPEED
    
    def haut(self) :
        for Image in self.images :
            self.replacer(Image)
            Image[1] -= SPEED

    def gauche(self) :
        for Image in self.images :
            self.replacer(Image)
            Image[0] += SPEED
    
    def bas(self) :
        for Image in self.images :
            self.replacer(Image)
            Image[1] += SPEED

    def display(self) :
        for Image in self.images :
            screen.blit(self.image, (Image[0], Image[1]))
    
    def replacer(self, Image) :
        '''Fonction du pavege de l'herbe.'''
        if Image[0] < -2*self.size :
            Image[0] = self.size
        elif Image[0] > 2*self.size :
            Image[0] = -self.size
        if Image[1] < -2*self.size :
            Image[1] = self.size
        elif Image[1] > 2*self.size :
            Image[1] = -self.size
        pass

class Hero() :
    def __init__(self) :
        self.image = pygame.image.load('images/personages/Humain_type1.png')
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.pv = 100
        self.angle = 90
        self.size = 150
        self.rotated = pygame.image.load('images/personages/Humain_type1.png')
    
    def display(self) :
        screen.blit(self.rotated, (x/2-self.size/2, y/2-self.size/2))

    def change(self, mousepos) :
        '''Tourne le perso pour qu'il ragarde la souris.'''
        if mousepos[0]-x/2 != 0 :
            self.angle = math.atan((mousepos[1]-y/2)/(mousepos[0]-x/2))
            self.angle = convert_degrees(self.angle)
            if mousepos[0] < x/2 :
                self.rotated = pygame.transform.rotate(self.image, 180-self.angle)
            else :
                self.rotated = pygame.transform.rotate(self.image, -self.angle)

def main() :
    grass = Grass()
    hero = Hero()
    while True :
        screen.fill(WHITE)
        for event in pygame.event.get() :
                    if event.type == pygame.QUIT :
                        pygame.quit()
                        sys.exit()
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP] or pressed[pygame.K_z] :
            grass.bas()
        if pressed[pygame.K_DOWN] or pressed[pygame.K_s] :
            grass.haut()
        if pressed[pygame.K_LEFT] or pressed[pygame.K_q] :
            grass.gauche()
        if pressed[pygame.K_RIGHT] or pressed[pygame.K_d] :
            grass.droite()
        hero.change(pygame.mouse.get_pos())
        grass.display()
        hero.display()
        pygame.display.flip()


if __name__ == '__main__' :
    main()