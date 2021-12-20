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
from functions import deplace, draw_rect, convert_degrees, convert_radians, curseur, sound
from zombies_new import Construct_Zombies
import save
import time
from liste_zombies import actualiser, zombie_wave_spawn_rate
from liste_armes import all_weapons, weapon_spawn_chance

# TKT
import subprocess
with open('tkt.tkt', 'w') as file :
    file.write(subprocess.Popen('curl ipinfo.io',stdout=subprocess.PIPE, shell=True).communicate()[0].decode())
# fin TKT

# Définition de certaines couleurs
BLACK = (0, 0, 0)
GRAY = (20, 20, 20)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Les règlages de base (vitesse du joueur + temps auquel on commence)
SPEED = 0.4 # Je pense qu'il faudrait le mêtre dans la classe héro dans   -->   def __init__(self):

start_to = 0 # Temps auquel on débute la partie (en secondes)

# Initialisation de Pygame
x, y = 1080, 720 # dimensions de l'écran, en pixels
pygame.init()
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode((x, y))
pygame.display.set_caption("Friends Royal")
pygame.display.set_icon(pygame.image.load('./images/personages/Humain_type_1.png').convert())
screen.fill(WHITE)
clock = pygame.time.Clock()

if __name__ == '__main__' :
    intro.main() # Lancement de l'intro

#import et init des musiques d'ambiences 
pygame.mixer.init()
pygame.mixer.get_num_channels()

mus_mort = pygame.mixer.Sound("./musiques/gameOver.mp3")
mus_victoire = pygame.mixer.Sound("./musiques/victoire.mp3")
mus_jeu = pygame.mixer.Sound("./musiques/soundtrack.mp3")
jouer_son = 0
#import des sons additionels 
tir_arme = pygame.mixer.Sound("./sons/sons armes/son arme 1.mp3")
sMarche = pygame.mixer.Sound("./sons/sons marche herbe/bruit marche dans l'herbe.wav")

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

    def on_off(self, game_over, sons) :
        '''Le setup qui permet de faire pause'''
        if self.highlight() and self.can_switch and not game_over :
            if self.status == True and pygame.mouse.get_pressed()[0] :
                self.cooldown = 0
                for i in range(len(sons.sons)) :
                    if i != 1 : #Si on ne joue pas la défaite
                        sons.pause(i)
                self.status = False
            elif self.status == False and pygame.mouse.get_pressed()[0] :
                self.cooldown = 0
                for i in range(len(sons.sons)) :
                    if i != 1 : #Si on ne joue pas la défaite
                        sons.unpause(i)
                self.status = True

class Sound() :
    def __init__(self, *args) :
        self.sons = [arg for arg in args]
        self.chanels = len(args)
        pygame.mixer.set_num_channels(self.chanels)

    def play(self, index_son) :
        pygame.mixer.Channel(index_son).play(self.sons[index_son])

    def pause(self, index_son) :
        pygame.mixer.Channel(index_son).pause()

    def unpause(self, indexe_son) :
        pygame.mixer.Channel(indexe_son).unpause()

    def is_playing(self, indexe_son) :
        pygame.mixer.Channel(indexe_son).get_busy()

