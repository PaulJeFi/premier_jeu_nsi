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

class Inventaire() :

    def __init__(self) :
        self.ouvert = False # False = inventaire invisible ; True = inventaire visible
        self.base_cooldown = 50
        self.cooldown = self.base_cooldown
        self.size = 50
        self.image1 = pygame.image.load('./images/inventaire/case_doree.png')
        self.image1 = pygame.transform.scale(self.image1, (self.size, self.size))
        self.image2 = pygame.image.load('./images/inventaire/case_sombre.png')
        self.image2 = pygame.transform.scale(self.image2, (self.size, self.size))
        self.rect = self.image1.get_rect()
        self.positions1 = [] # x et y pour toutes les cases image1 sous la forme x1, y1, x2, y2, etc...
        self.positions2 = [] # x et y pour toutes les cases image2
        self.pos = [3, 2, 3, 5, 10] # Collonnes1, Lignes1, Collonnes2, Lignes2, Espacement
        for i in range(self.pos[0]) :
            for j in range(self.pos[1]) :
                self.positions1.append(x/2-(self.pos[1]*(self.size+self.pos[4]))+(j-1)*(self.size+self.pos[4]))
                self.positions1.append(y-(self.pos[0]*(self.size+self.pos[4]))+i*(self.size+self.pos[4]))
        for i in range(self.pos[2]) :
            for j in range(self.pos[3]) :
                self.positions2.append(x/2-(self.pos[1]*(self.size+self.pos[4]/2))+(self.pos[3]*(self.size+self.pos[4]))-(j-1)*(self.size+self.pos[4]))
                self.positions2.append(y-(self.pos[2]*(self.size+self.pos[4]))+i*(self.size+self.pos[4]))
        self.objets = ["No_item"]*self.pos[0]*self.pos[1] # Tu commences sans objets

    def display(self) :
        '''On affiche l'inventaire'''
        for i in range(0, len(self.positions1), 2) :
            screen.blit(self.image1, (self.positions1[i], self.positions1[i+1]))
        for i in range(0, len(self.positions2), 2) :
            screen.blit(self.image2, (self.positions2[i], self.positions2[i+1]))

def main() :
    '''Fonction principale'''
    inventaire = Inventaire()
    while True : # False = le jeu s'arrête
        screen.fill(WHITE)
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                pygame.quit()
                sys.exit()
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_a] :
            if inventaire.cooldown == inventaire.base_cooldown :
                inventaire.ouvert = not inventaire.ouvert
                inventaire.cooldown = 0
        elif inventaire.cooldown < inventaire.base_cooldown :
            inventaire.cooldown += 1
        if inventaire.ouvert :
            inventaire.display()
        pygame.display.flip()

if __name__ == '__main__' :
    main()