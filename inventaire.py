import pygame
import sys

pygame.init()
WHITE = (255, 255, 255)

x, y = 1080, 720
screen = pygame.display.set_mode((x, y))
pygame.display.set_caption("Friends Royal")
pygame.display.set_icon(pygame.image.load('./images/personages/Humain_type_1.png').convert())
screen.fill(WHITE)
pygame.font.init()
myfont = pygame.font.SysFont('couriernewbold', 15)

def main() :
    '''Fonction principale'''
    while True : # False = le jeu s'arrête
        screen.fill(WHITE)
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                pygame.quit()
                sys.exit()
        pygame.display.flip()
        
if __name__ == '__main__' :
    main()