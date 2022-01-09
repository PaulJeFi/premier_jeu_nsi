import pygame
import sys
import main, intro, tuto # Les scripts à importer

x, y = 1080, 720 # dimensions de l'écran, en pixels
pygame.init()
pygame.mouse.set_visible(True)
screen = pygame.display.set_mode((x, y))
pygame.display.set_caption("The lessived")
pygame.display.set_icon(pygame.image.load('./images/Icone.png'))
screen.fill((255, 255, 255))

lessived = pygame.image.load('./images/lessived.png')
lessived = pygame.transform.scale(lessived, (x, y))


class Bouton() :
    '''Les boutons affichés à l'écran'''

    def __init__(self) :
        self.size_facteur = 64 # Facteur de taille
        self.size = (self.size_facteur*3, self.size_facteur) # Taille (format 3:1)
        # Ci-dessous, toutes les images pour les boutons (Nom du bouton : [[image, image onclick], (coordonées x et y)])
        middle = (x - self.size[0]) / 2
        self.all_boutons = {
            "Jouer" : [["Jouer", "Jouer_onclick"], (middle, 200)],
            "Tutoriel" : [["Tutoriel", "Tutoriel_onclick"], (middle, 300)],
            "Quiter" : [["Quiter", "Quiter_onclick"], (middle, 400)]
            }
        # Chargement des images
        for cle in list(self.all_boutons.keys()) :
            for image in self.all_boutons[cle][0] :
                self.all_boutons[cle][0][self.all_boutons[cle][0].index(image)] = pygame.transform.scale(pygame.image.load(f"./images/menu/{image}.png"), self.size)

    def display(self) :
        '''Affichage'''
        mouse = pygame.mouse.get_pos()
        bouton_selectionne = "Menu" # Permet de savoir quel bouton est sélectionné ("menu" = pas de bouton sélectionné)
        for cle in list(self.all_boutons.keys()) :
            if self.all_boutons[cle][1][0] < mouse[0] < self.all_boutons[cle][1][0] + self.size[0] and self.all_boutons[cle][1][1] < mouse[1] < self.all_boutons[cle][1][1] + self.size[1] :
                screen.blit(self.all_boutons[cle][0][1], self.all_boutons[cle][1]) # Si la souris est sur le bouton
                bouton_selectionne = cle
            else :
                screen.blit(self.all_boutons[cle][0][0], self.all_boutons[cle][1]) # Si la souris n'est pas sur le bouton
        return bouton_selectionne

def jeu() :
    '''Fonction permettant d'exécuter le jeu proprement'''
    pygame.mouse.set_visible(False)
    intro.main()
    play = True
    while play :
        play = main.main()
    pygame.mouse.set_visible(True)

def menu() :
    '''Le menu principal du jeu'''

    operation_selectionnee = "Menu" # Permet de savoir que faire lorsque le joueur clique ("menu" est la valeur par défaut et ne fait rien)
    clique = False # Permet de savoir si le joueur à cliqué
    # Liste des opérations à effectuer (ne pas entrer n'importe quoi ou il va y avoir de gros problèmes)
    liste_operations = {
        "Menu" : "None",
        "Jouer" : "jeu()",
        "Tutoriel" : "pygame.mouse.set_visible(False), tuto.main(), pygame.mouse.set_visible(True)",
        "Quiter" : "pygame.quit(), sys.exit()"
        }

    while True : # False = le jeu s'arrête

        bouton = Bouton()

        screen.fill((255, 255, 255)) # Background
        screen.blit(lessived, (0, 0))

        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                pygame.quit()
                sys.exit()
        
            if event.type == pygame.MOUSEBUTTONDOWN : # Clique
                clique = True
            else :
                clique = False

        operation_selectionnee = bouton.display() # Display + attribution d'une valeur à une variable

        if clique : # Lorsque le joueur clique
            eval(liste_operations[operation_selectionnee]) # Je sais que éval c'est dangereux mais ici tout est sous contrôle
            clique = False
            operation_selectionnee = "Menu"

        pygame.display.flip()

if __name__ == '__main__' :
    menu()