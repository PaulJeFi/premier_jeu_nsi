'''
IMPORTANT :

Pour ouvrir l'inventaire, tapez " a "
Pour le fermer c'est la même touche
Configurable dans la fonction main() en bas de ce script

Clique gauche pour sélectionner
Clique droit après avoir sélectionné un objet pour le changer de place

MERCI DE NE PAS MODIFIER SANS AUTORISATION SINON C'EST 0/20 !!!

Si vous avez besoin d'aide contactez votre chef de groupe préféré : Térence
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

base_stats = {"Spe" : 1, "Def" : 0, "Vie" : 100}
stats = {"Spe" : 1, "Def" : 0, "Vie" : 100}

class Inventaire() :
    '''L'inventaire du héro'''

    def __init__(self) :
        self.objet_selection = "" # L'objet sélectionné
        self.all_items = {"Bottes" : ["bottes", "description", ["Spe +0.1", "Def +10"]], # nom objet : [nom fichier png, description, stats]
            "Armure" : ["armure", "description", ["Spe -0.05", "Def +40"]],
            "Objet de type random" : ["objet_random", "description...", "stats"],
            "Un truc" : ["un_truc", "description", "stats"]}
        self.inventaire_done = False # NE PAS TOUCHER : permet d'attribuer des espaces d'inventaire vide
        self.ouvert = False # False = inventaire invisible ; True = inventaire visible
        self.can_switch = True # Si True on peut ouvrir/fermer l'inventaire
        self.o_image1 = pygame.image.load('./images/inventaire/case_doree.png') # Case jaune (objets équipés)
        self.o_image2 = pygame.image.load('./images/inventaire/case_sombre.png') # Case noir (inventaire)
        self.o_image3 = pygame.image.load('./images/inventaire/case_overlay.png') # Surbrillance
        self.o_image4 = pygame.image.load('./images/inventaire/case_selection.png') # Sélection
        self.actualiser_pos()

    def actualiser_pos(self) :
        '''Actualise l'agencement de l'inventaire'''
        self.size = 50
        self.image1 = pygame.transform.scale(self.o_image1, (self.size, self.size))
        self.image2 = pygame.transform.scale(self.o_image2, (self.size, self.size))
        self.image3 = pygame.transform.scale(self.o_image3, (self.size, self.size))
        self.image4 = pygame.transform.scale(self.o_image4, (self.size, self.size))
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
        objet_selection_pos = self.overlay()
        self.items_display()
        self.selection(objet_selection_pos)

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

    def overlay(self) :
        '''Permet de faire une petite surbrillance sur la case que l'on touche avec le curseur, ainsi que renvoie les informations de cette case'''
        mouse = pygame.mouse.get_pos()
        # Partie inventaire
        for i in range(0, len(self.positions2), 2) :
            if mouse[0] > self.positions2[i] and mouse[1] > self.positions2[i+1] and mouse[0] < self.positions2[i] + self.size and mouse[1] < self.positions2[i+1] + self.size :
                screen.blit(self.image3, (self.positions2[i], self.positions2[i+1]))
                return (self.positions2[i], self.positions2[i+1], self.objets_inventaire[i//2], i//2, "inventaire") # Position X et y de la case ainsi que l'objet contenu dans celle-ci
        # Partie équipement
        for i in range(0, len(self.positions1), 2) :
            if mouse[0] > self.positions1[i] and mouse[1] > self.positions1[i+1] and mouse[0] < self.positions1[i] + self.size and mouse[1] < self.positions1[i+1] + self.size :
                screen.blit(self.image3, (self.positions1[i], self.positions1[i+1]))
                return (self.positions1[i], self.positions1[i+1], self.objets[i//2], i//2, "equipement")

    def selection(self, infos) :
        if type(infos) == tuple and pygame.mouse.get_pressed()[0] : # Clique gauche
            screen.blit(self.image4, (infos[0], infos[1]))
            self.objet_selection = infos
        elif pygame.mouse.get_pressed()[0] :
            self.objet_selection = ""
        elif pygame.mouse.get_pressed()[2] : # Clique droit
            if type(infos) == tuple and self.objet_selection != "" :
                '''Permet d'échanger la position de 2 objets, en fonction de si ils sont dans l'inventaire ou dans les objets équipés'''
                # PS : ne pas oublier d'utiliser " self.objets_stats() "" pour actualiser les stats du héro. Pas besoin de le mettre pour le premier cas vu que l'on ne touche pas aux objets équipés
                if infos[4] == "inventaire" and self.objet_selection[4] == "inventaire" :
                    self.objets_inventaire[infos[3]], self.objets_inventaire[self.objet_selection[3]] = self.objets_inventaire[self.objet_selection[3]], self.objets_inventaire[infos[3]]
                elif infos[4] == "equipement" and self.objet_selection[4] == "inventaire" :
                    self.objets[infos[3]], self.objets_inventaire[self.objet_selection[3]] = self.objets_inventaire[self.objet_selection[3]], self.objets[infos[3]]
                    self.objets_stats()
                elif infos[4] == "equipement" and self.objet_selection[4] == "equipement" :
                    self.objets[infos[3]], self.objets[self.objet_selection[3]] = self.objets[self.objet_selection[3]], self.objets[infos[3]]
                    self.objets_stats()
                elif infos[4] == "inventaire" and self.objet_selection[4] == "equipement" :
                    self.objets_inventaire[infos[3]], self.objets[self.objet_selection[3]] = self.objets[self.objet_selection[3]], self.objets_inventaire[infos[3]]
                    self.objets_stats()
            self.objet_selection = ""
        elif self.objet_selection != "" :
            screen.blit(self.image4, (self.objet_selection[0], self.objet_selection[1]))

    def add_item(self, item) :
        for i in range(len(self.objets_inventaire)) :
            if self.objets_inventaire[i] == "" :
                self.objets_inventaire[i] = item
                return True
        return False

    def objets_stats(self) :
        new_stats = base_stats.copy()
        for i in self.objets :
            if i != "" :
                if i in self.all_items :
                    for j in range(len(self.all_items[i][2])) :
                        value = self.all_items[i][2][j].split()
                        new_stats[value[0]] += float(value[1])
        stats = new_stats.copy()
        print(stats, new_stats, base_stats)

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