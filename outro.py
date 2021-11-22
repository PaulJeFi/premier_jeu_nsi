from typing_extensions import Self
import pygame
import sys
import time
import loadding
from random import randint
from functions import text, sound, draw_rect

# Définition de couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BROWN = (100, 60, 15)

#initialisation de la fenêtre pygame

x, y = 1080, 720
screen = pygame.display.set_mode((x, y))
pygame.display.set_caption("Friends Royal")
pygame.display.set_icon(pygame.image.load('./images/personages/Humain_type_1.png').convert())
screen.fill(WHITE)

#chargement des images 

img1 = pygame.image.load("./images/intro/zombie1.png")
img2 = pygame.image.load("./images/intro/lessive.png")
img3 = pygame.image.load("./images/intro/zombie2.png")
#image à ajouter

#initialisation et chargement de la police 
pygame.font.init()
myfont = pygame.font.Sysfont("couriernewbold", 20)

#initialisation du son
pygame.mixer.init()
son = pygame.mixer.load("./sons/clic_clavier.wav")

#definiton des textes

text_outro1 = ["Votre victoire est totale, vous avez enfin sauvé le monde de la lessive."]
text_outro2 = ["texte en cours d'écriture"]
text_outro3 = ["pas plus d'inspitration :", "texte en cours d'écriture"]


class outro():
    
    def __init__(self):
            self.text = text_outro1
            self.image = img1
            self.image = pygame.transform.scale((1080, 720 - 150))
            self.is_finished = False

    def changement_texte(self):
        #change le texte et l'image en fonction de celui déjà afficher à l'écran
        if self.text == text_outro1:
            self.text = text_outro2
            self.image = img2
            self.image = pygame.transform.scale(1080, 720 - 150)
        
        elif self.text == text_outro2:
            self.text = text_outro3
            self.image = img3
            self.image = pygame.transfrom.scale(1080, 720 - 150)

        #ferme l'affichage si les trois textes sont terminés 
        elif self.text == text_outro3:
            self.is_finished = True

    def ecran (self):
        #creer l'affichage de la fenêtre
        screen.blit(self.image, (0, 0))
        draw_rect(screen, (0, 570), (1080, 720), BROWN)
        draw_rect(screen, (15, 585), (1080, 705), BROWN)
        self.write()

    def ecriture():
        text(screen, myfont, text_outro1, WHITE, (30,600))
        if text_outro1 == (1050, 600):
            text(screen, myfont, text_outro1, WHITE, (30,650))

    def son (self):
        if randint(1, 2):
            sound(son)
        




"""
#main
main() 

while True:
    for event in pygame.evengt.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    if outro.is_finished: 
        break

"""


        
        

