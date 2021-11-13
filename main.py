'''
Partie principale du script
Les autre fichiers sont des éléments externes au gameplay principal ou des scripts en cours de dévelopement
'''

# Tous les imports du script, certains ne sont pas encore utilisés mais le seront très prochainement
import loadding
from pygame import mouse
from pygame.constants import MOUSEBUTTONDOWN, MOUSEBUTTONUP
from pygame.event import wait
from pygame.mixer import pause, unpause
import pygame
import sys
import math
import random
from functions import deplace, draw_rect, convert_degrees, convert_radians, curseur
from zombies import Construct_Zombies

# Définition de certaines couleurs
BLACK = (0, 0, 0)
GRAY = (20, 20, 20)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Les règlages de base (vitesse du joueur + set-up affichage + set-up frame-rate)
SPEED = 0.4 # Je pense qu'il faudrait le mêtre dans la classe héro dans   -->   def __init__(self):
# Initialisation de Pygame
x, y = 1080, 720 # dimensions de l'écran, en pixels
pygame.init()
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode((x, y))
pygame.display.set_caption("Friends Royal")
pygame.display.set_icon(pygame.image.load('./images/personages/Humain_type_1.png').convert())
screen.fill(WHITE)
clock = pygame.time.Clock()

# Police d'écriture ci-dessous
myfont = pygame.font.SysFont('couriernewbold', 24)

def text(screen, font, string, color, pos) :
    '''Permet d'afficher un texte de façon simplifiée'''
    textsurface = font.render(string, False, color)
    screen.blit(textsurface, pos)

class Marche_Arret() :
    '''Classe du bouton pause/marche'''

    def __init__(self) :
        '''Appel initial de la classe'''
        self.status = True # <-- True pour MARCHE ; False pour PAUSE
        self.image = pygame.image.load('./images/interface/Bouton_pause_stop.png')
        self.size = 50
        self.image = pygame.transform.scale(self.image,(self.size,self.size))
        self.rect = self.image.get_rect()
        self.rect.x = x - self.size*2
        self.rect.y = 0
        self.base_cooldown = 100 # permet d'éviter le lag losrque l'on met le jeu en pause/marche
        self.cooldown = self.base_cooldown
        self.can_switch = True # True pour on peut mettre le jeu en pause/marche via le bouton pause

    def display(self) :
        '''Affichage de soi-même'''
        screen.blit(self.image, self.rect)
    
    def highlight(self) :
        '''Permet de faire briller le bouton pause quand on a sa souris dessus'''
        pos = pygame.mouse.get_pos()
        if pos[0] > x - self.size*2 and pos[1] < self.size*2 :
            if self.status == True :
                self.image = pygame.image.load('./images/interface/Bouton_pause_stop_lumineux.png')
            else :
                self.image = pygame.image.load('./images/interface/Bouton_pause_marche_lumineux.png')
            return True
        else :
            if self.status == True :
                self.image = pygame.image.load('./images/interface/Bouton_pause_stop.png')
            else :
                self.image = pygame.image.load('./images/interface/Bouton_pause_marche.png')
            return False

    def game_state(self) :
        '''Pause ou Marche'''
        if self.cooldown != self.base_cooldown :
            self.cooldown += 1
        self.can_switch = self.cooldown == self.base_cooldown
        return self.status

    def on_off(self) :
        '''Le setup qui permet de faire pause'''
        if self.highlight() and self.can_switch :
            if self.status == True and pygame.mouse.get_pressed()[0] :
                self.cooldown = 0
                self.status = False
            elif self.status == False and pygame.mouse.get_pressed()[0] :
                self.cooldown = 0
                self.status = True
        
