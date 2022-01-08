import pygame
import sys

x, y = 1080, 720 # dimensions de l'écran, en pixels
pygame.init()
pygame.mouse.set_visible(True)
screen = pygame.display.set_mode((x, y))
pygame.display.set_caption("The lessived")
pygame.display.set_icon(pygame.image.load('./images/Icone.png'))
screen.fill((255, 255, 255))


class Bouton() :
    '''Les boutons affichés à l'écran'''

    def __init__(self) :
        self.size_facteur = 64 # Facteur de taille
        self.size = (self.size_facteur*3, self.size_facteur) # Taille (format 3:1)
        self.all_boutons = {"Jouer" : [["Jouer", "Jouer_onclick"], (400, 200)]} # Toutes les images pour les boutons
        for cle in list(self.all_boutons.keys()) :
            for image in self.all_boutons[cle][0] :
                self.all_boutons[cle][0][self.all_boutons[cle][0].index(image)] = pygame.transform.scale(pygame.image.load(f"./images/menu/{image}.png"), self.size)

    def display(self) :
        '''Affichage'''
        mouse = pygame.mouse.get_pos()
        for cle in list(self.all_boutons.keys()) :
            if self.all_boutons[cle][1][0] < mouse[0] < self.all_boutons[cle][1][0] + self.size[0] and self.all_boutons[cle][1][1] < mouse[1] < self.all_boutons[cle][1][1] + self.size[1] :
                screen.blit(self.all_boutons[cle][0][1], self.all_boutons[cle][1]) # Si la souris est sur le bouton
            else :
                screen.blit(self.all_boutons[cle][0][0], self.all_boutons[cle][1]) # Si la souris n'est pas sur le bouton


def main() :

    while True : # False = le jeu s'arrête

        bouton = Bouton()

        screen.fill((255, 255, 255))

        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                pygame.quit()
                sys.exit()
        
        bouton.display()

        pygame.display.flip()

if __name__ == '__main__' :
    main()