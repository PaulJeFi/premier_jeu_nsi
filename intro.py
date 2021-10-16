import loadding
import pygame
import sys

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

x, y = 1080, 720
screen = pygame.display.set_mode((x, y))
pygame.display.set_caption("Friends Royal")
pygame.display.set_icon(pygame.image.load('./images/personages/Humain_type_1.png').convert())
screen.fill(WHITE)
pygame.font.init()
myfont = pygame.font.SysFont('couriernewbold', 20)

pygame.mixer.init()
#clic = pygame.mixer.Sound("") # son du clavier
#music = pygame.mixer.Sound("./contents/punch.wav") # music de fond

def text(string, color, pos) :
		textsurface = myfont.render(string, False, color)
		screen.blit(textsurface, pos)

def sound(sound) :
    pygame.mixer.Sound.play(sound)
    pygame.mixer.music.stop()

text_intro = "Vous travailliez comme d'habitude dans votre boutique de machines à laver, quand votre collègue ouvre le frigo assoiffé, et boit une bouteille de lessive la confondant avec du lait. Vous le voyez se transformer sous vos yeux en zombie,  et très vite il contamine toute la ville. Étant le seul survivant, vous décidez de quitter de la ville. Dans votre fuite, vous passez devant l'armurerie désertée, et vous prenez quelques armes au cas où. La nuit commence à tomber et vous êtes presque arrivé à la forêt, avec une seule idée en tête, survire…"

def main() :
    while True :
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                pygame.quit()
                sys.exit()
        pygame.display.flip()

if __name__ == "__main__" :
	main()