class Score_actuel() :
    '''Classe pour le score'''

    def __init__(self) :
        '''Appel initial de la classe'''
        self.score = 0
        self.niveau = 0 # Plus le niveau est élevé, plus le jeu devient difficile
        # Palier de score requis pour passer au niveau de difficulté supérieur
        self.score_min_pour_niveau = [1000, 2500, 4500, 7000, 10000, 14000,
        20000, 28000, 38000, 50000, 65000, 80000, 100000]
        self.nom_niveau = ['Jeu d\'enfant', 'Simplissime', 'Facile',
        'Abordable', 'Intermédiaire', 'Un peu complexe', 'Compliqué',
        'Difficile', 'Très dur', 'Périlleux', 'Cauchemardesque', 'Démoniaque',
        'Impossible', 'SEIGNEUR MANDIC']

    def display(self) :
        text(screen, myfont, f'Votre score : {self.score} points', WHITE, (500, 20))
        text(screen, myfont, f'Difficuté actuelle: {self.nom_niveau[self.niveau]}', WHITE, (500, 40))

    def add(self, score) :
        '''Permet d'actualiser le score et la difficulté'''
        self.score += score
        if self.niveau < len(self.score_min_pour_niveau)  :
            if self.score >= self.score_min_pour_niveau[self.niveau] :
                self.niveau += 1




    # CETTE CLASSE RALENTIE UN PEU LE JEU

    #def __init__(self) :
    #    '''Appel initial de la classe'''
    #    self.score = 0
    #    self.niveau = 9 # <-- Plus cette valeur est faible, plus le champs de vision et réduit (de 9 à 1)

    #def display(self) :
    #    '''Affichage de soi-même'''
    #    self.b_image = pygame.image.load(f'./images/autres/Brouillard{self.niveau}.png')
    #    self.rect = self.b_image.get_rect()
    #    screen.blit(self.b_image, self.rect)
    #    self.add(0) # TEST evolution brouillard : A SUPRIMER !
    
    #def add(self, score) :
    #    '''Permet d'actualiser le score, le brouillard et la difficulté'''
    #    self.score += score
    #    if self.score+self.niveau*1000 >= 10000 and self.niveau != 1 :
    #        self.niveau -= 1


class Grass() :
    '''Classe permettant de remplir l'arrière plan avec des tuilles d'herbe'''

    def __init__(self) :
        '''Appel initial de la classe'''
        self.size = 1600
        self.image = pygame.image.load('./images/tuilles_de_terrain/Herbe_V2.png')
        self.image = self.image = pygame.transform.scale(self.image, (int(1.5*self.size+SPEED), int(1.5*self.size+SPEED)))
        # Placer tous les pavés de terrains à leurs emplacement initial
        self.image_1 = [0, 0]
        self.image_2 = [0, self.size]
        self.image_3 = [self.size, self.size]
        self.image_4 = [self.size, 0]
        self.image_5 = [self.size, -self.size]
        self.image_6 = [0, -self.size]
        self.image_7 = [-self.size, -self.size]
        self.image_8 = [-self.size, 0]
        self.image_9 = [-self.size, self.size]
        # Et un conteneur qui les contient tous...
        self.images = [self.image_1, self.image_2, self.image_3, self.image_4,
        self.image_5, self.image_6, self.image_7, self.image_8, self.image_9]
        for Image in self.images :
            screen.blit(self.image, (Image[0], Image[1]))

    '''Les fontions suivantes permettent le déplacement des tuiles pour donner l'illusion de mouvement'''

    def droite(self, dt) :
        for Image in self.images :
            self.replacer(Image)
            Image[0] -= SPEED*dt
    
    def haut(self, dt) :
        for Image in self.images :
            self.replacer(Image)
            Image[1] -= SPEED*dt

    def gauche(self, dt) :
        for Image in self.images :
            self.replacer(Image)
            Image[0] += SPEED*dt
    
    def bas(self, dt) :
        for Image in self.images :
            self.replacer(Image)
            Image[1] += SPEED*dt

    def display(self) :
        '''Affichage de soi-même'''
        for Image in self.images :
            screen.blit(self.image, (Image[0], Image[1]))
    
    def replacer(self, Image) :
        '''Fonction du pavage de l'herbe. Permet de replacer un pavé si il est inutile à l'affichage'''
        if Image[0] < -2*self.size :
            Image[0] = self.size
        elif Image[0] > 2*self.size :
            Image[0] = -self.size
        if Image[1] < -2*self.size :
            Image[1] = self.size
        elif Image[1] > 2*self.size :
            Image[1] = -self.size

