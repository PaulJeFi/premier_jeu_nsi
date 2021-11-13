import pygame
if __name__ == '__main__' :
    from main import Grass, Marche_Arret, Score_actuel
import sys
import math
import random
from functions import Q_rsqrt, deplace, convert_degrees, convert_radians, collisions, v2, draw_rect, text, sound

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
myfont = pygame.font.SysFont('couriernewbold', 15)

class Zombies(deplace) :

    """ intialisation de classe : image, pv et taille """
    def __init__(self, type=1) :
        self.size = 100
        self.SPEED = 0.4
        self.image = pygame.image.load(f'./images/personages/Zombie_type_{type}.png') 
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.image = pygame.transform.rotate(self.image, 180)
        self.spawn()
        self.pos = [self.x, self.y]
        self.size = 100
        screen.blit(self.image, (int(self.pos[0]-self.size/2), int(self.pos[1]-self.size/2)))
        self.pv_maxi = 100
        self.pv = self.pv_maxi
        self.rotated = self.image
        self.angle = 0
        self.rect = self.image.get_rect()
    
    def change_to_type(self, type) :
        if type in [1, 2, 3] :
            self.image = pygame.image.load(f'./images/personages/Zombie_type_{type}.png') 
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
            self.image = pygame.transform.rotate(self.image, 180)

    def nbrPV (self) : 
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
        #def spawn_x(the_x) :
        #    '''Faut pas le dire à Mr Mandic...'''
        #    the_x = random.randint(-1*x, 2*x)
        #    if 0-self.size <= the_x <= x+self.size :
        #        the_x = spawn_x(the_x)
        #    return the_x
        #def spawn_y(the_y=0) :
        #    '''Faut pas le dire à Mr Mandic...'''
        #    the_y = random.randint(-1*y, 2*y)
        #    if 0-self.size <= the_y <= y+self.size :
        #        the_y = spawn_y(the_y)
        #    return the_y
        #self.x, self.y = spawn_x(self), spawn_y(self)

    def deplacement (self, dt) :
        '''Le déplacement de l'IA'''
        #############################################
        # Old code d'Anatole. J'ai pas tout compris.#
        # if self.x > 540 and self.y > 360 :        #
        #    self.x += 2                            #
        #    self.y += 1                            #
        #if self.x < 540 and self.y < 360 :         #
        #    self.x -= 2                            #
        #    self.y -= 1                            #
        #############################################
        
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
            self.pv -= random.randrange(0, 2, 1)/10
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
        text(screen, myfont, valeur_pv, WHITE, (self.x-(30), self.y-(41)))
        # Test de la barre de vie en foction des pv restants

class Construct_Zombies() :

    '''Cette classe permet de gérer un ensemble de zombies'''
    def __init__(self, number=3) :
        self.zombies = []
        self.respawn_cooldown = 350
        for i in range(number) :
            self.zombies.append(self.do_again(1))
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

    def display(self, dt, game_state, score) :
        if game_state :
            self.respawn()
        ID = -1 # Permet d'attribuer une ID temporaire à chaque zombie
        for zomb in self.zombies :
            ID += 1 # Chaque ID doit être différentes
            self.mourir(zomb, ID, score)
            the_x, the_y = zomb.x, zomb.y
            zomb.display(dt, game_state, score)
            for zombi in self.zombies :
                if zomb is zombi :
                    continue
                elif zomb.get_rect().colliderect(zombi.get_rect()) and zombi != zomb :
                #elif self.is_next(zomb, zombi) :
                    zomb.x, zomb.y = the_x, the_y
                    break

    def mourir(self, zomb, ID, score) :
        '''Vérifie si le zombie est supposé mourir --> le suprime si c'est le cas'''
        if zomb.pv <= 0 :
            score.add(1000)
            self.zombies.pop(ID)
            
    def respawn(self):
        '''Lorsque le compteur respawn_cooldown atteint 0, on spawn un zombie'''
        if self.respawn_cooldown <= 0 :
            self.zombies.append(self.do_again(1))
            self.respawn_cooldown = 350
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
        zombies.display(dt, marche_arret.game_state())
        pygame.display.flip()
        #zombies.add(3)

if __name__ == '__main__' :
    main()

