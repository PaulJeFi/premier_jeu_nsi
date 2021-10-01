import pygame
import sys
import math
import random

pygame.init()
pygame.mouse.set_visible(False)
'''pygame.cursors.arrow
pygame.cursors.diamond
pygame.cursors.broken_x
pygame.cursors.tri_left
pygame.cursors.tri_right'''
#pygame.mouse.set_cursor(pygame.cursors.arrow)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


SPEED = 4
x, y = 1080, 720
screen = pygame.display.set_mode((x, y))
pygame.display.set_caption("Friends Royal")
pygame.display.set_icon(pygame.image.load('images/personages/Humain_type_1.png').convert())
screen.fill(WHITE)


def curseur() :
    pos = pygame.mouse.get_pos()
    size = (30, 30)
    image = pygame.image.load('images/curseur/croix.png')
    image = pygame.transform.scale(image,(size[0], size[1]))
    screen.blit(image, (int(pos[0]-size[0]/2), int(pos[1]-size[1]/2)))

def convert_degrees(angle) :
    '''Convertit un angle en radians en degrés.'''
    return angle*180/math.pi

def convert_radians(angle) :
    '''Convertit un angle en degrés en radians.'''
    return angle*math.pi/180

def draw_rect(position, size, color) :
	'''Permet de tracer un rectangle'''
	pygame.draw.rect(screen, color, (position[0], position[1], size[0], size[1]))

class Score_actuel() :
    def __init__(self) :
        self.score = 0
        self.niveau = 1
        self.points = 0
        self.score += self.points
        if self.points != 0 :
            self.points = 0
        self.b_image = pygame.image.load('images/autres/Brouillard_V2.png')
        self.b_size_x = 1080+4240//self.niveau
        self.b_size_y = 720+2480//self.niveau
        self.b_image = self.b_image = pygame.transform.scale(self.b_image,(self.b_size_x,self.b_size_y))
        self.rect = self.b_image.get_rect()
        self.rect.x = (1080-self.b_size_x)/2
        self.rect.y = (720-self.b_size_y)/2
        if self.score//(1000*self.niveau) >= self.niveau :
            self.niveau = self.score//(1000*self.niveau)
        
    def display(self) :
        screen.blit(self.b_image, self.rect)
    
    def add(self, score) :
        self.score += score

class Grass() :
    def __init__(self) :
        self.size = 1600
        self.image = pygame.image.load('images/tuilles_de_terrain/Herbe_V2.png')
        self.image = self.image = pygame.transform.scale(self.image,(self.size+SPEED,self.size+SPEED))
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
        self.x = x/2
        self.y = (y/2)+100
        self.arme = Arme()
        self.image = pygame.image.load('images/personages/Humain_type_1.png')
        self.size = 100
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.pv = 100
        self.angle = 90
        self.rotated = pygame.image.load('images/personages/Humain_type_1.png')
    
    def display(self) :
        draw_rect((50, 50), (200, 50), BLACK)
        draw_rect((55, 55), (200-10, 50-10), RED)
        draw_rect((55, 55), (int((200-10)*(self.pv/100)), 50-10), GREEN)
        screen.blit(self.rotated, (x/2-self.size/2, y/2-self.size/2))
        self.arme.display()

    def change(self, mousepos) :
        '''Tourne le perso pour qu'il ragarde la souris.'''
        if mousepos[0]-x/2 != 0 :
            self.angle = math.atan((mousepos[1]-y/2)/(mousepos[0]-x/2))
            self.angle = convert_degrees(self.angle)
            if mousepos[0] < x/2 :
                self.angle = 180-self.angle
            else :
                self.angle = -self.angle
            self.rotated = pygame.transform.rotate(self.image, self.angle)
            self.arme.rotate(self.angle)

    def get_rect(self) :
        return pygame.Rect(self.x, self.y, self.size, self.size)

class Soin() :
    def __init__(self) :
        self.x, self.y = random.randint(0, x), random.randint(0, y)
        self.image = pygame.image.load('images/objets/Pack de soin.png')
        self.size = (50, 50)
        self.image = pygame.transform.scale(self.image, self.size)
    
    def droite(self) :
        self.x -= SPEED
    
    def haut(self) :
        self.y -= SPEED

    def gauche(self) :
        self.x += SPEED
    
    def bas(self) :
        self.y += SPEED

    def replace(self) :
        if (self.x+self.size[0] < 0) or (self.x > x) or (self.y+self.size[1] < 0) or (self.y > y) :
            self.x, self.y = random.randint(0, x), random.randint(0, y)

    def display(self) :
        self.replace()
        screen.blit(self.image, (self.x, self.y))

    def get_rect(self) :
        return pygame.Rect(self.x, self.y, *self.size)

    def touch_hero(self, hero) :
        if self.get_rect().colliderect(hero.get_rect()) :
            return True
        print(False)

class Arme() :
    def __init__(self) :
        # taille = 1105 x 682
        self.image = pygame.image.load('images/armes/Mitraillette/Mitraillette_frame1.png')
        self.size = [1105/8, 682/8]
        self.image = pygame.transform.scale(self.image, (int(self.size[0]), int(self.size[1])))
        self.rotated = pygame.image.load('images/armes/Mitraillette/Mitraillette_frame1.png')
    
    def display(self) :
        screen.blit(self.rotated, (int(self.x/2-self.size[0]/2), int(self.y/2-self.size[1]/2)))
    
    def rotate(self, angle) :
        self.rotated = pygame.transform.rotate(self.image, angle)
        self.x = (x)+math.sin(convert_radians(angle))*100+50
        self.y = (y)+math.cos(convert_radians(angle))*100-10
        

def main() :
    grass = Grass()
    hero = Hero()
    score = Score_actuel()
    soin = Soin()
    while True :
        screen.fill(WHITE)
        for event in pygame.event.get() :
                    if event.type == pygame.QUIT :
                        pygame.quit()
                        sys.exit()
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP] or pressed[pygame.K_z] :
            grass.bas()
            soin.bas()
        if pressed[pygame.K_DOWN] or pressed[pygame.K_s] :
            grass.haut()
            soin.haut()
        if pressed[pygame.K_LEFT] or pressed[pygame.K_q] :
            grass.gauche()
            soin.gauche()
        if pressed[pygame.K_RIGHT] or pressed[pygame.K_d] :
            grass.droite()
            soin.droite()
        if soin.touch_hero(hero) :
            print("Yeah")
        hero.change(pygame.mouse.get_pos())
        grass.display()
        soin.display()
        hero.display()
        score.display()
        curseur()
        pygame.display.flip()


if __name__ == '__main__' :
    main()