'''
Partie principale du script
Les autre fichiers sont des éléments externes au gameplay principal ou des scripts en cours de dévelopement
'''

# Tous les imports du script, certains ne sont pas encore utilisés mais le seront très prochainement
import intro    # L'introduction se lance toute seule
import loadding  # L'écran de chargement se charge tout seul
from pygame import mouse
from pygame.constants import MOUSEBUTTONDOWN, MOUSEBUTTONUP
from pygame.event import wait
from pygame.mixer import pause, unpause
from inventaire import Inventaire
import pygame
import sys
import math
import random
from functions import deplace, draw_rect, convert_degrees, convert_radians, curseur
from zombies_new import Construct_Zombies
import save

# Définition de certaines couleurs
BLACK = (0, 0, 0)
GRAY = (20, 20, 20)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

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

intro.main() # Lancement de l'intro

#import et init des musiques d'ambiences 
pygame.mixer.init()
pygame.mixer.get_num_channels()

mus_game_over = pygame.mixer.Sound("musiques/gameOver.mp3")
mus_victoire = pygame.mixer.Sound("./musiques/victoire.mp3")
mus_jeu = pygame.mixer.Sound("./musiques/soundtrack.mp3")
jouer_son = 0
#import des sons additionels 
tir_arme = pygame.mixer.Sound("./sons/sons armes/son arme 1.mp3")
sMarche = pygame.mixer.Sound("./sons/sons marche herbe/bruit marche dans l'herbe.wav")
#création variables pour les channels du mixer 
pygame.mixer.set_num_channels(10)  # Crée 10 chaînes. 8 par défaut. On les apellera après.

# Police d'écriture ci-dessous
# doc :
#pygame.font.get_default_font()
#pygame.font.get_fonts()
'''  Les polices actuelles sont "./FreeSansBold.ttf" et "./courriernewbold.ttf".  '''

def text(screen, font, size, string, color, pos) :
    '''Permet d'afficher un texte de façon simplifiée'''
    textsurface = pygame.font.Font(font, size).render(string, False, color)
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

    
    def musique_start(self):
        #le lancement de la musique s'effectue doucement puis tourne en boucle jusqu'à la fin du jeu
        pygame.mixer.Channel(0).play(mus_jeu)
    
    
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

    def on_off(self, game_over) :
        '''Le setup qui permet de faire pause'''
        if self.highlight() and self.can_switch and not game_over :
            if self.status == True and pygame.mouse.get_pressed()[0] :
                self.cooldown = 0
                pygame.mixer.pause()
                self.status = False
            elif self.status == False and pygame.mouse.get_pressed()[0] :
                self.cooldown = 0
                pygame.mixer.unpause()
                self.status = True

class tout_sons():
     # gestion intégrale du son

    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.set_num_channels(self.channels)

    def pause(self):
        pygame.mixer.channel(jouer_son).pause

    def unpause(self):
        pygame.mixer.channel(jouer_son).unpause

    def fin_musique(self):
        pass

    def musique_mort(self):
        #le lancement de la musique s'effectue doucement puis tourne en boucle jusqu'à la fin du jeu
        pygame.mixer.Channel(1).play(mus_game_over)


