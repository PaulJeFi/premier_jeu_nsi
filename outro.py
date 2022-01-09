import loadding
import pygame
import sys
import time
from random import randint
from functions import text, sound, draw_rect

# Définition de couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BROWN = (100, 60, 15)

# Initialisation de Pygame
x, y = 1080, 720
screen = pygame.display.set_mode((x, y))
pygame.display.set_caption("Friends Royal")
pygame.display.set_icon(pygame.image.load('./images/personages/Humain_type_1.png').convert())
screen.fill(WHITE)

# Initialisation du texte
pygame.font.init()
frame1 = pygame.image.load('./images/intro/zombie1.png').convert()
frame2 = pygame.image.load('./images/intro/entrepreneur.jpg').convert()
frame3 = pygame.image.load('./images/intro/paicCitron.jpg').convert()

# Initialisation du son.
pygame.mixer.init()
clic = pygame.mixer.Sound("./sons/clic_clavier.wav") # son du clavier
#music = pygame.mixer.Sound("./contents/punch.wav") # music de fond

# Les différents textes d'Outro, regroupés par slides contenant des lignes
text_Outro1 = ["Apres cette grande période de chaos que vous venez de traverser, vous êtes quelque","peut fatigué et vous décidez de prendre un moment pour réfléchir à votre avenir","dans ce monde désormais si propre. "]
text_Outro2 = ["Qu'allez vous faire de tout votre temps maintenant que vous êtes sans emploi ?","Mais vous vous souvenez tout à coup de vos cours de SES en seconde et décider de ","créer un produit révolutionnaire qui n'existe pas dans le monde des machines à laver"]
text_Outro3 = ["Vous devenez l'un des patrons les plus en vogue et les plus respecté de la silicone ","vallée et votre start-up de liquide vaisselle génère des milliards de dollards.","Vous êtes maintenant le roi du monde"]

class Outro() :
    """Classe de l'Outro"""
    def __init__(self) :
        self.text = text_Outro1
        self.image = frame1
        self.image = pygame.transform.scale(self.image,(1080, 720-150))
        self.char = -1
        self.is_finished = False

    def change_text(self) :
        """Passer d'une slide à l'autre"""
        if self.text == text_Outro1 :
            self.text = text_Outro2
            self.image = frame2
            self.image = pygame.transform.scale(self.image,(1080, 720-150))
        elif self.text == text_Outro2 :
            self.text = text_Outro3
            self.image = frame3
            self.image = pygame.transform.scale(self.image,(1080, 720-150))
        elif self.text == text_Outro3 :
            self.is_finished = True

    def display(self) :
        '''Affichage'''
        screen.blit(self.image, (0, 0))
        draw_rect(screen, (0, 720-150), (1080, 150), BROWN)
        draw_rect(screen, (10, 720-135), (1080-20, 135-15), BLACK)
        self.write()
        time.sleep(0.08)

    def write(self) :
        '''Comment écrire le texte'''
        self.char += 1  # On basera toutes les actions sur le nombre de carractères affichés jusqu'alors
        if self.char < len(self.text[0]) : # si on est à la première ligne
            text(screen, "./courriernewbold.ttf", 20, self.text[0][0:self.char]+'|', WHITE, (30, 720-150+30))
            self.sound()
        elif self.char-len(self.text[0]) < len(self.text[1]) : # sinon si on est à la deuxième ligne
            text(screen, "./courriernewbold.ttf", 20, self.text[0][0:self.char], WHITE, (30, 720-150+30))
            text(screen, "./courriernewbold.ttf", 20, self.text[1][0:self.char-len(self.text[0])]+'|', WHITE, (30, 720-150+60))
            self.sound()
        elif self.text == text_Outro1 or self.text == text_Outro3 : # sinon, si on est à la troisième ligne
            if self.char-len(self.text[0])-len(self.text[1]) < len(self.text[2]) :
                text(screen, "./courriernewbold.ttf", 20, self.text[0], WHITE, (30, 720-150+30))
                text(screen, "./courriernewbold.ttf", 20, self.text[1], WHITE, (30, 720-150+60))
                text(screen, "./courriernewbold.ttf", 20, self.text[2][0:self.char-len(self.text[0])-len(self.text[1])]+'|', WHITE, (30, 720-150+90))
                self.sound()
            else :
                time.sleep(5) # on attend 5 sec entre chaque slide
                self.change_text()
                self.char = 0
        else :
            time.sleep(5) # on attend 5 sec entre chaque slide
            self.change_text()
            self.char = 0
        
    def sound(self) :
        '''Le son des clics du clavier'''
        if self.char%randint(1, 4) == 0 : # on clique tous les random caractères, pour un son plus réaliste.
            sound(clic)

def main() :
    '''Boucle principale'''
    outro = Outro()
    while True :
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                pygame.quit()
                sys.exit()
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_SPACE] : # histoire qu'on puisse passer l'Outro
            break
        outro.display()
        text(screen, "./courriernewbold.ttf", 20, '[espace]: passer l\'outro', WHITE, (750, 720-150+90))
        pygame.display.flip()
        if outro.is_finished :
            break

if __name__ == "__main__" :
    main()