import pygame
import sys

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

class Grass() :
    def __init__(self) :
        self.size = 1105
        self.image = pygame.image.load('images/tuilles_de_terrain/Herbe.png')
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
        '''Bon c'est cette fonction qui pose problème. Elle doit refaire le pavage quand il n'y a plus d'herbe.'''
        if (Image[0] < -self.size) :
            Image[0] = 2*self.size
        elif (Image[0] > x) :
            Image[0] -= 2*self.size
        if (Image[1] < -self.size) :
            Image[1] = 2*self.size
        elif (Image[1] > y) :
            Image[1] -= 2*self.size
        return [Image[0], Image[1]]
        pass

def main() :
    grass = Grass()
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
        grass.display()
        pygame.display.flip()


if __name__ == '__main__' :
    main()