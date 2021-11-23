import pygame
if __name__ == '__main__' :
    from main import Grass, Marche_Arret, Score_actuel
import sys
import math
import random
from functions import Q_rsqrt, deplace, convert_degrees, convert_radians, collisions, v2, draw_rect, text, sound
from liste_zombies import all_zombie_type, zombie_wave_spawn_rate

pygame.init()
BLACK = (0, 0, 0)
GRAY = (20, 20, 20)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Les règlages de base (vitesse du joueur + set-up affichage + set-up frame-rate)
x, y = 1080, 720
screen = pygame.display.set_mode((x, y))
pygame.display.set_caption("Friends Royal")
pygame.display.set_icon(pygame.image.load('./images/personages/Humain_type_1.png').convert())
screen.fill(WHITE)
clock = pygame.time.Clock()
pygame.font.init()
#myfont = pygame.font.SysFont('couriernewbold', 15)
myfont = pygame.font.Font("./FreeSansBold.ttf", 15)

class Zombies(deplace) :

    """ intialisation de classe : image, pv et taille """
    def __init__(self, type="Z1") :
        self.type = type
        self.all_zombies = all_zombie_type
        self.size = 100
        self.SPEED = self.all_zombies[self.type][1][1]
        self.image = pygame.image.load(f'./images/personages/{self.all_zombies[self.type][0]}.png') 
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.image = pygame.transform.rotate(self.image, 180)
        self.spawn()
        self.pos = [self.x, self.y]
        screen.blit(self.image, (int(self.pos[0]-self.size/2), int(self.pos[1]-self.size/2)))
        self.pv_maxi = self.all_zombies[self.type][1][0]
        self.pv = self.pv_maxi
        self.rotated = self.image
        self.angle = 0
        self.rect = self.image.get_rect()
    
    def change_to_type(self, type) :
        if type in list(self.all_zombies.keys()) :
            self.image = pygame.image.load(f'./images/personages/{self.all_zombies[self.type][0]}.png') 
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
            self.image = pygame.transform.rotate(self.image, 180)

    def nbrPV(self) : 
        if self.pv > self.pv_maxi :
            self.pv = self.pv_maxi
        elif self.pv < 0 :
            self.pv = 0

    def spawn(self) :
        '''Fait naître les Zombies par la grâce de [REDACTED]. N'oublions pas sa supériorité totale.'''
        position = random.randint(1,4)
        if position == 1 :
            self.x, self.y = 0-self.size, random.randint(0-self.size, y+self.size)
        elif position == 2 :
            self.x, self.y = random.randint(0-self.size, x+self.size), 0-self.size
        elif position == 3 :
            self.x, self.y = x+self.size, random.randint(0-self.size, y+self.size)
        elif position == 4 :
            self.x, self.y = random.randint(0-self.size, x+self.size), y+self.size

    def deplacement (self, dt) :
        '''Le déplacement de l'IA'''

        '''
        Un code naïf serait le suivant :

        if self.x > x/2 :
            self.x -= 1
        elif self.x < x/2 :
            self.x += 1
        if self.y > y/2 :
            self.y -= 1
        elif self.y < y/2 :
            self.y += 1
        
        Mais le problème est que le zombie ne se déplace pas DIRECTEMENT vers le
        centre, mais vers les axes centraux, donc au final vers le centre.
        If faut donc utiliser des VECTEURS.
        On peut alors utiliser le code suivant :

        l = math.sqrt((self.x - x/2)**2 + (self.y - y/2)**2 )
        self.vect = [1/l * (self.x - x/2), 1/l * (self.y - y/2)]
        self.x -= self.SPEED * self.vect[0]
        self.y -= self.SPEED * self.vect[1]

        Mais ce code, bien qu'il soit FONCTIONNEL, est tès LENT. En effet, les
        racines et les divisions sont des opérations lentes par les ordinateurs.
        Donc on fait comme suit :
        '''
        un_sur_l = Q_rsqrt((self.x - x/2)**2 + (self.y - y/2)**2)
        self.vect = [un_sur_l * (self.x - x/2), un_sur_l * (self.y - y/2)]
        self.x -= dt*self.SPEED * self.vect[0]
        self.y -= dt*self.SPEED * self.vect[1]

    def deplacement_inverse(self, dt):
        l = math.sqrt((self.x - x/2)**2 + (self.y - y/2)**2 )
        self.vect = [1/l * (self.x - x/2), 1/l * (self.y - y/2)]
        self.x += dt*self.SPEED * self.vect[0]
        self.y += dt*self.SPEED * self.vect[0]

    def degatZomb(self) :
        # Si le zombie est touché
        self.pv -= 1
    
    def display(self, dt, game_state, score) :
        if game_state :
            self.deplacement(dt)
            self.change()
            #self.pv -= random.randrange(0, 2, 1)/10
        screen.blit(self.rotated, (self.x-self.size/2, self.y-self.size/2))
        self.barreVie()

    def change(self) :
        '''Tourne le zombie pour qu'il ragarde le centre'''
        if self.x-x/2 != 0 :
            self.angle = math.atan((self.y-y/2)/(self.x-x/2))
            self.angle = convert_degrees(self.angle)
            if self.x < x/2 :
                self.angle = 180-self.angle
            else :
                self.angle = -self.angle
            self.rotated = pygame.transform.rotate(self.image, self.angle)
    
    def get_rect(self) :
        return pygame.Rect(self.x-self.size/2, self.y-self.size/2, *2*[self.size])

    def barreVie(self) :
        '''Affiche la barre de pv des zombies'''
        # Couleur des barres + deffinition du texte
        if self.pv > 0:
            couleur_pv = (255-self.pv/self.pv_maxi*200, self.pv/self.pv_maxi*200, 0)
        else:
            couleur_pv = RED
        valeur_pv = f"{str(round(self.pv))} / {str(self.pv_maxi)}"
        # Dessiner la bare de vie
        draw_rect(screen, (self.x-(32), self.y-(32)), (94, 14), BLACK)
        draw_rect(screen, (self.x-(32), self.y-(42)), (round(len(valeur_pv)*6)-5, 11), BLACK) # Barre noire suplémentaire
        draw_rect(screen, (self.x-(30), self.y-(30)), (self.pv*(100-10)/self.pv_maxi, 20-10), couleur_pv)
        text(screen, "./FreeSansBold.ttf", 10, valeur_pv, WHITE, (self.x-(30), self.y-(41)))
        # Test de la barre de vie en foction des pv restants