class Hero() :
    '''Classe du personnage'''

    def __init__(self) :
        '''Appel initial de la classe'''
        self.arme = Arme()
        self.image = pygame.image.load('./images/personages/Humain_type_1.png')
        self.size = 100
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.x = x/2 - self.size//2
        self.y = y/2 - self.size//2
        self.rect = self.image.get_rect()
        self.max_pv = 100
        self.pv = 100
        self.angle = 90
        self.rotated = pygame.image.load('./images/personages/Humain_type_1.png')
    
    def pv_check(self) :
        '''Permet au pv du personnage de rester dans l'interval suivant   -->   [ 0 ; slef.max_pv ]'''
        if self.pv > self.max_pv :
            self.pv = self.max_pv
        elif self.pv < 0 :
            self.pv = 0

    def display(self) :
        '''Affichage de soi-même'''
        screen.blit(self.rotated, (self.x, self.y))
        self.arme.display()

    def GUI_display(self):
        '''Affichage de la barre de pv'''
        if self.pv > 0 : # <-- La division par 0 cause une ERREUR
            HP_GREEN = (200-(self.pv/self.max_pv*200), self.pv/self.max_pv*255, 0) # <-- La barre de vie change de couleur en fonction du nombre de pv restant
        else :
            HP_GREEN = (200, 0, 0)
        draw_rect(screen, (25, 25), (300, 25), BLACK)
        draw_rect(screen, (27, 27), (296, 21), GRAY)
        draw_rect(screen, (27, 27), (int((296)*(self.pv/self.max_pv)), 21), HP_GREEN)

    def change(self, mousepos) :
        '''Tourne le personnage pour qu'il ragarde la souris'''
        if mousepos[0]-x/2 != 0 :
            self.angle = math.atan((mousepos[1]-y/2)/(mousepos[0]-x/2))
            self.angle = convert_degrees(self.angle)
            if mousepos[0] < x/2 :
                self.angle = 180-self.angle
            else :
                self.angle = -self.angle
            self.rotated = pygame.transform.rotate(self.image, self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)
            self.arme.rotate(self.angle)

    def get_rect(self) :
        '''Donne les infos du rectangle du personnage (abscisse, ordonnée, largeur, longueur)'''
        return pygame.Rect(self.x, self.y, self.size, self.size)

class Soin(deplace) :
    '''Classe de la trousse de premiers secours'''

    def __init__(self) :
        '''Appel initial de la classe'''
        self.x, self.y = random.randint(0, x), random.randint(0, y)
        self.image = pygame.image.load('./images/objets/Pack de soin.png')
        self.size = (50, 50)
        self.image = pygame.transform.scale(self.image, self.size)

    def replace(self) :
        position = random.randint(1,5)
        if position == 1 :
            self.x, self.y = -x, random.randint(-y, 2*y)
        elif position == 2 :
            self.x, self.y = random.randint(-x, 2*x), -y
        elif position == 3 :
            self.x, self.y = 2*x, random.randint(-y, 2*y)
        else :
            self.x, self.y = random.randint(-x, 2*x), 2*y

    def display(self) :
        '''Affichage de soi-même'''
        if (self.x+self.size[0] < -x) or (self.x > 2*x) or (self.y+self.size[1] < -y) or (self.y > 2*y) :
            self.replace()
        screen.blit(self.image, (self.x, self.y))

    '''def get_rect(self) :
        # Donne les infos du rectangle de la trousse de premiers secours (abscisse, ordonnée, longueur)
        return pygame.Rect(self.x, self.y, *self.size)'''

    def prendre(self, hero) :
        '''Interraction avec la trousse de premiers secours'''
        if self.x > x/2 - hero.size//2 and self.x < x/2 + hero.size//2 and self.y > y/2 - hero.size//2 and self.y < y/2 + hero.size//2 and hero.pv != hero.max_pv :
            self.replace()
            if hero.pv < hero.max_pv - 35 :
                hero.pv += 35
            else :
                hero.pv = hero.max_pv

class Arme() :
    '''Classe des armes'''
    # PS : va bientôt disparaitre car la classe héro va fusionner avec celle ci

    def __init__(self) :
        '''Appel initial de la classe'''
        # taille = 1105 x 682
        self.image = pygame.image.load('./images/armes/Mitraillette/Mitraillette_frame1.png')
        self.size = [1105/8, 682/8]
        self.image = pygame.transform.scale(self.image, (int(self.size[0]), int(self.size[1])))
        self.rotated = pygame.image.load('./images/armes/Mitraillette/Mitraillette_frame1.png')
    
    def display(self) :
        '''Affichage de soi-même'''
        screen.blit(self.rotated, (int(self.x/2-self.size[0]/2), int(self.y/2-self.size[1]/2)))
    
    def rotate(self, angle) :
        '''Rotation de soi-même pour regarder vers la souris'''
        self.rotated = pygame.transform.rotate(self.image, angle)
        self.x = (x)+math.sin(convert_radians(angle))*100+50
        self.y = (y)+math.cos(convert_radians(angle))*100-10