class Score_actuel() :
    '''Classe pour le score'''

    def __init__(self) :
        '''Appel initial de la classe'''
        self.score = 0
        self.niveau = 0 # Plus le niveau est élevé, plus le jeu devient difficile
        # Palier de score requis pour passer au niveau de difficulté supérieur
        self.score_min_pour_niveau = [1000, 2500, 4500, 7000, 10000, 14000,
        20000, 28000, 38000, 50000, 65000, 80000, 100000, float('inf')]
        self.nom_niveau = ['Jeu d\'enfant', 'Simplissime', 'Facile',
        'Abordable', 'Intermédiaire', 'Un peu complexe', 'Compliqué',
        'Difficile', 'Très dur', 'Périlleux', 'Cauchemardesque', 'Démoniaque',
        'Impossible', 'SEIGNEUR MANDIC']

    def display(self) :
        text(screen, "./FreeSansBold.ttf", 25, f'Votre score : {self.score} points', WHITE, (500, 20))
        text(screen, "./FreeSansBold.ttf", 25, f'Difficuté actuelle: {self.nom_niveau[self.niveau]}', WHITE, (500, 40))

    def add(self, score) :
        '''Permet d'actualiser le score et la difficulté'''
        self.score += score
        if self.niveau < len(self.score_min_pour_niveau)-1 :
            while self.score >= self.score_min_pour_niveau[self.niveau] :
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
        self.max_pv = Inventaire().stats["Vie"]
        self.pv = self.max_pv
        self.old_pv = self.pv # Utilisé pour la fonction regen
        self.pv_différence = 0 # Même chose
        self.angle = 90
        self.rotated = pygame.image.load('./images/personages/Humain_type_1.png')
    
    def regen(self, valeur, dt) :
        '''Régénération naturelle de la vie du héro'''
        # Si le héro a pris de gros dégat récemment, il regagnera plus lentement des pv
        if self.old_pv > self.pv : # Calcul des dégats reçus
            self.pv_différence += 200*(self.old_pv - self.pv)/self.max_pv
        self.old_pv = self.pv
        if self.pv + valeur*(0.97**self.pv_différence) < self.max_pv : # Régénération des pv en fonction de la pénalité de dégats reçus
            self.pv += valeur*(0.97**self.pv_différence)
        else :
            self.pv = self.max_pv
        self.pv_différence -= self.max_pv/dt/250 # Diminution du malus de régénération
        if self.pv_différence < 0 :
            self.pv_différence = 0
        if self.pv_différence > 100 :
            self.pv_différence = 100

    def pv_check(self, vie) :
        '''Permet au pv du personnage de rester dans l'interval suivant   -->   [ 0 ; self.max_pv ]'''
        # Permet aussi d'actualiser le nombre maximal de pv
        Inventaire().objets_stats()
        if self.pv > self.max_pv :
            self.pv = self.max_pv
        elif self.pv <= 0 :
            self.pv = 0
        if self.max_pv != vie and vie >= 1 :
            self.pv = self.pv/self.max_pv*vie
            self.max_pv = vie
        elif self.max_pv != 0.001 and vie < 1 :
            self.pv = 0.001
            self.max_pv = 0.001
        

    def display(self) :
        '''Affichage de soi-même'''
        screen.blit(self.rotated, (self.x, self.y))
        self.arme.display()

    def GUI_display(self):
        '''Affichage de la barre de pv'''
        if self.max_pv == 0.001 : # Easter egg pour avoir self.max_pv = 0
            HP_GREEN = (100, 0, 0)
        elif self.pv > 0 : # <-- La division par 0 cause une ERREUR
            HP_GREEN = (200-(self.pv/self.max_pv*200), self.pv/self.max_pv*255, 0) # <-- La barre de vie change de couleur en fonction du nombre de pv restant
        else :
            HP_GREEN = (200, 0, 0)
        draw_rect(screen, (25, 25), (300, 25), BLACK)
        draw_rect(screen, (27, 27), (296, 21), GRAY)
        draw_rect(screen, (27, 27), (int((296)*(self.pv/self.max_pv)), 21), HP_GREEN)
        # Affichage de la valeur numérique des pv
        if self.max_pv != 0.001 :
            draw_rect(screen, (25, 50), ((len(f'{round(self.pv)} / {round(self.max_pv)}'))*7, 16), BLACK)
            text(screen, "./FreeSansBold.ttf", 12, f'{round(self.pv)} / {round(self.max_pv)}', WHITE, (31, 50))
        else :
            text(screen, "./FreeSansBold.ttf", 12, 'ERROR', RED, (140, 30)) # Easter egg pour avoir self.max_pv = 0

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
        self.size = 40
        self.image = pygame.image.load('./images/armes/Projectiles/Projectile.png')#.convert()
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.x = x/2-self.size/2
        self.y = y/2-self.size/2
        self.calculer(mouse)
        self.image = pygame.transform.rotate(self.image, self.angle)

    def calculer(self, mousepos) :
        '''Si vous n'aimez pas la trigonométrie ou les vecteurs, passez votre
        chemin.'''
        self.angle = 0
        if mousepos[0]-x/2 != 0 :
            self.angle = math.atan((mousepos[1]-y/2)/(mousepos[0]-x/2))
            self.angle = convert_degrees(self.angle)
            if mousepos[0] < x/2 :
                self.angle = 180-self.angle
            else :
                self.angle = -self.angle
        else :
            if mousepos[1] < y/2 :
                self.angle = 90
            else :
                self.angle = -90
        self.vect = [math.cos(convert_radians(self.angle)), -math.sin(convert_radians(self.angle))]
    
    def move(self, dt, marche_arret) :
        if marche_arret :
            self.x += self.vect[0]*self.speed*dt
            self.y += self.vect[1]*self.speed*dt
    
    def display(self, dt, marche_arret) :
        '''Affichage de soi-même'''
        self.move(dt, marche_arret)
        screen.blit(self.image, (round(self.x), round(self.y)))
    
    def get_rect(self) :
        '''Donne les infos du rectangle de la balle (abscisse, ordonnée, largeur, longueur)'''
        return pygame.Rect(self.x, self.y, self.size, self.size)

