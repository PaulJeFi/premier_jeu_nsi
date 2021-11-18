'''
IMPORTANT :
Pour ouvrir l'inventaire, tapez " a "
Pour le fermer c'est la même touche
Configurable dans la fonction main() en bas de ce script
ET MERCI DE NE PAS MODIFIER SANS AUTORISATION
Si vous avez besoin d'aide contactez votre chef de groupe
'''

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
    '''L'inventaire du héro'''

    def __init__(self) :
        self.all_items = {"Bottes" : ["Bottes", "description", "stats"], # nom objet : [nom fichier png, description, stats]
            "Armure" : ["Armure", "description", "stats"],
            "Objet de type random" : ["objet_random", "description...", "stats"],
            "Un truc" : ["un_truc", "description", "stats"]}
        self.inventaire_done = False # NE PAS TOUCHER : permet d'attribuer des espaces d'inventaire vide
        self.ouvert = False # False = inventaire invisible ; True = inventaire visible
        self.can_switch = True # Si True on peut ouvrir/fermer l'inventaire
        self.o_image1 = pygame.image.load('./images/inventaire/case_doree.png') # Case jaune (objets équipés)
        self.o_image2 = pygame.image.load('./images/inventaire/case_sombre.png') # Case noir (inventaire)
        self.actualiser_pos()

    def actualiser_pos(self) :
        '''Actualise l'agencement de l'inventaire'''
        self.size = 50
        self.image1 = pygame.transform.scale(self.o_image1, (self.size, self.size))
        self.image2 = pygame.transform.scale(self.o_image2, (self.size, self.size))
        self.rect = self.image1.get_rect()
        self.positions1 = [] # x et y pour toutes les cases image1 sous la forme x1, y1, x2, y2, etc...
        self.positions2 = [] # x et y pour toutes les cases image2
        # les valeurs 0 à 3 de self.pos permettent de règler la taille de l'inventaire
        self.pos = [3, 2, 3, 7, self.size/5] # Lignes1, Collonnes1, Lignes2, Collonnes2, Espacement ( puis posX, posY )
        self.pos.append((x-(self.pos[1]+self.pos[3]-1)*(self.size+self.pos[4]))/2) # Calcul posX
        self.pos.append(y-self.pos[0]*(self.size+self.pos[4])) # Calcul posY
        for i in range(self.pos[0]) : # Equation pour placer les cases
            for j in range(self.pos[1]) :
                self.positions1.append(self.pos[5]+(j-1)*(self.size+self.pos[4]))
                self.positions1.append(self.pos[6]+i*(self.size+self.pos[4]))
        for i in range(self.pos[2]) : # Même chose mais avec d'autres cases
            for j in range(self.pos[3]) :
                self.positions2.append(self.pos[5]+(j+self.pos[1])*(self.size+self.pos[4]))
                self.positions2.append(self.pos[6]+i*(self.size+self.pos[4]))
        if not self.inventaire_done : # Création de la liste contenant l'équipement et l'inventaire
            self.objets = [""]*(self.pos[0]*self.pos[1]-1)
            self.objets_inventaire = [""]*(self.pos[2]*self.pos[3])
            # Merci d'appeller les objet par leur nom de clé et si il ne doit pas avoir d'objet à un emplacement mettre simplement ""
            self.objets = ["", "Armure", "Bottes", "Bottes", "Bottes", ""] # TEST : Customisez l'équipement (attention à ne pas faire un "index out of range")
            self.objets_inventaire = ["Armure", "", "", "", "Bottes", "Armure", "",
                "", "", "Bottes", "Armure", "", "", "",
                "Bottes", "Armure", "", "", "", "Bottes", "Armure"] # TEST : Customisez l'inventaire (attention à ne pas faire un "index out of range")
            self.inventaire_done = True # Pour ne pas reset l'inventaire en permanance

    def display(self) :
        '''On affiche l'inventaire'''
        for i in range(0, len(self.positions1), 2) :
            screen.blit(self.image1, (self.positions1[i], self.positions1[i+1]))
        for i in range(0, len(self.positions2), 2) :
            screen.blit(self.image2, (self.positions2[i], self.positions2[i+1]))
        self.items_display()

    def items_display(self) :
        '''Affichage des objets dans l'inventaire'''
        for index in range(len(self.objets)) :
            if self.objets[index] != "" : # Si nom de l'objet == "", ça veut dire que ce n'est pas un objet, et ça permet d'éviter de laisser le script prendre du temps à le chercher
                if self.objets[index] in self.all_items :
                    screen.blit(pygame.transform.scale(pygame.image.load(f'./images/inventaire/{self.all_items[self.objets[index]][0]}.png'), (self.size, self.size)), (self.positions1[index*2], self.positions1[index*2+1]))
        for index in range(len(self.objets_inventaire)) :
            if self.objets_inventaire[index] != "" : # Si nom de l'objet == "", ça veut dire que ce n'est pas un objet, et ça permet d'éviter de laisser le script prendre du temps à le chercher
                if self.objets_inventaire[index] in self.all_items :
                    screen.blit(pygame.transform.scale(pygame.image.load(f'./images/inventaire/{self.all_items[self.objets_inventaire[index]][0]}.png'), (self.size, self.size)), (self.positions2[index*2], self.positions2[index*2+1]))

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
        # Ci-dessous le petit code qui permet de dire au script s'il doit afficher ou non l'inventaire
        if pressed[pygame.K_a] :
            if inventaire.can_switch :
                inventaire.ouvert = not inventaire.ouvert
                inventaire.can_switch = False
        elif not inventaire.can_switch :
            inventaire.can_switch = True
        if inventaire.ouvert :
            inventaire.display() # Affichage
        pygame.display.flip()

if __name__ == '__main__' :
    main()