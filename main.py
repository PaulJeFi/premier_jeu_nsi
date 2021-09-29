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
            if self.not_in_screen(Image) :
                Image = self.replacer(Image)
            Image[0] -= SPEED
    
    def display(self) :
        for Image in self.images :
            screen.blit(self.image, (Image[0], Image[1]))
    
    def not_in_screen(Image) :
        pass
    def replacer(Image) :
        pass

while True :
    screen.fill(WHITE)
    pygame.display.flip()
    for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    pygame.quit()
                    sys.exit()