class Construct_munitions() :
    '''Classe de gestion des munitions'''
    def __init__(self) :
        self.balles = []
    
    def add(self) :
        self.balles.append(Munition())
    
    def display(self, dt, marche_arret) :
        self.update()
        for balle in self.balles :
            balle.display(dt, marche_arret)

    def update(self) :
        '''Supprime les balles qui doivent être supprimées.'''
        for balle in self.balles :
            if balle.x < -2*x or balle.y < -2*y or balle.x > 2*x or balle.y > 2*y :
                self.balles.pop(self.balles.index(balle))

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

def main(score=save.get()["best_score"]) :
    '''Fonction principale'''
    save.add_game()
    jouer_son = mus_jeu
    marche_arret = Marche_Arret()
    inventaire = Inventaire()
    grass = Grass()
    hero = Hero()
    score = Score_actuel()
    soin = Soin()
    zombies = Construct_Zombies()
    balles = Construct_munitions()
    marche_arret.musique_start()
    """musique_start()"""
    game_over = False
    while True : # False = le jeu s'arrête
        dt = clock.tick(144) # IMPORTANT : FPS du jeu
        screen.fill(WHITE)
        if score.score > save.get()["best_score"] :
            save.set_score(score.score)
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over and marche_arret.game_state() and not inventaire.ouvert :
                balles.add()
        marche_arret.on_off(game_over) # Permet de savoir si le jeu est OUI ou NON en PAUSE
        if marche_arret.game_state() and not inventaire.ouvert : # Exécute seulement si le jeu est en marche
            '''Les lignes suivantes permettent le déplacement de tous les objets, sauf du héro (illusion de mouvement)'''
            pressed = pygame.key.get_pressed()
            # Ajustement de la valleur de la vitesse du joueur afin qu'il se déplace aussi vite en diagonal qu'en ligne droite
            if pressed[pygame.K_z] and pressed[pygame.K_q] or pressed[pygame.K_z] and pressed[pygame.K_d] or pressed[pygame.K_s] and pressed[pygame.K_q] or pressed[pygame.K_s] and pressed[pygame.K_d] or pressed[pygame.K_UP] and pressed[pygame.K_LEFT] or pressed[pygame.K_UP] and pressed[pygame.K_RIGHT] or pressed[pygame.K_DOWN] and pressed[pygame.K_LEFT] or pressed[pygame.K_DOWN] and pressed[pygame.K_RIGHT] :
                speed_hero = math.sqrt(2)/2*dt
            else :
                speed_hero = dt
            speed_hero *= inventaire.stats["Spe"] # Vitesse du héro en fonction du stat "Spe"
            can_be_hit = True # Permet de faire en sorte que le héro se fasse toucher qu'une seul fois
            if pressed[pygame.K_UP] or pressed[pygame.K_z] :
                grass.bas(speed_hero)
                soin.bas(speed_hero)
                zombies.bas(speed_hero)
                balles.bas(speed_hero)
                touche = zombies.touch_balle(dt, hero.get_rect())
                if touche[0] :
                    if can_be_hit :
                        hero.pv -= (zombies.all_zombies[touche[2]][1][2])*0.99**inventaire.stats["Def"]
                        can_be_hit = False
                    grass.haut(speed_hero)
                    soin.haut(speed_hero)
                    zombies.haut(speed_hero)
                    balles.haut(speed_hero)
            if pressed[pygame.K_DOWN] or pressed[pygame.K_s] :
                grass.haut(speed_hero)
                soin.haut(speed_hero)
                zombies.haut(speed_hero)
                balles.haut(speed_hero)
                touche = zombies.touch_balle(dt, hero.get_rect())
                if touche[0] :
                    if can_be_hit :
                        hero.pv -= (zombies.all_zombies[touche[2]][1][2])*0.99**inventaire.stats["Def"]
                        can_be_hit = False
                    grass.bas(speed_hero)
                    soin.bas(speed_hero)
                    zombies.bas(speed_hero)
                    balles.bas(speed_hero)
            if pressed[pygame.K_LEFT] or pressed[pygame.K_q] :
                grass.gauche(speed_hero)
                soin.gauche(speed_hero)
                zombies.gauche(speed_hero)
                balles.gauche(speed_hero)
                touche =  zombies.touch_balle(dt, hero.get_rect())
                if touche[0] :
                    if can_be_hit :
                        hero.pv -= (zombies.all_zombies[touche[2]][1][2])*0.99**inventaire.stats["Def"]
                        can_be_hit = False
                    grass.droite(speed_hero)
                    soin.droite(speed_hero)
                    zombies.droite(speed_hero)
                    balles.droite(speed_hero)
            if pressed[pygame.K_RIGHT] or pressed[pygame.K_d] :
                grass.droite(speed_hero)
                soin.droite(speed_hero)
                zombies.droite(speed_hero)
                balles.droite(speed_hero)
                touche =  zombies.touch_balle(dt, hero.get_rect())
                if touche[0] :
                    if can_be_hit :
                        hero.pv -= (zombies.all_zombies[touche[2]][1][2])*0.99**inventaire.stats["Def"]
                        can_be_hit = False
                    grass.gauche(speed_hero)
                    soin.gauche(speed_hero)
                    zombies.gauche(speed_hero)
                    balles.gauche(speed_hero)
            touche = zombies.touch_balle(dt, hero.get_rect())
            if touche[0] and can_be_hit :
                hero.pv -= (zombies.all_zombies[touche[2]][1][2])*0.99**inventaire.stats["Def"]
                can_be_hit = False
            for balle in balles.balles : # Pour chaque balle
                test = zombies.touch_balle(dt, balle.get_rect())
                if test[0] : # Si elle touche un zombie
                    zombies.zombies[test[1]].pv -= 50 # On retire 50 aux PVs du Zombie
                    balles.balles.pop(balles.balles.index(balle)) # Et on supprime la balle
            soin.prendre(hero) # Ineterraction avec la trousse de premiers secours
            hero.regen(inventaire.stats["Reg"]/(dt*10), dt)
            hero.pv_check(inventaire.stats["Vie"])
            hero.change(pygame.mouse.get_pos())
        if hero.pv <= 0 :
            game_over = True
            pygame.mixer.stop()
            marche_arret.status = False
            marche_arret.can_switch = False
            """pygame.mixer.play(mus_game_over)"""
        pressed = (pygame.key.get_pressed(), game_over)
        if pressed[0][pygame.K_n] and pressed[1] :
            return score.score

        '''Tous les affichages de sprites'''
        grass.display()
        soin.display()
        zombies.display(dt, (marche_arret.game_state() and not inventaire.ouvert), score, inventaire)
        balles.display(dt, (marche_arret.game_state() and not inventaire.ouvert))
        hero.display()
        text(screen, "./FreeSansBold.ttf", 15, f'FPS : {dt}', BLACK, (x-150, y-50)) # Affichage des FPS
        hero.GUI_display()
        score.display()
        marche_arret.display()
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_a] :
            if inventaire.can_switch :
                inventaire.ouvert = not inventaire.ouvert
                inventaire.can_switch = False
        elif pressed[pygame.K_e] :
            if inventaire.can_switch :
                inventaire.can_switch = False
                inventaire.add_item(random.choice(inventaire.all_items_name))
        elif not inventaire.can_switch :
            inventaire.can_switch = True
        if inventaire.ouvert :
            inventaire.display() # Affichage
        if inventaire.affichage > 0 :
            inventaire.objet_trouve()
        inventaire.stats_display()
        curseur(screen)
        if game_over :
            pygame.mixer.music.load("./musiques/gameOver.mp3")
            pygame.mixer.music.play()
            text(screen, "./FreeSansBold.ttf", 50, 'GAME OVER', RED, (385, 350))
            text(screen, "./FreeSansBold.ttf", 20, 'Tapez \'n\' pour commencer une nouvelle partie.', BLACK, (250, 400))
        pygame.display.flip()

if __name__ == '__main__' :
    while True :
        main()