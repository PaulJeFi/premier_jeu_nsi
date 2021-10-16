import loadding
import pygame
import sys
import time

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BROWN = (100, 60, 15)

x, y = 1080, 720
screen = pygame.display.set_mode((x, y))
pygame.display.set_caption("Friends Royal")
pygame.display.set_icon(pygame.image.load('./images/personages/Humain_type_1.png').convert())
screen.fill(WHITE)
pygame.font.init()
myfont = pygame.font.SysFont('couriernewbold', 20)
frame1 = pygame.image.load('./images/intro/lessive.png').convert()
frame2 = pygame.image.load('./images/intro/armurerie.png').convert()
frame3 = pygame.image.load('./images/intro/zombie1.png').convert()

pygame.mixer.init()
clic = pygame.mixer.Sound("./sons/clic_clavier.wav") # son du clavier
#music = pygame.mixer.Sound("./contents/punch.wav") # music de fond

def text(string, color, pos) :
		textsurface = myfont.render(string, False, color)
		screen.blit(textsurface, pos)

def sound(sound) :
    pygame.mixer.Sound.play(sound)
    pygame.mixer.music.stop()

def draw_rect(position, size, color) :
	'''Permet de tracer un rectangle'''
	pygame.draw.rect(screen, color, (position[0], position[1], size[0], size[1]))

text_intro1 = ["Vous travailliez comme d'habitude dans votre boutique de machines à laver, quand votre", "collègue ouvre le frigo assoiffé, et boit une bouteille de lessive, la confondant avec", "du lait."]
text_intro2 = ["Vous le voyez se transformer sous vos yeux en zombie,  et très vite il contamine toute", "la ville. Étant le seul survivant, vous décidez de quitter de la ville."]
text_intro3 = ["Dans votre fuite, vous passez devant l'armurerie désertée, et vous prenez quelques", "armes au cas où. La nuit commence à tomber et vous êtes presque arrivé à la forêt, avec", "une seule idée en tête, survire…"]

class Intro() :
    """Classe de l'intro"""
    def __init__(self) :
        self.text = text_intro1
        self.image = frame1
        self.image = pygame.transform.scale(self.image,(1080, 720-200))
        self.char = -1

    def change_text(self) :
        if self.text == text_intro1 :
            self.text = text_intro2
        elif self.text == text_intro2 :
            self.text = text_intro3

    def dislpay(self) :
        screen.blit(self.image, (0, 0))
        draw_rect((0, 720-200), (1080, 200), BROWN)
        draw_rect((10, 720-185), (1080-20, 175), BLACK)
        self.write()
        time.sleep(0.1)

    def write(self) :
        self.char += 1
        if self.char < len(self.text[0]) :
            text(self.text[0][0:self.char]+'|', WHITE, (30, 720-200+30))
        elif self.char-len(self.text[0]) < len(self.text[1]) :
            text(self.text[0][0:self.char], WHITE, (30, 720-200+30))
            text(self.text[1][0:self.char-len(self.text[0])]+'|', WHITE, (30, 720-200+60))
        if self.char%3 == 0 : # on clique tous les 3d caractères, pour un son plus réaliste.
            sound(clic)

def main() :
    intro = Intro()
    while True :
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                pygame.quit()
                sys.exit()
        intro.dislpay()
        pygame.display.flip()

if __name__ == "__main__" :
	main()