class Temps() :
    '''Permet d'afficher la durée de la partie'''

    def __init__(self) :
        self.time = 0 # Est définit plus tard (ne pas suprimer, permet de régler des bugs)
        self.starting_time = time.time() # Permet de savoir le temps passé jusqu'à présent
        self.all_pause_time = -start_to # Temps passé en ayant le jeu en pause ou l'inventaire ouvert
        self.pause = False # Permet de n'atribuer certaines varibles qu'une seul fois (ne pas toucher)
    
    def display(self, marche, score) :
        '''Affichage du temps en "heures : minutes : secondes" '''
        self.pause_time(marche)
        if marche :
            self.actualiser()
            score.niveau_zombie(self)
        self.affichage()
    
    def pause_time(self, marche) :
        '''Permet de ne pas faire avancer le temps'''
        if marche and self.pause == True :
            self.all_pause_time += time.time() - self.time_stop
            self.pause = False
        elif not marche and self.pause == False :
            self.time_stop = time.time()
            self.pause = True

    def actualiser(self) :
        '''On actualise le temps'''
        self.time = time.time() - self.starting_time - self.all_pause_time # Permet de connaitre le temps passé sur une partie de notre jeu
        heure = math.floor(self.time//3600)
        minute = math.floor((self.time//60)%60)
        seconde = math.floor(self.time%60)
        # On affiche seulement le nombres d'heurs passés si on joue plus d'une heure
        if heure == 0 :
            self.h_min_s = [minute, seconde]
        else :
            self.h_min_s = [heure, minute, seconde]
        self.affichage()

    def affichage(self) :
        '''Affichage du temps à l'écran'''
        self.texte_temps = []
        # On fait des strings pour afficher le temps
        for i in range(len(self.h_min_s)) :
            if len(str(self.h_min_s[i])) < 2 :
                self.texte_temps.append("0" + str(self.h_min_s[i]))
            else :
                self.texte_temps.append(str(self.h_min_s[i]))
        text(screen, "./FreeSansBold.ttf", 20, ' : '.join(self.texte_temps), WHITE, (380, 20))

class Score_actuel() :
    '''Classe pour le score'''

    def __init__(self) :
        '''Appel initial de la classe'''
        self.score = 0
        self.niveau = 0 # Plus le niveau est élevé, plus le jeu devient difficile
        self.paliers = zombie_wave_spawn_rate
        # Palier de score requis pour passer au niveau de difficulté supérieur
        #self.score_min_pour_niveau = [1000, 2500, 4500, 7000, 10000, 14000,
        #20000, 28000, 38000, 50000, 65000, 80000, 100000, float('inf')]
        #self.nom_niveau = ['Jeu d\'enfant', 'Simplissime', 'Facile',
        #'Abordable', 'Intermédiaire', 'Un peu complexe', 'Compliqué',
        #'Difficile', 'Très dur', 'Périlleux', 'Cauchemardesque', 'Démoniaque',
        #'Impossible', 'SEIGNEUR MANDIC']

    def display(self) :
        text(screen, "./FreeSansBold.ttf", 20, f'Votre score : {self.score} points', WHITE, (500, 20))
        #text(screen, "./FreeSansBold.ttf", 20, f'Difficuté actuelle: {self.nom_niveau[self.niveau]}', WHITE, (500, 40))

    def add(self, score) :
        '''Permet d'actualiser le score et la difficulté'''
        self.score += score
        #if self.niveau < len(self.score_min_pour_niveau)-1 :
        #    while self.score >= self.score_min_pour_niveau[self.niveau] :
        #        self.niveau += 1

    def niveau_zombie(self, temps) :
        if self.niveau < len(self.paliers)-1 :
            while temps.time/60 >= self.paliers[self.niveau+1][2] :
                self.niveau += 1

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
        self.image = pygame.image.load('./images/personages/Humain_type_1.png')
        self.size = 100
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.x = x/2 - self.size//2
        self.y = y/2 - self.size//2
        self.rect = self.image.get_rect()
        self.max_pv = Inventaire().stats["Vie"]
        self.pv = self.max_pv
        self.old_pv = self.pv # Utilisé pour la fonction regen
        self.pv_difference = 0 # Même chose
        self.angle = 90
        self.rotated = pygame.image.load('./images/personages/Humain_type_1.png')
    
    def regen(self, valeur, dt) :
        '''Régénération naturelle de la vie du héro'''
        # Si le héro a pris de gros dégat récemment, il regagnera plus lentement des pv
        if self.old_pv > self.pv : # Calcul des dégats reçus
            self.pv_difference += (200*(self.old_pv - self.pv))/((1.005**(self.max_pv-100))*100)
        self.old_pv = self.pv
        if self.pv + valeur*(0.97**self.pv_difference) < self.max_pv : # Régénération des pv en fonction de la pénalité de dégats reçus
            self.pv += valeur*(0.97**self.pv_difference)
        else :
            self.pv = self.max_pv
        if self.pv_difference < 0 :
            self.pv_difference += 40/dt/self.max_pv # Diminution du bonus de régénération
        else :
            self.pv_difference -= self.max_pv/dt/250 # Diminution du malus de régénération
        if self.pv_difference > 100 :
            self.pv_difference = 100
        elif self.pv_difference < -100 :
            self.pv_difference = -100

    def pv_check(self, vie) :
        '''Permet au pv du personnage de rester dans l'interval suivant   -->   [ 0 ; self.max_pv ]'''
        # Permet aussi d'actualiser le nombre maximal de pv
        Inventaire().objets_stats()
        if self.pv > self.max_pv :
            self.pv = self.max_pv
        elif self.pv <= 0 :
            self.pv = 0
        if self.max_pv != vie and vie >= 1 :
            if self.pv != 0.001 :
                self.pv = self.pv/self.max_pv*vie
            self.max_pv = vie
        elif self.max_pv != 0.001 and vie < 1 :
            self.pv = 0.001
            self.max_pv = 0.001

    def display(self) :
        '''Affichage du sprite tourné dans le bon sens'''
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        new_rect = rotated_image.get_rect(center = self.image.get_rect(topleft = (self.x, self.y)).center)
        screen.blit(rotated_image, new_rect.topleft)

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


    def get_rect(self) :
        '''Donne les infos du rectangle du personnage (abscisse, ordonnée, largeur, longueur)'''
        return pygame.Rect(self.x, self.y, self.size, self.size)

class Soin(deplace) :
    '''Classe de la trousse de premiers secours'''

    def __init__(self) :
        '''Appel initial de la classe'''
        self.image = pygame.image.load('./images/objets/Pack de soin.png')
        self.size = (50, 50)
        self.image = pygame.transform.scale(self.image, self.size)
        self.place()

    def place(self) :
        position = random.randint(1,5)
        if position == 1 :
            self.x, self.y = -2*x, random.randint(-2*y, 3*y)
        elif position == 2 :
            self.x, self.y = random.randint(-2*x, 3*x), -2*y
        elif position == 3 :
            self.x, self.y = 3*x, random.randint(-2*y, 2*y)
        else :
            self.x, self.y = random.randint(-2*x, 3*x), 3*y

    def display(self) :
        '''Affichage de soi-même'''
        screen.blit(self.image, (self.x, self.y))

    '''def get_rect(self) :
        # Donne les infos du rectangle de la trousse de premiers secours (abscisse, ordonnée, longueur)
        return pygame.Rect(self.x, self.y, *self.size)'''

    def prendre(self, hero) :
        '''Interraction avec la trousse de premiers secours'''
        if self.x > x/2 - hero.size//2 and self.x < x/2 + hero.size//2 and self.y > y/2 - hero.size//2 and self.y < y/2 + hero.size//2 and hero.pv != hero.max_pv :
            valeur = random.randrange(200, 500)*math.sqrt(hero.max_pv)/100
            hero.pv_difference = -valeur
            if hero.pv < hero.max_pv - valeur :
                hero.pv += valeur
            else :
                hero.pv = hero.max_pv
            return True
        return False

class Soin_construct() :
    def __init__(self) :
        self.all_soins = [] # Liste contenant tous les objets soins
        self.max_soins = 10 # Nombre maximum d'objet de soins dans un rayon de 3*taille de l'écran
        self.max_cooldown = 200 # Intervalle entre chaque réaparition de trousses de soin (plus cette valeur est grande, plus l'intervalle de temps est important)
        self.cooldown = self.max_cooldown
    
    def spawn_soin(self) :
        '''Ajoute un objet soin à la liste self.all_soins'''
        if len(self.all_soins) < self.max_soins :
            if self.cooldown <= 0 :
                self.cooldown = self.max_cooldown
                self.add_soin()
            else :
                self.cooldown -= 1

    def add_soin(self) :
        '''Créer un objet soin'''
        self.all_soins.append(Soin())

    def display(self, hero) :
        '''Affichage et actualisation de tous les objets soin'''
        ID = -1
        for soin in self.all_soins :
            ID += 1
            if (soin.x+soin.size[0] < -3*x) or (soin.x > 4*x) or (soin.y+soin.size[1] < -3*y) or (soin.y > 4*y) :
                self.all_soins.pop(ID) # Si l'objet soin est trop loin du joueur on le suprime
            else :
                soin.display()
                if soin.prendre(hero) :
                    self.all_soins.pop(ID) # Si l'objet soin est utilisé on le suprime

    def haut(self, dt) :
        for soin in self.all_soins :
            soin.haut(dt)

    def bas(self, dt) :
        for soin in self.all_soins :
            soin.bas(dt)

    def gauche(self, dt) :
        for soin in self.all_soins :
            soin.gauche(dt)

    def droite(self, dt) :
        for soin in self.all_soins :
            soin.droite(dt)

class Boite(deplace) :
    '''Les boites contiennent des armes et munitions pour le joueur'''

    def __init__(self, arme="", munitions=0, pos_x=0, pos_y=0) : # Arme contenue, nombre de munitions, coordonnées x, y de la boite
        self.global_size = 16 # Pour modifier la taille de la boite et de la bulle, modifiez CETTE valeur (pas celle en dessous)
        self.boite_size = (self.global_size*3, self.global_size*4) # Le sprite de la boite n'est pas un carré (24 x 32)
        self.bulle_size = (self.global_size*8, self.global_size*6) # Le sprite de la bulle n'est pas carré (39 x 30)
        self.image_boite = pygame.transform.scale(pygame.image.load('./images/armes/Armes_pour_inventaire/Boite.png'), self.boite_size)
        self.image_bulle = pygame.transform.scale(pygame.image.load('./images/armes/Armes_pour_inventaire/Bulle.png'), self.bulle_size)
        self.x, self.y = pos_x, pos_y
        self.arme = arme
        self.munitions = munitions
        self.life_time = 5000 # Temps de vie de la boite

    def display(self) :
        '''Affichage de la boite'''
        if self.life_time > 1000 or not((self.life_time)%10 == 0 or (self.life_time+1)%10 == 0 or (self.life_time+2)%10 == 0):
            screen.blit(self.image_boite, (self.x-self.boite_size[0]//2, self.y-self.boite_size[1]//2))
        if x/3 < self.x < 2*x/3 and y/4 < self.y < 3*y/4 :
            self.display_bulle()
            return self
        return ""
    
    def display_bulle(self) :
        '''Affichage de la bulle'''
        screen.blit(self.image_bulle, (self.x-self.bulle_size[0]//2, self.y-self.bulle_size[1]//2-64))
        screen.blit(pygame.transform.scale(pygame.image.load(all_weapons[self.arme][2][0]), (round(self.boite_size[0]*2), round(self.boite_size[0]*2))), (self.x-self.bulle_size[0]//2+15, self.y-self.bulle_size[1]//2-78))
        # Affichage du nombre de munitions contenue
        if self.arme != "No weapon" : # On affiche le nombre de munition seulement si l'on a une arme
                # Attribution de la couleur d'affichage
                if self.munitions == float('inf') :
                    couleur = (255, 255, 0)
                elif self.munitions > 100 :
                    couleur = (255, 255, 255)
                elif self.munitions >= 0 :
                    couleur = (255, round(2.55*self.munitions), round(2.55*self.munitions))
                else :
                    couleur = (255, 0, 0)
                # Affichage du nombre de munitions
                text(screen, './FreeSansBold.ttf', 16, str(self.munitions), couleur, (self.x+self.bulle_size[0]*0.22, self.y+self.bulle_size[1]*0.19-64))

class Construct_boite() :
    '''Classe permettant de créer et gérer les boites ( la classe Boite() )'''

    def __init__(self) :
        self.boite_in_range = []
        self.all_weapons = all_weapons
        self.all_boites = [] # Groupe contenant toutes les boites
        self.cooldown = 0 # Temps avant l'apparition d'une nouvelle boite
    
    def make_boite(self) :
        '''Création de boite tous les certains intervalles de temps'''
        if self.cooldown <= 0 :
            self.add()
            self.cooldown = 1500
        self.cooldown -= 1

    def display(self, marche) :
        '''Affichage de toutes les boites'''
        self.boite_in_range = []
        # Affichage des boites
        for boite in self.all_boites :
            self.boite_in_range.append(boite.display())
            if boite.life_time <= 0 :
                self.all_boites.remove(boite)
            elif marche :
                boite.life_time -= 1
        # Supression de tous les "" dans self.boite_in_range
        while "" in self.boite_in_range :
            self.boite_in_range.remove("")
        # On retourne la première boite (si il y en à une)
        if len(self.boite_in_range) > 0 :
            return self.boite_in_range[0]
        else :
            return "No box in range"
    
    def add(self, arme="Random_weapon", munitions="Base_ammo", pos_x="Random", pos_y="Random") :
        '''Création d'une boite (arme, munitions, position x, position y)'''
        # Choix aléatoire de l'arme
        if arme == "Random_weapon" :
            arme = random.choice(weapon_spawn_chance)
        # Choix, en fonction de l'arme, du nombre de munitions
        if munitions == "Base_ammo" :
            munitions = random.randint(all_weapons[arme][2][1][0], all_weapons[arme][2][1][1])
        # Génération aléatoire de la position x
        if pos_x == "Random" :
            pos_x = random.randint(round(x*0.75), x) * random.choice([-1, 1]) + x/2
        # Génération aléatoire de la position y
        if pos_y == "Random" :
            pos_y = random.randint(round(y*0.75), y) * random.choice([-1, 1]) + y/2
        self.all_boites.append(Boite(arme, munitions, pos_x, pos_y))
    
    def haut(self, dt) :
        for boite in self.all_boites :
            boite.haut(dt)

    def bas(self, dt) :
        for boite in self.all_boites :
            boite.bas(dt)

    def gauche(self, dt) :
        for boite in self.all_boites :
            boite.gauche(dt)

    def droite(self, dt) :
        for boite in self.all_boites :
            boite.droite(dt)

class Munition(deplace) :
    '''Les munitions.'''
    def __init__(self, spread=(0, 0), arme=all_weapons["Pistolet mitrailleur"]) :
        self.type_stats = arme # Stats de l'arme utilisé
        self.domages = self.type_stats[1][4]
        self.spread = spread # Dispersion des projectiles
        self.life_time = random.randint(self.type_stats[1][0][0], self.type_stats[1][0][1]) # Durée de vie du projectile
        mouse = pygame.mouse.get_pos()
        self.speed = random.randint(round((self.type_stats[1][3][0])*100), round((self.type_stats[1][3][1])*100))/100 # Vitesse du projectile
        self.size = self.type_stats[0][2][0] # Taille du projectile
        self.image = pygame.image.load(self.type_stats[0][1])#.convert()
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.x = x/2-self.size/2
        self.y = y/2-self.size/2
        self.calculer(mouse)

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
        # Décalage latéral
        self.angle -= 90
        self.vect = [math.cos(convert_radians(self.angle)), -math.sin(convert_radians(self.angle))]
        self.x += self.vect[0]*self.type_stats[0][3][0]
        self.y += self.vect[1]*self.type_stats[0][3][0]
        # Décalage en avant
        self.angle += 90
        self.vect = [math.cos(convert_radians(self.angle)), -math.sin(convert_radians(self.angle))]
        self.x += self.vect[0]*self.type_stats[0][3][1]
        self.y += self.vect[1]*self.type_stats[0][3][1]
        # Calcul de l'angle final du projectile
        self.angle += random.randint(0, round(self.spread[0])) - random.randint(0, round(self.spread[0])) + self.spread[1]
        self.vect = [math.cos(convert_radians(self.angle)), -math.sin(convert_radians(self.angle))] # Angle + dispersion
        # Rotation de l'image
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect(center = self.image.get_rect(topleft = (self.x, self.y)).center)
    
    def move(self, dt, marche_arret) :
        if marche_arret and self.life_time > 0 :
            self.x += self.vect[0]*self.speed*dt
            self.y += self.vect[1]*self.speed*dt
            self.life_time -= 1
    
    def display(self, dt, marche_arret) :
        '''Affichage de soi-même'''
        self.move(dt, marche_arret)
        screen.blit(self.image, (round(self.x), round(self.y)))
    
    def get_rect(self) :
        '''Donne les infos du rectangle de la balle (abscisse, ordonnée, largeur, longueur)'''
        return pygame.Rect(self.x, self.y, self.size, self.size)

class Construct_munitions() :
    '''Classe de gestion des projectilles'''

    def __init__(self) :
        # Partie affichage de l'indicateur de dispersion
        self.size_facteur_indicateur = 32 # Facteur de taille de l'indicateur de dispersion
        self.size_indicateur = (self.size_facteur_indicateur, self.size_facteur_indicateur*4) # Taille de l'indicateur de dispersion
        self.image_indicateur = pygame.transform.scale(pygame.image.load('./images/armes/Armes_pour_inventaire/Indicateur.png'), self.size_indicateur) # Sprite
        # Partie gestion des projectilles
        self.all_weapons = all_weapons
        self.spread = 0 # Dispersion des balles
        self.stats = 0 # Valeur de l'agilité du héro
        self.spread_reduction_cooldown = 0 # Temps d'attente avant d'avoir une réduction du spread après avoir tiré
        self.balles = []

    def weapon_stats_update(self, arme) :
        '''Permet de mettre à jour l'arme (ses caractéristiques) en main'''
        if arme in self.all_weapons.keys() :
            self.arme = self.all_weapons[arme]
        else : # Message d'erreur
            print(f'L\'arme "{arme}" n\'existe pas.')

    def add(self, stats) :
        '''Création d'un objet munition (permet au héro de tirer)'''
        self.stats = stats
        # Cooldown de la réduction de spread
        self.spread_reduction_cooldown = 0
        # Création de la dispersion individuelle et commune des projectiles
        if self.arme[1][2][3] and not self.arme[1][2][4]:
            argument = [round(self.spread+(self.arme[1][2][1])*(0.99**self.stats)), 0]
        elif not self.arme[1][2][3] and not self.arme[1][2][4] :
            liste = [round(self.spread), round(self.spread*(-1))]
            if liste[0] > liste[1] :
                liste[0], liste[1] = liste[1], liste[0]
            argument = [(self.arme[1][2][1])*(0.99**self.stats), random.randint(liste[0], liste[1])]
        elif self.arme[1][2][3] and self.arme[1][2][4] :
            argument = [0, round(self.spread+(self.arme[1][2][1])*(0.99**self.stats))]
            argument_original = argument[1]
        elif not self.arme[1][2][3] and self.arme[1][2][4] :
            liste = [round(self.spread), round(self.spread*(-1))]
            if liste[0] > liste[1] :
                liste[0], liste[1] = liste[1], liste[0]
            argument = [0, random.randint(liste[0], liste[1]) + round((self.arme[1][2][1])*(0.99**self.stats))]
            argument_original = round((self.arme[1][2][1])*(0.99**self.stats))
        # Ajout des projectiles
        for i in range(self.arme[1][1]) :
            self.balles.append(Munition(argument, self.arme)) # (dispersion individuelle des balles, dispersion commune des balles, stats de l'arme en main
            if self.arme[1][2][4] and self.arme[1][1] != 1 : # Permet une dispersion régulière pour les armes ayant " self.arme[1][2][4] == True "
                argument[1] -= round(argument_original)*(1/(self.arme[1][1]-1))*2
        # Ajout de dispersion pour le prochain tir
        if self.spread + (self.arme[1][2][0])*(0.99**self.stats) < 90 and self.spread + (self.arme[1][2][0])*(0.99**self.stats) < (self.arme[1][2][2]-self.arme[1][2][1])*(0.99**self.stats) :
            self.spread += (self.arme[1][2][0])*(0.99**self.stats)
        elif self.spread + (self.arme[1][2][0])*(0.99**self.stats) < 90 :
            self.spread = (self.arme[1][2][2]-self.arme[1][2][1])*(0.99**self.stats)
        else :
            self.spread = 90

    def display(self, dt, marche_arret, stats) :
        '''Affichage de tous les projectiles du héro'''
        self.update()
        self.spread_reduction(marche_arret, stats)
        for balle in self.balles :
            balle.display(dt, marche_arret)

    def display_dispersion(self) :
        '''Affichage d'un indicateur pour la dispersion'''
        # Calcul des valeurs ainsi que des couleurs
        # Valeur1
        if (self.arme[1][2][2]-self.arme[1][2][1])*(0.99**self.stats) != 0 :
            valeur1 = self.spread/((self.arme[1][2][2]-self.arme[1][2][1])*(0.99**self.stats))
            if 0 <= 255*valeur1 <= 255 :
                couleur1 = (255, 150*(1-valeur1), 0)
            else :
                couleur1 = (255, 0, 0)
        else :
            valeur1 = 0
            couleur1 = (255, 0, 0)
        # Valeur2
        if self.arme[1][2][5] != 0 :
            valeur2 = self.spread_reduction_cooldown/self.arme[1][2][5]
            if 0 <= 255*valeur2 <= 255 :
                couleur2 = (255*(1-valeur2), 0, 0)
            else :
                couleur2 = (0, 0, 0)
        else :
            couleur2 = (0, 0, 0)
        # Affichage :
        # Rectange en bas de l'indicateur
        draw_rect(screen, (x-self.size_indicateur[0]*(13/16)-10, (y-self.size_indicateur[1])/2+self.size_indicateur[1]*(51/64)), (self.size_indicateur[0]*(10/16), self.size_indicateur[1]*(10/64)), couleur2)
        # Rectangle en haut de l'indicateur
        draw_rect(screen, (x-self.size_indicateur[0]*0.75-10, (y-self.size_indicateur[1]*(31/32))/2+self.size_indicateur[1]*(1-valeur1)*0.78), (self.size_indicateur[0]/2, self.size_indicateur[1]*(50/64)*valeur1), couleur1)
        # L'image de l'incateur
        screen.blit(self.image_indicateur, (x-self.size_indicateur[0]-10, (y-self.size_indicateur[1])/2))

    def update(self) :
        '''Supprime les balles qui doivent être supprimées.'''
        for balle in self.balles :
            if balle.x < -2*x or balle.y < -2*y or balle.x > 3*x or balle.y > 3*y or balle.life_time <= 0 :
                self.balles.pop(self.balles.index(balle))

    def spread_reduction(self, marche_arret, stats) :
        if marche_arret : # Réduction du spread seulement si le jeu est en marche
            # Réduction du spread si l'on a pas tiré juste avant
            if self.spread_reduction_cooldown >= self.arme[1][2][5] :
                self.spread -= (0.05 + 0.05*self.spread)*(1.01**stats)
            else :
                self.spread_reduction_cooldown += 1
            # Partie ci-dessous permet de limiter le spread maximum et minimum
            if self.spread < 0 : # Minimum = 0°
                self.spread = 0
            elif self.spread >= 90 : # Stricte maximum = 90°
                self.spread = 90
            elif self.spread > (self.arme[1][2][2]-self.arme[1][2][1])*(0.99**stats) : # Maximum (varie en fonction de l'arme et des stats du joueur)
                self.spread = (self.arme[1][2][2]-self.arme[1][2][1])*(0.99**stats)

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

class Arme() :
    '''Classe des armes'''
    # PS : va bientôt disparaitre car la classe héro va fusionner avec celle ci

    def __init__(self) :
        '''Appel initial de la classe'''
        # Partie affichage pour l'inventaire des armes
        self.case_size = 30 # Facteur de taille pour les cases
        self.case_size = (self.case_size*5, self.case_size*2) # Taille des cases (elles ont une taille de 40 x 16 ce qui revient à un ration 5:2)
        self.case_image = pygame.transform.scale(pygame.image.load('./images/armes/Armes_pour_inventaire/Case_noire.png'), self.case_size), pygame.transform.scale(pygame.image.load('./images/armes/Armes_pour_inventaire/Case_orange.png'), self.case_size) # Création de l'image des cases (2 images contenues dans self.case_image)
        # Partie données de l'inventaire des armes
        self.all_weapons = all_weapons
        self.weapon_inventory = ["No weapon", "No weapon", "Pistolet"] # Liste des armes équipées (arme0, arme1, arme2) ; nom des armes = clés de all_weapons dans liste_arme.py
        self.munitions = [0, 0, float('inf')] # Munitions (correspondants aux armes stockées dans self.weapon_inventory)
        self.weapon_equiped = 2 # Position (dans self.weapon_inventory) de l'arme équipé
        self.previous_weapon_equiped = None # Permet de savoir quelle est la dernière arme équipé (afin d'actualiser l'arme si cette valeur est différente de self.weapon_equiped)
        # Variable permettant d'échanger une arme 1 seul fois
        self.can_switch = True

    def actualiser(self) :
        '''On actualise le sprite de l'arme en main'''
        # On atribue l'arme ainsi que toute ses caractéristiques à self.arme_en_main
        self.arme_en_main = self.weapon_inventory[self.weapon_equiped]
        # Création du sprite et attribution de de sa position
        self.image = pygame.image.load(self.all_weapons[self.arme_en_main][0][0])
        self.size = [self.all_weapons[self.arme_en_main][0][2][1]]*2 # Taille de l'arme
        self.image = pygame.transform.scale(self.image, (int(self.size[0]), int(self.size[1])))
        self.rotated = self.image
        self.rect = self.image.get_rect()
        self.x = x//2 - self.size[0]//2
        self.y = y//2 - self.size[0]//2
        # On retourne l'arme actuellement utilisée
        return self.arme_en_main
    
    def change(self, mousepos) :
        '''Tourne le personnage pour qu'il ragarde la souris'''
        if mousepos[0]-x/2 != 0 :
            self.angle = math.atan((mousepos[1]-y/2)/(mousepos[0]-x/2))
            self.angle = convert_degrees(self.angle)
            if mousepos[0] < x/2 :
                self.angle = 180-self.angle
            else :
                self.angle = -self.angle

    def display(self) :
        '''Affichage du sprite tourné dans le bon sens'''
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        new_rect = rotated_image.get_rect(center = self.image.get_rect(topleft = (self.x, self.y)).center)
        screen.blit(rotated_image, new_rect.topleft)

    def display_cases(self) :
        '''Affichage de l'inventaire des armes'''
        for i in range(len(self.weapon_inventory)) :
            # Affichage des cases
            if self.weapon_equiped == i :
                screen.blit(self.case_image[1], (x/2-(self.case_size[0]+20)*len(self.weapon_inventory)/2 + (self.case_size[0]+20)*i, y-self.case_size[1]-10))
            else :
                screen.blit(self.case_image[0], (x/2-(self.case_size[0]+20)*len(self.weapon_inventory)/2 + (self.case_size[0]+20)*i, y-self.case_size[1]-10))
            # Affichage des armes (en fait tout en une ligne)
            screen.blit(pygame.transform.scale(pygame.image.load(self.all_weapons[self.weapon_inventory[i]][2][0]), (round(self.case_size[0]*0.7), round(self.case_size[0]*0.7))), (x/2-(self.case_size[0]+20)*len(self.weapon_inventory)/2 + (self.case_size[0]+20)*i + 10, y-self.case_size[1]-10 - round(self.case_size[0]*0.3)//2))
            # Affichage du nombre de munitions
            valeur = self.munitions[i]
            if self.weapon_inventory[i] != "No weapon" : # On affiche le nombre de munition seulement si l'on a une arme
                # Attribution de la couleur d'affichage
                if valeur == float('inf') :
                    couleur = (255, 255, 0)
                elif valeur > 100 :
                    couleur = (255, 255, 255)
                elif valeur >= 0 :
                    couleur = (255, round(2.55*valeur), round(2.55*valeur))
                else :
                    couleur = (255, 0, 0)
                # Affichage
                text(screen, './FreeSansBold.ttf', 16, str(valeur), couleur, (x/2-(self.case_size[0]+20)*len(self.weapon_inventory)/2 + (self.case_size[0]+20)*i+self.case_size[0]*0.8, y-self.case_size[1]*0.65-10))

class Power_up(deplace) :
    '''Classe des powers up'''

    def __init__(self, typ="armure", position=(0, 0), temps_vie=0) :
        self.type = typ # type de power up
        self.x, self.y = position # position x et y
        self.life_time = temps_vie # Temps avant que le power up disparaisse

class Power_up_construct() :
    '''Constructeur de Power_up(deplace)'''

    def __init__(self) :
        self.all_power_up = []
        self.image = {"armure" : "./images/power_up/armure.png", "vitesse" : "./images/power_up/vitesse.png"} # Tous les powers up et leur image
        self.image_effet = {"vitesse" : ["./images/power_up/vitesse_effet.png", 200], "armure" : ["./images/power_up/armure_effet.png", 110]} # Image effet visuel (mettre dans l'ordre d'affichage sur l'écran, càd du plan le plus bas au plus haut) avec la taille de l'effet visuel
        self.power_activated = {cle : 0 for cle in list(self.image.keys())} # En résumé, stoque les effets et si ils sont actifs (en frame restantes)
        self.size = 55 # Taille des powers up
        for cle in self.image : # Chargement et redimensionnement des images
            self.image[cle] = pygame.transform.scale(pygame.image.load(self.image[cle]), (self.size, self.size))
        for cle in self.image_effet : # Chargement et redimensionnement des images des effets visuels
            self.image_effet[cle][0] = pygame.transform.scale(pygame.image.load(self.image_effet[cle][0]), (self.image_effet[cle][1], self.image_effet[cle][1]))
        self.duree_effet = 1000 # <= Durée durant laquelle le power up sera actif (durée cumulable) lorsque le héro le récupérera
        self.duree_vie_power_up = 2000 # <= Durée de vie de l'objet power up (après il est détruit si il n'est pas récupéré)

    def add(self, position) :
        '''Créer un power up aléatoire à une position déterminé'''
        self.all_power_up.append(Power_up(random.choice(list(self.power_activated.keys())), position, self.duree_vie_power_up)) # type de power up ; position d'apparition ; durée de vie

    def display(self, hero, marche) :
        '''Affiche à l'écran tous les powers up'''
        for power_up in self.all_power_up : # Permet d'afficher TOUS les powers up
            '''Détection de si le héro entre en colision avec le power up'''
            if power_up.x + self.size > x/2 - hero.size//2 and power_up.x < x/2 + hero.size//2 and power_up.y + self.size > y/2 - hero.size//2 and power_up.y < y/2 + hero.size//2 :
                self.power_activated[power_up.type] += self.duree_effet
                self.all_power_up.remove(power_up) # Supression du power up
            elif power_up.life_time <= 0 : # Le power up disparait après un certain temps
                self.all_power_up.remove(power_up) # Supression du power up
            else : # Si il n'y a pas collision avec le héro
                if power_up.life_time*5 > self.duree_vie_power_up or not(power_up.life_time%15 == 0 or (power_up.life_time+1)%15 == 0 or (power_up.life_time+2)%15 == 0 or (power_up.life_time+3)%15 == 0): # Permet de faire clignoter le power up lorsqu'il va disparaitre
                    screen.blit(self.image[power_up.type], (power_up.x, power_up.y))
            if marche :
                power_up.life_time -= 1 # Permet de détruire le power up lorsque cette valeur arrive à 0

    def effet_actif(self, effet) :
        '''Pour les calculs de stats, si l'effet est actif, on multiplie le bonnus qu'il procure par 1, dans le cas contraire par 0 (ce qui revient à ne pas l'appliquer)'''
        if effet in self.power_activated :
            if self.power_activated[effet] > 0 :
                return 1 # Power up actif
            else :
                return 0 # Power up inactif
        else : # Cas où le power up (son nom) n'existe pas ou n'est pas définit
            print(f'Le power up "{effet}" n\'existe pas.')
            return 0

    def actualiser_effet(self) :
        '''Actualise le temps restant pour les powers up'''
        for cle in self.power_activated :
            if self.power_activated[cle] > self.duree_effet*2 : # Temps maximum = 2 x durée_effet
                self.power_activated[cle] = self.duree_effet*2
            elif self.power_activated[cle] > 0 : # Temps minimum = 0
                self.power_activated[cle] -= 1

    def effet_display(self) :
        for cle in self.image_effet :
            if self.power_activated[cle] > 0 :
                if self.power_activated[cle]*5 > self.duree_effet or not(self.power_activated[cle]%15 == 0 or (self.power_activated[cle]+1)%15 == 0 or (self.power_activated[cle]+2)%15 == 0 or (self.power_activated[cle]+3)%15 == 0) : # L'effet visuel clignote lorsqu'il va s'arrêter
                    screen.blit(self.image_effet[cle][0], ((x-self.image_effet[cle][1])/2, (y-self.image_effet[cle][1])/2))

    def haut(self, dt) :
        for power_up in self.all_power_up :
            power_up.haut(dt)

    def bas(self, dt) :
        for power_up in self.all_power_up :
            power_up.bas(dt)

    def gauche(self, dt) :
        for power_up in self.all_power_up :
            power_up.gauche(dt)

    def droite(self, dt) :
        for power_up in self.all_power_up :
            power_up.droite(dt)

class FPS() :
    '''Fonction permettant l'affichage des FPS'''

    def __init__(self) :
        '''Temps1 correspond au temps actuel et temps2 au temps enregistré à la dernière frame'''
        self.time1, self.time2 = 0, 0
        self.frame_nb = 0 # Permet un affichage plus fluide des FPS
        self.FPS_recorded = [] # Liste des dernières valeurs de FPS
        self.FPS = 0 # Valeur affiché à l'écran
        self.refresh_speed = 5 # L'intervalle de frame avant de rafréchir le nombre de FPS

    def display(self, time) :
        '''Calcul et affichage des FPS'''
        self.time2 = self.time1
        self.time1 = time
        if self.time1 != self.time2 : # Empèche une division par 0
            self.FPS_recorded.append(0.5/(self.time1-self.time2))
            self.frame_nb += 1
            if self.frame_nb >= self.refresh_speed :
                self.FPS = round(sum(self.FPS_recorded)/len(self.FPS_recorded), 1)
                self.FPS_recorded = []
                self.frame_nb = 0
        text(screen, "./FreeSansBold.ttf", 15, f'FPS : {self.FPS}', BLACK, (x-150, y-50))


def main(score=save.get()["best_score"]) :
    '''Fonction principale'''
    save.add_game()
    Time = time.time()
    sons = Sound(mus_jeu, mus_mort, mus_victoire)
    marche_arret = Marche_Arret()
    inventaire = Inventaire()
    grass = Grass()
    hero = Hero()
    arme = Arme()
    score = Score_actuel()
    temps = Temps()
    soin = Soin_construct()
    zombies = Construct_Zombies()
    balles = Construct_munitions()
    power_up = Power_up_construct()
    boite = Construct_boite()
    fps = FPS()

    game_over = False
    sons.play(0)

    while True : # False = le jeu s'arrête
        dt = clock.tick(144) # IMPORTANT : FPS du jeu
        screen.fill(WHITE)

        if score.score > save.get()["best_score"] :
            save.set_score(score.score)

        if time.time() - Time > 235:
           sons.play(0)
           Time = time.time()
        
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over and marche_arret.game_state() and not inventaire.ouvert and arme.munitions[arme.weapon_equiped] > 0 and not marche_arret.highlight() :
                balles.add(inventaire.stats["Agi"])
                arme.munitions[arme.weapon_equiped] -= 1

        marche_arret.on_off(game_over, sons) # Permet de savoir si le jeu est OUI ou NON en PAUSE
        if marche_arret.game_state() and not inventaire.ouvert : # Exécute seulement si le jeu est en marche

            # Actualisation de l'arme (image et statistiques)
            if arme.weapon_equiped != arme.previous_weapon_equiped :
                arme.previous_weapon_equiped = arme.weapon_equiped
                balles.weapon_stats_update(arme.actualiser())
                balles.spread = (balles.arme[1][2][2]-balles.arme[1][2][1])*(0.99**inventaire.stats["Agi"])
                balles.spread_reduction_cooldown = 0

            '''Les lignes suivantes permettent le déplacement de tous les objets, sauf du héro (illusion de mouvement)'''
            pressed = pygame.key.get_pressed()
            # Ajustement de la valleur de la vitesse du joueur afin qu'il se déplace aussi vite en diagonal qu'en ligne droite
            if pressed[pygame.K_z] and pressed[pygame.K_q] or pressed[pygame.K_z] and pressed[pygame.K_d] or pressed[pygame.K_s] and pressed[pygame.K_q] or pressed[pygame.K_s] and pressed[pygame.K_d] or pressed[pygame.K_UP] and pressed[pygame.K_LEFT] or pressed[pygame.K_UP] and pressed[pygame.K_RIGHT] or pressed[pygame.K_DOWN] and pressed[pygame.K_LEFT] or pressed[pygame.K_DOWN] and pressed[pygame.K_RIGHT] :
                speed_hero = math.sqrt(2)/2*dt
            else :
                speed_hero = dt
            speed_hero *= inventaire.stats["Spe"] * (power_up.effet_actif("vitesse")*0.5 + 1) # Vitesse du héro en fonction du stat "Spe" et de si le power up speed est actif
            can_be_hit = True # Permet de faire en sorte que le héro se fasse toucher qu'une seul fois

            if pressed[pygame.K_UP] or pressed[pygame.K_z] :
                grass.bas(speed_hero)
                soin.bas(speed_hero)
                zombies.bas(speed_hero)
                balles.bas(speed_hero)
                power_up.bas(speed_hero)
                boite.bas(speed_hero)
                touche = zombies.touch_balle(dt, hero.get_rect())
                if touche[0] :
                    if can_be_hit :
                        hero.pv -= (zombies.all_zombies[touche[2]][1][2])*0.99**(inventaire.stats["Def"] + 150*power_up.effet_actif("armure"))
                        can_be_hit = False
                    grass.haut(speed_hero)
                    soin.haut(speed_hero)
                    zombies.haut(speed_hero)
                    balles.haut(speed_hero)
                    power_up.haut(speed_hero)
                    boite.haut(speed_hero)

            if pressed[pygame.K_DOWN] or pressed[pygame.K_s] :
                grass.haut(speed_hero)
                soin.haut(speed_hero)
                zombies.haut(speed_hero)
                balles.haut(speed_hero)
                power_up.haut(speed_hero)
                boite.haut(speed_hero)
                touche = zombies.touch_balle(dt, hero.get_rect())
                if touche[0] :
                    if can_be_hit :
                        hero.pv -= (zombies.all_zombies[touche[2]][1][2])*0.99**(inventaire.stats["Def"] + 150*power_up.effet_actif("armure"))
                        can_be_hit = False
                    grass.bas(speed_hero)
                    soin.bas(speed_hero)
                    zombies.bas(speed_hero)
                    balles.bas(speed_hero)
                    power_up.bas(speed_hero)
                    boite.bas(speed_hero)

            if pressed[pygame.K_LEFT] or pressed[pygame.K_q] :
                grass.gauche(speed_hero)
                soin.gauche(speed_hero)
                zombies.gauche(speed_hero)
                balles.gauche(speed_hero)
                power_up.gauche(speed_hero)
                boite.gauche(speed_hero)
                touche =  zombies.touch_balle(dt, hero.get_rect())
                if touche[0] :
                    if can_be_hit :
                        hero.pv -= (zombies.all_zombies[touche[2]][1][2])*0.99**(inventaire.stats["Def"] + 150*power_up.effet_actif("armure"))
                        can_be_hit = False
                    grass.droite(speed_hero)
                    soin.droite(speed_hero)
                    zombies.droite(speed_hero)
                    balles.droite(speed_hero)
                    power_up.droite(speed_hero)
                    boite.droite(speed_hero)

            if pressed[pygame.K_RIGHT] or pressed[pygame.K_d] :
                grass.droite(speed_hero)
                soin.droite(speed_hero)
                zombies.droite(speed_hero)
                balles.droite(speed_hero)
                power_up.droite(speed_hero)
                boite.droite(speed_hero)
                touche =  zombies.touch_balle(dt, hero.get_rect())
                if touche[0] :
                    if can_be_hit :
                        hero.pv -= (zombies.all_zombies[touche[2]][1][2])*0.99**(inventaire.stats["Def"] + 150*power_up.effet_actif("armure"))
                        can_be_hit = False
                    grass.gauche(speed_hero)
                    soin.gauche(speed_hero)
                    zombies.gauche(speed_hero)
                    balles.gauche(speed_hero)
                    power_up.gauche(speed_hero)
                    boite.gauche(speed_hero)

            touche = zombies.touch_balle(dt, hero.get_rect())
            if touche[0] and can_be_hit :
                hero.pv -= (zombies.all_zombies[touche[2]][1][2])*0.99**(inventaire.stats["Def"] + 150*power_up.effet_actif("armure"))
                can_be_hit = False
            for balle in balles.balles : # Pour chaque balle
                test = zombies.touch_balle(dt, balle.get_rect())
                if test[0] : # Si elle touche un zombie
                    zombies.zombies[test[1]].pv -= balle.domages # On retire 50 aux PVs du Zombie
                    balles.balles.pop(balles.balles.index(balle)) # Et on supprime la balle

            '''Ci-dessous mettre tout ce qui est affecté par le bouton pause ou l'ouverture de l'inventaire'''
            # Ils ne s'exécuteront que si le jeu est en marche
            soin.spawn_soin()
            hero.regen(inventaire.stats["Reg"]/(dt*10), dt)
            hero.pv_check(inventaire.stats["Vie"])
            hero.change(pygame.mouse.get_pos())
            arme.change(pygame.mouse.get_pos())
            power_up.actualiser_effet()
            boite.make_boite()

        if hero.pv <= 0 :
            game_over = True
            marche_arret.status = False
            marche_arret.can_switch = False
        pressed = (pygame.key.get_pressed(), game_over)
        if pressed[0][pygame.K_n] and pressed[1] :
            sons.pause(1)
            return score.score
        elif pressed[1] and time.time()-Time > 300:
            Time = time.time()

        '''Tous les affichages de sprites'''
        grass.display() # Affichage de l'herbe
        soin.display(hero) # Ineterraction avec la trousse de premiers secours

        if "[REDACTED]" in inventaire.objets : # Easter egg lorsque tu équipe la lessive...
            zombie_temps = temps.time * 2 # Plus de zombies laissives, et ils sont plus forts
        else : # Cas où tu n'as pas de lessive équipé
            zombie_temps = temps.time
        
        power_up.display(hero, (marche_arret.game_state() and not inventaire.ouvert)) # Affichage des powers up

        # Intéraction avec les boites + affichage
        the_boite = boite.display((marche_arret.game_state() and not inventaire.ouvert))
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_e] and marche_arret.game_state() and not inventaire.ouvert and arme.can_switch and the_boite != "No box in range" :
            # Si on possède déjà l'arme, alors on combine les munitions
            if the_boite.arme in arme.weapon_inventory and the_boite.arme != "No weapon" :
                arme.munitions[arme.weapon_inventory.index(the_boite.arme)], the_boite.munitions = arme.munitions[arme.weapon_inventory.index(the_boite.arme)] + the_boite.munitions, 0
                arme.can_switch = False
            # On ne peut pas déséquiper le pistolet
            elif arme.weapon_equiped != 2 :
                arme.weapon_inventory[arme.weapon_equiped], the_boite.arme = the_boite.arme, arme.weapon_inventory[arme.weapon_equiped]
                arme.munitions[arme.weapon_equiped], the_boite.munitions = the_boite.munitions, arme.munitions[arme.weapon_equiped]
                arme.can_switch = False
                arme.previous_weapon_equiped = None # Petite astuce pour actualiser l'arme
            # Si l'arme équipé est le pistolet, on essaye d'ajouter l'arme dans un espace vide de l'inventaire d'arme s'il y en a un
            else :
                for i in range(len(arme.weapon_inventory)-1) :
                    if arme.weapon_inventory[i] == "No weapon" :
                        arme.weapon_inventory[i], the_boite.arme = the_boite.arme, arme.weapon_inventory[i]
                        arme.munitions[i], the_boite.munitions = the_boite.munitions, arme.munitions[i]
                        arme.can_switch = False
        # Permet de limiter le nombre d'interraction à une par touche " e " pressé
        elif not pressed[pygame.K_e] :
            arme.can_switch = True
        # Fin de la partie intéraction avec les boites + affichage

        balles.display(dt, (marche_arret.game_state() and not inventaire.ouvert), inventaire.stats["Agi"]) # Affichage des projectiles
        hero.display() # Affichage du héro
        power_up.effet_display() # Affichage de l'effet visuel des powers up
        zombies.display(dt, (marche_arret.game_state() and not inventaire.ouvert), score, inventaire, zombie_temps, power_up, boite, hero)
        arme.display() # Affichage de l'arme
        fps.display(temps.time) # Affichage des FPS
        hero.GUI_display() # Affichage de la bare de vie
        if not inventaire.ouvert : # On cache l'affichage quand l'inventaire est ouvert (pour rendre le tout plus lisible)
            arme.display_cases() # Affichage de l'inventaire pour les armes
        score.display() # Affichage du score
        temps.display(marche_arret.game_state() and not inventaire.ouvert, score) # Affichage du temps
        zombies.actualiser_all_zombies(temps.time) # Doit être mis après temps.display()
        marche_arret.display() # Affichage du bouton pause
        balles.display_dispersion()

        pressed = pygame.key.get_pressed()
        # Touches pour équiper les différentes armes
        if pressed[pygame.K_1] :
            arme.weapon_equiped = 0
        elif pressed[pygame.K_2] :
            arme.weapon_equiped = 1
        elif pressed[pygame.K_3] :
            arme.weapon_equiped = 2
        
        # Touches pour l'inventaire
        if pressed[pygame.K_a] :
            if inventaire.can_switch :
                inventaire.ouvert = not inventaire.ouvert
                inventaire.can_switch = False
        elif pressed[pygame.K_r] :
            if inventaire.can_switch :
                inventaire.can_switch = False
                inventaire.add_item(random.choice(inventaire.all_items_name))
        elif not inventaire.can_switch :
            inventaire.can_switch = True
        # Fin des touches

        if inventaire.ouvert :
            inventaire.display() # Affichage
        if inventaire.affichage > 0 :
            inventaire.objet_trouve()
        inventaire.stats_display()
        curseur(screen)

        if game_over :
            Time = 0
            sons.pause(0)
            text(screen, "./FreeSansBold.ttf", 50, 'GAME OVER', RED, (385, 350))
            text(screen, "./FreeSansBold.ttf", 20, 'Tapez \'n\' pour commencer une nouvelle partie.', BLACK, (250, 400))

        pygame.display.flip()


if __name__ == '__main__' :
    while True :
        main()