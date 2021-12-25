'''
IMPORTANT :

Pour ouvrir l'inventaire, tapez " a "
Pour le fermer c'est la même touche
Pour obtenir un item aléatoire, tapez " e "
Configurable dans la fonction main() en bas de ce script

Clic gauche pour sélectionner
Clic droit après avoir sélectionné un objet pour le changer de place

MERCI DE NE PAS MODIFIER SANS AUTORISATION SINON C'EST 0/20 !!!
# Oui bien sûr ^^.

Si vous avez besoin d'aide contactez votre chef de groupe préféré : Térence

Si vous voulez créer votre propre objet merci de vous référer au script liste_objets.py
'''

from random import choice
import pygame
import sys
from functions import text
from liste_objets import definition_de_tous_les_objets, stats_de_base

# Constantes des couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

# Initialisation de pygame
pygame.init()
x, y = 1080, 720
screen = pygame.display.set_mode((x, y))
pygame.display.set_caption("Friends Royal")
pygame.display.set_icon(pygame.image.load('./images/personages/Humain_type_1.png').convert())
screen.fill(WHITE)
pygame.font.init()

class Inventaire() :
    '''L'inventaire du héro'''

    def __init__(self) :
        self.size_del = 32 # Taille du bouton "suprimer" et "équiper"
        self.affichage = 0
        self.base_stats = stats_de_base # Stats de base du héro
        self.stats = self.base_stats.copy() # Stats actuelles du héro
        self.objet_selection = "" # L'objet sélectionné
        self.all_items = definition_de_tous_les_objets # Liste de tous les objets du jeu, ainsi que leur nom, description et stats
        self.all_items_name = list(self.all_items.keys()) # Permet de faire une liste d'objets avec seulement leurs noms
        self.inventaire_done = False # NE PAS TOUCHER : permet d'attribuer des espaces d'inventaire vide
        self.ouvert = False # False = inventaire invisible ; True = inventaire visible
        self.can_switch = True # Si True on peut ouvrir/fermer l'inventaire
        self.o_image1 = pygame.image.load('./images/inventaire/case_doree.png') # Case jaune (objets équipés)
        self.o_image2 = pygame.image.load('./images/inventaire/case_sombre.png') # Case noire (inventaire)
        self.o_image3 = pygame.image.load('./images/inventaire/case_overlay.png') # Surbrillance
        self.o_image4 = pygame.image.load('./images/inventaire/case_selection.png') # Sélection (contour orange)
        self.o_image5 = pygame.image.load('./images/inventaire/case_description.png') # Panel sur lequel on affiche les informations de l'objet
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
            self.objets = [""]*(self.pos[0]*self.pos[1])
            self.objets_inventaire = [""]*(self.pos[2]*self.pos[3])
            self.objets_stats()
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
        self.description()

    def items_display(self) :
        '''Affichage des objets dans l'inventaire'''
        for index in range(len(self.objets)) :
            if self.objets[index] != "" : # Si nom de l'objet == "", ça veut dire que ce n'est pas un objet, et ça permet d'éviter de laisser le script prendre du temps à le chercher
                if self.objets[index] in self.all_items :
                    screen.blit(pygame.transform.scale(pygame.image.load(f'./images/inventaire/objets/{self.all_items[self.objets[index]][0]}.png'), (self.size, self.size)), (self.positions1[index*2], self.positions1[index*2+1]))
        for index in range(len(self.objets_inventaire)) :
            if self.objets_inventaire[index] != "" : # Si nom de l'objet == "", ça veut dire que ce n'est pas un objet, et ça permet d'éviter de laisser le script prendre du temps à le chercher
                if self.objets_inventaire[index] in self.all_items :
                    screen.blit(pygame.transform.scale(pygame.image.load(f'./images/inventaire/objets/{self.all_items[self.objets_inventaire[index]][0]}.png'), (self.size, self.size)), (self.positions2[index*2], self.positions2[index*2+1]))

    def overlay(self) :
        '''Permet de faire une petite surbrillance sur la case que l'on touche avec le curseur, ainsi que renvoyer les informations de cette case'''
        mouse = pygame.mouse.get_pos()
        # Partie inventaire
        for i in range(0, len(self.positions2), 2) :
            if mouse[0] > self.positions2[i] and mouse[1] > self.positions2[i+1] and mouse[0] < self.positions2[i] + self.size and mouse[1] < self.positions2[i+1] + self.size :
                screen.blit(self.image3, (self.positions2[i], self.positions2[i+1]))
                return (self.positions2[i], self.positions2[i+1], self.objets_inventaire[i//2], i//2, "inventaire") # Position X et y de la case ainsi que l'objet contenu dans celle-ci et le numéro de la case
        # Partie équipement
        for i in range(0, len(self.positions1), 2) :
            if mouse[0] > self.positions1[i] and mouse[1] > self.positions1[i+1] and mouse[0] < self.positions1[i] + self.size and mouse[1] < self.positions1[i+1] + self.size :
                screen.blit(self.image3, (self.positions1[i], self.positions1[i+1]))
                return (self.positions1[i], self.positions1[i+1], self.objets[i//2], i//2, "equipement")

    def selection(self, infos) :
        self.mouse = pygame.mouse.get_pos()
        if type(infos) == tuple and pygame.mouse.get_pressed()[0] : # Clic gauche
            screen.blit(self.image4, (infos[0], infos[1]))
            self.objet_selection = infos
        elif pygame.mouse.get_pressed()[0] and not(self.mouse[0] < x-14 and self.mouse[0] > x-2*self.size_del-20 and self.mouse[1] < y-14 and self.mouse[1] > y-self.size_del-14) :
            self.objet_selection = ""
        elif pygame.mouse.get_pressed()[2] : # Clic droit
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
        '''Ajoute un objet dans l'inventaire'''
        if item != "" :
            for i in range(len(self.objets_inventaire)) :
                if self.objets_inventaire[i] == "" :
                    self.affichage = 200
                    self.item = item
                    self.inventaire_plein = False
                    self.objet_trouve()
                    self.objets_inventaire[i] = item
                    return True
            self.affichage = 200
            self.inventaire_plein = True
            self.objet_trouve()
            return False

    def objet_trouve(self) :
        self.affichage -= 2
        if not self.inventaire_plein :
            self.text2(screen, "./FreeSansBold.ttf", 20, f'Vous avez obtenu {self.item} !', (255, 255, 255-self.affichage), (x/2-len(f'Vous avez obtenu {self.item} !')*5, 500+self.affichage))
        else :
            self.text2(screen, "./FreeSansBold.ttf", 20, 'Votre inventaire est plein !', (255, 155-self.affichage/2, 155-self.affichage/2), (x/2-len('Votre inventaire est plein !')*5, 500+self.affichage))

    def objets_stats(self) :
        '''Réactualise les stats données par les objets équipés'''
        new_stats = self.base_stats.copy()
        for i in self.objets :
            if i != "" :
                if i in self.all_items :
                    for j in range(len(self.all_items[i][2])) :
                        value = self.all_items[i][2][j].split()
                        new_stats[value[0]] += float(value[1])
        self.stats = new_stats.copy()

    def text2(self, screen, font, size, string, color, pos) :
        '''Permet d'afficher un texte de façon simplifiée'''
        textsurface = pygame.font.Font(font, size).render(string, False, color)
        screen.blit(textsurface, pos)

    def stats_display(self) :
        '''Affiche les stats totales'''
        x, y, size = 10, 500, 20
        for i in self.stats :
            self.text2(screen, "./FreeSansBold.ttf", size, f'{i} : {round(self.stats[i], 2)}', BLACK, (x, y))
            y += size*1.2

    def description(self) :
        if type(self.objet_selection) == tuple and self.objet_selection[2] != '' : # On affiche les informations seulement si un objet a été sélectionné (autrement ça fait une erreur)
            size = (200, 55 + 20*(list(self.all_items[self.objet_selection[2]][1]).count('|') + 2) + 25*len(self.all_items[self.objet_selection[2]][2]))
            pos = [x - size[0] + 14, y - size[1] + 14]
            self.image5 = pygame.transform.scale(self.o_image5, size)
            screen.blit(self.image5, (x-size[0], y-size[1]))
            self.text2(screen, "./FreeSansBold.ttf", 18, self.objet_selection[2], YELLOW, (pos[0], pos[1])) # Nom de l'objet
            pos[1] += 40
            if self.all_items[self.objet_selection[2]][1] != "" :
                texte = self.all_items[self.objet_selection[2]][1].split('|')
                for i in texte :
                    self.text2(screen, "./FreeSansBold.ttf", 15, i, WHITE, (pos[0], pos[1]))
                    pos[1] += 20
                pos[1] += 15
            for i in range(len(self.all_items[self.objet_selection[2]][2])) : # Statistiques de l'objet
                if float((self.all_items[self.objet_selection[2]][2][i].split())[1]) < 0 :
                    self.text2(screen, "./FreeSansBold.ttf", 18, self.all_items[self.objet_selection[2]][2][i], RED, (pos[0], pos[1]))
                else :
                    self.text2(screen, "./FreeSansBold.ttf", 18, self.all_items[self.objet_selection[2]][2][i], GREEN, (pos[0], pos[1]))
                pos[1] += 25
            self.mouse = pygame.mouse.get_pos()
            self.suprimer()
            self.equiper()

    def suprimer(self) :
        '''Permet de supprimer un objet depuis l'inventaire grâce à un bouton'''
        if self.mouse[0] < x-14 and self.mouse[0] > x-self.size_del-14 and self.mouse[1] < y-14 and self.mouse[1] > y-self.size_del-14 : # Permet de savoir si la souris survole le bouton
            screen.blit(pygame.transform.scale(pygame.image.load('./images/inventaire/icone_suprimer_rouge.png'), (self.size_del, self.size_del)), (x-self.size_del-14, y-self.size_del-14)) # Cas positif
            if pygame.mouse.get_pressed()[0] : # Si le bouton est cliqué on suprime l'objet
                if type(self.objet_selection) == tuple :
                    if self.objet_selection[4] == "equipement" :
                        self.objets[self.objet_selection[3]] = ""
                        self.objet_selection = ""
                        self.objets_stats() # On actualise les stats
                    elif self.objet_selection[4] == "inventaire" :
                        self.objets_inventaire[self.objet_selection[3]] = ""
                        self.objet_selection = ""
        else :
            screen.blit(pygame.transform.scale(pygame.image.load('./images/inventaire/icone_suprimer.png'), (self.size_del, self.size_del)), (x-self.size_del-14, y-self.size_del-14)) # Cas négatif

    def equiper(self) :
        if self.mouse[0] < x-self.size_del-20 and self.mouse[0] > x-2*self.size_del-20 and self.mouse[1] < y-14 and self.mouse[1] > y-self.size_del-14 : # Permet de savoir si la souris survole le bouton
            screen.blit(pygame.transform.scale(pygame.image.load('./images/inventaire/icone_equiper_verte.png'), (self.size_del, self.size_del)), (x-2*self.size_del-20, y-self.size_del-14)) # Cas positif
            if pygame.mouse.get_pressed()[0] : # Si le bouton est cliqué on suprime l'objet
                if type(self.objet_selection) == tuple :
                    if self.objet_selection[4] == "equipement" :
                        if "" in self.objets_inventaire :
                            self.objets[self.objet_selection[3]], self.objets_inventaire[self.objets_inventaire.index("")] = "", self.objets[self.objet_selection[3]]
                            self.objet_selection = ""
                            self.objets_stats() # On actualise les stats
                        else : # Cas inventaire plein
                            screen.blit(pygame.transform.scale(pygame.image.load('./images/inventaire/icone_equiper_rouge.png'), (self.size_del, self.size_del)), (x-2*self.size_del-20, y-self.size_del-14))
                    elif self.objet_selection[4] == "inventaire" :
                        if "" in self.objets :
                            self.objets_inventaire[self.objet_selection[3]], self.objets[self.objets.index("")] = "", self.objets_inventaire[self.objet_selection[3]]
                            self.objet_selection = ""
                            self.objets_stats() # On actualise les stats
                        else : # Cas équipement plein
                            screen.blit(pygame.transform.scale(pygame.image.load('./images/inventaire/icone_equiper_rouge.png'), (self.size_del, self.size_del)), (x-2*self.size_del-20, y-self.size_del-14))
        else :
            screen.blit(pygame.transform.scale(pygame.image.load('./images/inventaire/icone_equiper.png'), (self.size_del, self.size_del)), (x-2*self.size_del-20, y-self.size_del-14)) # Cas négatif

def main() :
    '''Fonction principale'''
    inventaire = Inventaire()
    while True : # False = le jeu s'arrête
        screen.fill(BLUE) # Pas WITE pour mieux voir pour les textes
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
        elif pressed[pygame.K_e] :
            if inventaire.can_switch :
                inventaire.can_switch = False
                inventaire.add_item(choice(inventaire.all_items_name))
        elif not inventaire.can_switch :
            inventaire.can_switch = True
        if inventaire.ouvert :
            inventaire.display() # Affichage
        if inventaire.affichage > 0 :
            inventaire.objet_trouve()
        inventaire.stats_display()
        pygame.display.flip()

if __name__ == '__main__' :
    main()