class Munition(deplace) :
    '''Les munitions.'''
    def __init__(self) :
        mouse = pygame.mouse.get_pos()
        self.speed = 1.5
        self.size = 20
        self.image = pygame.image.load('./images/personages/Humain_type_1.png').convert()
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.x = x/2-self.size/2
        self.y = y/2-self.size/2
        self.calculer(mouse)
        self.image = pygame.transform.rotate(self.image, self.angle)

    def calculer(self, mousepos) :
        '''Si vous n'aimez pas la trigonométrie ou les vecteurs, passez votre
        chemin.'''
        if mousepos[0]-x/2 != 0 :
            self.angle = math.atan((mousepos[1]-y/2)/(mousepos[0]-x/2))
            self.angle = convert_degrees(self.angle)
            if mousepos[0] < x/2 :
                self.angle = 180-self.angle
            else :
                self.angle = -self.angle
        self.vect = [math.cos(convert_radians(self.angle)), -math.sin(convert_radians(self.angle))]
    
    def move(self, dt) :
        self.x += round(self.vect[0]*self.speed*dt)
        self.y += round(self.vect[1]*self.speed*dt)
    
    def display(self, dt) :
        '''Affichage de soi-même'''
        self.move(dt)
        screen.blit(self.image, (self.x, self.y))
    
    def get_rect(self) :
        '''Donne les infos du rectangle de la balle (abscisse, ordonnée, largeur, longueur)'''
        return pygame.Rect(self.x, self.y, self.size, self.size)

class Construct_munitions() :
    '''Classe de gestion des munitions'''
    def __init__(self) :
        self.balles = []
    
    def add(self) :
        self.balles.append(Munition())
    
    def display(self, dt) :
        for balle in self.balles :
            balle.display(dt)

    def haut(self, dt) :
        for balle in self.balles :
            balle.haut(dt)

    def bas(self, dt) :
        for balle in self.balles :
            balle.bas(dt)

    def gauche(self, dt) :
        for balle in self.balles :
            balle.gauche(dt)

    def droite(self, dt) :
        for balle in self.balles :
            balle.droite(dt)

def main() :
    '''Fonction principale'''
    marche_arret = Marche_Arret()
    grass = Grass()
    hero = Hero()
    score = Score_actuel()
    soin = Soin()
    zombies = Construct_Zombies()
    balles = Construct_munitions()
    while True : # False = le jeu s'arrête
        dt = clock.tick(144) # IMPORTANT : FPS du jeu
        screen.fill(WHITE)
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN :
                balles.add()
        marche_arret.on_off() # Permet de savoir si le jeu est OUI ou NON en PAUSE
        if marche_arret.game_state() : # Exécute seulement si le jeu est en marche
            '''Les lignes suivantes permettent le déplacement de tous les objets, sauf du héro (illusion de mouvement)'''
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_UP] or pressed[pygame.K_z] :
                grass.bas(dt)
                soin.bas(dt)
                zombies.bas(dt)
                balles.bas(dt)
                if zombies.touch_hero(dt, hero.get_rect()) :
                    hero.pv -= 0.5
                    grass.haut(dt)
                    soin.haut(dt)
                    zombies.haut(dt)
                    balles.haut(dt)
            if pressed[pygame.K_DOWN] or pressed[pygame.K_s] :
                grass.haut(dt)
                soin.haut(dt)
                zombies.haut(dt)
                balles.haut(dt)
                if zombies.touch_hero(dt, hero.get_rect()) :
                    hero.pv -= 0.5
                    grass.bas(dt)
                    soin.bas(dt)
                    zombies.bas(dt)
                    balles.bas(dt)
            if pressed[pygame.K_LEFT] or pressed[pygame.K_q] :
                grass.gauche(dt)
                soin.gauche(dt)
                zombies.gauche(dt)
                balles.gauche(dt)
                if zombies.touch_hero(dt, hero.get_rect()) :
                    hero.pv -= 0.5
                    grass.droite(dt)
                    soin.droite(dt)
                    zombies.droite(dt)
                    balles.droite(dt)
            if pressed[pygame.K_RIGHT] or pressed[pygame.K_d] :
                grass.droite(dt)
                soin.droite(dt)
                zombies.droite(dt)
                balles.droite(dt)
                if zombies.touch_hero(dt, hero.get_rect()) :
                    hero.pv -= 0.5
                    grass.gauche(dt)
                    soin.gauche(dt)
                    zombies.gauche(dt)
                    balles.gauche(dt)
            if zombies.touch_hero(dt, hero.get_rect()) :
                hero.pv -= 0.5
            soin.prendre(hero) # Ineterraction avec la trousse de premiers secours
            hero.pv_check()
            hero.change(pygame.mouse.get_pos())
        '''Tous les affichages de sprites'''
        grass.display()
        soin.display()
        zombies.display(dt, marche_arret.game_state(), score)
        balles.display(dt)
        hero.display()
        hero.GUI_display()
        score.display()
        marche_arret.display()
        curseur(screen)
        pygame.display.flip()

if __name__ == '__main__' :
    main()