class Construct_Zombies() :

    '''Cette classe permet de gérer un ensemble de zombies'''
    def __init__(self, number=0) :
        self.all_zombies = all_zombie_type
        self.zombies = []
        self.respawn_cooldown = 350
        for i in range(number) :
            self.zombies.append(self.do_again(1))
        self.zomb_level = zombie_wave_spawn_rate
        #self.zombies = [self.do_again(1) for i in range(number)]
            
    def do_again(self, type) :
        zombie = Zombies(type)
        for zomb in self.zombies :
            if self.is_next(zombie, zomb) :
                zombie = self.do_again(type)
        return zombie
    
    def is_next(self, zomb, zombi) :
        size = Zombies().size
        longueur_max = size*v2 # la distance maximale d'éligibilité
        if math.sqrt((zomb.x-zombi.x)**2+(zomb.y-zombi.y)**2) <= longueur_max :
            return True
        else :
            return False

    def add(self, type) :
        self.zombies.append(self.do_again(type))#.change_to_type(type))

    def display(self, dt, game_state, score, inventaire) :
        if game_state :
            self.respawn(score)
        ID = -1 # Permet d'attribuer une ID temporaire à chaque zombie
        for zomb in self.zombies :
            ID += 1 # Chaque ID doit être différentes
            self.mourir(zomb, ID, score, inventaire)
            the_x, the_y = zomb.x, zomb.y
            zomb.display(dt, game_state, score)
            for zombi in self.zombies :
                if zomb is zombi :
                    continue
                elif zomb.get_rect().colliderect(zombi.get_rect()) and zombi != zomb :
                #elif self.is_next(zomb, zombi) :
                    zomb.x, zomb.y = the_x, the_y
                    break

    def mourir(self, zomb, ID, score, inventaire) :
        '''Vérifie si le zombie est supposé mourir --> le suprime si c'est le cas'''
        if zomb.pv <= 0 :
            score.add(self.all_zombies[zomb.type][2])
            inventaire.add_item(random.choice(self.all_zombies[zomb.type][3]))
            self.zombies.pop(ID)
            
    def respawn(self, score):
        '''Lorsque le compteur respawn_cooldown atteint 0, on spawn un zombie'''
        if self.respawn_cooldown <= 0 :
            self.zombies.append(self.do_again(random.choice(self.zomb_level[score.niveau])))
            self.respawn_cooldown = random.randint(250, 350)-20*score.niveau
        else :
            self.respawn_cooldown -= 1
        
    def touch_hero(self, dt, hero: pygame.Rect) -> bool :
        '''Si les zombies touchent le héro.'''
        touche_hero = False
        for zombie in self.zombies :
            if zombie.get_rect().colliderect(hero) :
                zombie.deplacement_inverse(dt)
                touche_hero = True
        return touche_hero

    def touch_balle(self, dt, hero: pygame.Rect) -> bool :
        '''Si les zombies touchent une balle.'''
        touche_hero = False
        zombie = None
        ID = None
        for zombie in self.zombies :
            if zombie.get_rect().colliderect(hero) :
                zombie.deplacement_inverse(dt)
                touche_hero = True
                ID = self.zombies.index(zombie)
                return touche_hero, ID, zombie.type
        return touche_hero, ID, zombie

    def haut(self, dt) :
        for zomb in self.zombies :
            zomb.haut(dt)

    def bas(self, dt) :
        for zomb in self.zombies :
            zomb.bas(dt)

    def gauche(self, dt) :
        for zomb in self.zombies :
            zomb.gauche(dt)

    def droite(self, dt) :
        for zomb in self.zombies :
            zomb.droite(dt)
    

def main() :
    '''Fonction principale'''
    grass = Grass()
    score = Score_actuel()
    marche_arret = Marche_Arret()
    zombies = Construct_Zombies()
    while True : # False = le jeu s'arrête
        dt = clock.tick(144) # IMPORTANT : FPS du jeu
        screen.fill(WHITE)
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                pygame.quit()
                sys.exit()
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP] or pressed[pygame.K_z] :
            grass.bas(dt)
            zombies.bas(dt)
        if pressed[pygame.K_DOWN] or pressed[pygame.K_s] :
            grass.haut(dt)
            zombies.haut(dt)
        if pressed[pygame.K_LEFT] or pressed[pygame.K_q] :
            grass.gauche(dt)
            zombies.gauche(dt)
        if pressed[pygame.K_RIGHT] or pressed[pygame.K_d] :
            grass.droite(dt)
            zombies.droite(dt)
        # Affiche ton sprite ici.
        grass.display()
        zombies.display(dt, marche_arret.game_state(), score)
        pygame.display.flip()
        #zombies.add(3)

if __name__ == '__main__' :
    main()

