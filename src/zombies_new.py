'''
Ce fichier fait partie du jeu. Il répertorie les fonctions, classes, … de
gestion et de génération des zoimbies, ainsi que leurs interactions avec les
autres objets du jeu.
'''

import pygame
if __name__ == '__main__' : # Pour les tests (et éviter les erreurs générées par l'éditeur de texte)
    from main import Grass, Marche_Arret, Score_actuel, Temps, Inventaire
import sys
import math
import random
from functions import Q_rsqrt, deplace, convert_degrees, convert_radians, collisions, v2, draw_rect, text, sound
from liste_zombies import actualiser, zombie_wave_spawn_rate, always_spawn

pygame.init()
BLACK = (0, 0, 0)
GRAY = (20, 20, 20)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Les réglages de base (vitesse du joueur + set-up affichage + set-up frame-rate)
x, y = 1080, 720
screen = pygame.display.set_mode((x, y))
pygame.display.set_caption("Friends Royal")
pygame.display.set_icon(pygame.image.load('./src/images/personages/Humain_type_1.png').convert())
screen.fill(WHITE)
clock = pygame.time.Clock()
pygame.font.init()
#myfont = pygame.font.SysFont('couriernewbold', 15)
myfont = pygame.font.Font("./src/FreeSansBold.ttf", 15)

class Zombies(deplace) :
    '''Classe des zombies : gestion d'UN SEUL zombie'''

    def __init__(self, type="Z1", temps=0) :
        '''Intialisation de l'objet Zombies par le type de zombie et son temps (pour la difficulté). \n
        Tous les principaux attributs d'un objet Zombies sont déclarés ici.'''
        self.type = type
        self.all_zombies = actualiser(temps)
        if self.type == "ZD" :
            self.max_cooldown = 500 # Délai entre chaque utilisation de la compétance spéciale du zombie
        else :
            self.max_cooldown = 0
        self.cooldown = round(self.max_cooldown*random.randint(65, 135)/100) # Cooldown aléatoire (pour rendre l'attaque imprévisible) mais reste proche du cooldown classique en temps
        self.size = 100
        self.SPEED = self.all_zombies[self.type][1][1]
        self.regen_pv = self.all_zombies[self.type][1][3]
        self.image = pygame.image.load(f'./src/images/personages/{self.all_zombies[self.type][0]}.png') 
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
        '''Petite méthode qui fut utile pour changer rapidement le type d'un Zombies. N'est plus utilisée il me semble.'''
        if type in list(self.all_zombies.keys()) :
            self.image = pygame.image.load(f'./src/images/personages/{self.all_zombies[self.type][0]}.png') 
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
            self.image = pygame.transform.rotate(self.image, 180)

    def nbrPV(self) :
        '''Réajustement des pv du zombie dans l'intervalle [0, self.pv_maxi]'''
        if self.pv > self.pv_maxi :
            self.pv = self.pv_maxi
        elif self.pv < 0 :
            self.pv = 0

    def spawn(self) :
        '''Fait naître les Zombies par la grâce de [REDACTED][TERENCE]. N'oublions pas sa supériorité totale.'''
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
        '''Le déplacement de l'IA

        Un code naïf serait le suivant :

        ```
        if self.x > x/2 :
            self.x -= 1
        elif self.x < x/2 :
            self.x += 1
        if self.y > y/2 :
            self.y -= 1
        elif self.y < y/2 :
            self.y += 1
        ```

        Mais le problème est que le zombie ne se déplace pas DIRECTEMENT vers le
        centre, mais vers les axes centraux, donc au final vers le centre.
        If faut donc utiliser des VECTEURS.
        On peut alors utiliser le code suivant :

        ```
        l = math.sqrt((self.x - x/2)**2 + (self.y - y/2)**2 )
        self.vect = [1/l * (self.x - x/2), 1/l * (self.y - y/2)]
        self.x -= self.SPEED * self.vect[0]
        self.y -= self.SPEED * self.vect[1]
        ```

        Mais ce code, bien qu'il soit FONCTIONNEL, est tès LENT. En effet, les
        racines et les divisions sont des opérations lentes par les ordinateurs.
        Donc on fait comme suit :
        '''
        un_sur_l = Q_rsqrt((self.x - x/2)**2 + (self.y - y/2)**2)
        self.vect = [un_sur_l * (self.x - x/2), un_sur_l * (self.y - y/2)]
        self.x -= dt*self.SPEED * self.vect[0]
        self.y -= dt*self.SPEED * self.vect[1]

    def deplacement_inverse(self, dt):
        '''Pour faire reculer le zombie. Utile si il touche le héros, touche une munition (peut-être aussi si il touche un autre zombie).'''
        un_sur_l = Q_rsqrt((self.x - x/2)**2 + (self.y - y/2)**2)
        self.vect = [un_sur_l * (self.x - x/2), un_sur_l * (self.y - y/2)]
        self.x += dt*self.SPEED * self.vect[0]
        self.y += dt*self.SPEED * self.vect[1]

    def degatZomb(self) :
        '''Infliger des dégâts au zombie si il est touché'''
        self.pv -= 1
    
    def display(self, dt, game_state, score) :
        '''Affichage du zombie'''
        if game_state :
            self.deplacement(dt)
            self.change()
            self.regen(dt)
            #self.pv -= random.randrange(0, 2, 1)/10
        if -self.size - x*0.1 < self.x < 1.1*x and -self.size - y*0.1 < self.y < y*1.1 : # Permet d'afficher le zombie seulement s'il peut être vu par le joueur (économie de performance)
            screen.blit(self.rotated, (self.x-self.size/2, self.y-self.size/2))
            self.barreVie()

    def regen(self, dt) :
        '''Régénération naturelle des pv du zombie'''
        valeur_regen = self.regen_pv/dt/6
        if self.pv + valeur_regen >= self.pv_maxi :
            self.pv = self.pv_maxi
        else :
            self.pv += valeur_regen

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
        '''Retourne un ```pygame.Rect``` pour le zombie. Utile pour les collisions.'''
        return pygame.Rect(self.x-self.size/2, self.y-self.size/2, *2*[self.size])

    def barreVie(self) :
        '''Affiche la barre de pv des zombies'''
        # Couleur des barres + deffinition du texte
        if self.pv > 0:
            couleur_pv = (255-self.pv/self.pv_maxi*200, self.pv/self.pv_maxi*200, 0)
        else:
            couleur_pv = RED
        valeur_pv = f"{str(round(self.pv))} / {str(round(self.pv_maxi))}"
        # Dessiner la bare de vie
        draw_rect(screen, (self.x-(32), self.y-(32)), (94, 14), BLACK)
        draw_rect(screen, (self.x-(32), self.y-(42)), (round(len(valeur_pv)*6)-5, 11), BLACK) # Barre noire suplémentaire
        draw_rect(screen, (self.x-(30), self.y-(30)), (self.pv*(100-10)/self.pv_maxi, 20-10), couleur_pv)
        text(screen, "./src/FreeSansBold.ttf", 10, valeur_pv, WHITE, (self.x-(30), self.y-(41)))
        # Test de la barre de vie en foction des pv restants

    def touch_hero(self, dt, hero: pygame.Rect) -> bool :
        '''Si le zombie touche le héro.'''
        touche_hero = False
        if self.get_rect().colliderect(hero) :
            self.deplacement_inverse(dt)
            touche_hero = True
        return touche_hero

class Projectiles_zombie(deplace) :
    '''Classe des projectiles des zombies (oui il y a des zombies qui nous tirent dessus !).'''

    def __init__(self, type="ZD", angle=0, vecteur=[1, 0], x=0, y=0) :
        '''Initialisation de l'objet. Le type est un zombie deymon (type de zombie qui tire).'''
        self.type = type
        # On créer l'image du projectile
        self.image = pygame.image.load('./src/images/armes/Projectiles/feu.png')
        # Taille du projectile
        self.size = 50
        # Redimentionnement de l'image du projectile
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        # Angle du projectile (sert pour tourner le projectile dans le bon sens)
        self.angle = (angle + 180) % 360
        # On tourne l'image du projectile
        self.image = pygame.transform.rotate(self.image, self.angle)
        # Direction du projectile (en vecteur)
        self.vecteur = vecteur
        # Vitesse du projectile
        self.speed = 1.1
        # Durée de vie du projectile
        self.life_time = 100
        # Dégat que le projectile inflige au joueur
        self.attaque = 20
        # Position d'apparition du projectile + création de sa zone de collision
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
    
    def mouvement(self, dt) :
        '''Pour le mouvement du projectile'''
        if self.life_time > 0 :
            self.x -= dt*self.speed * self.vecteur[0]
            self.y -= dt*self.speed * self.vecteur[1]
            self.life_time -= 1

    def display(self) :
        '''Affichage du projectile'''
        screen.blit(self.image, (self.x, self.y))
    
    def get_rect(self) :
        '''Retourne un ```pygame.Rect``` pour le projectile. Utile pour les collisions.'''
        return pygame.Rect(self.x-self.size/2, self.y-self.size/2, *2*[self.size])

class Construct_Zombies() :
    '''Cette classe permet de gérer un ensemble de zombies'''

    def __init__(self, number=0) :
        self.all_zombies = actualiser(0)
        self.projectiles = []
        self.zombies = []
        self.respawn_cooldown = 350
        for i in range(number) :
            self.zombies.append(self.do_again(1))
        self.zomb_level = zombie_wave_spawn_rate
        #self.zombies = [self.do_again(1) for i in range(number)]
            
    def actualiser_all_zombies(self, temps) :
        self.all_zombies = actualiser(temps)

    def do_again(self, type, temps=0) :
        '''Trouve des coordonnées pour un nouveau zombie en vérifiant qu'il ne
        tombe pas sur un zombie existant. Attention, méthode récursive.'''
        zombie = Zombies(type, temps)
        for zomb in self.zombies :
            if self.is_next(zombie, zomb) :
                zombie = self.do_again(type, temps)
        return zombie
    
    def is_next(self, zomb, zombi) :
        '''Vérifie que deux zombies ne se superposent pas (si ils se superposent
        ils ne pourront plus bouger jusqu'à ce que l'un d'eux meure).'''
        size = Zombies().size
        longueur_max = size*v2 # la distance maximale d'éligibilité
        if math.sqrt((zomb.x-zombi.x)**2+(zomb.y-zombi.y)**2) <= longueur_max :
            return True
        else :
            return False

    def add(self, type) :
        '''Ajoute un zombie'''
        self.zombies.append(self.do_again(type))#.change_to_type(type))

    def competance(self, zomb, game_state) :
        '''Si le zombie est de type deymon et qu'il peut tirer, faisons-le tirer !'''
        if game_state :
            if zomb.cooldown <= 0 :
                if zomb.type == "ZD" :
                    self.projectiles.append(Projectiles_zombie(zomb.type, zomb.angle, zomb.vect, zomb.x, zomb.y))
                zomb.cooldown = round(zomb.max_cooldown*random.randint(65, 135)/100)
            else :
                zomb.cooldown -= 1

    def display(self, dt, game_state, score, inventaire, temps, power_up, boite, hero=None) :
        '''Affichage de tous les zombies'''
        if game_state :
            self.respawn(score, temps)
        ID = -1 # Permet d'attribuer une ID temporaire à chaque zombie
        for zomb in self.zombies :
            ID += 1 # Chaque ID doit être différente des autres
            self.mourir(zomb, ID, score, inventaire, power_up, boite)
            the_x, the_y = zomb.x, zomb.y
            self.competance(zomb, game_state)
            zomb.display(dt, game_state, score)
            for zombi in self.zombies :
                if zomb is zombi :
                    continue
                elif zomb.get_rect().colliderect(zombi.get_rect()) and zombi != zomb :
                #elif self.is_next(zomb, zombi) :
                    zomb.x, zomb.y = the_x, the_y
                    break
        ID = -1 # Permet d'attribuer une ID temporaire à chaque projectile
        for projectile in self.projectiles :
            ID += 1 # Chaque ID doit être différente des autres
            if projectile.life_time > 0 :
                if game_state :
                    projectile.mouvement(dt)
                projectile.display()
                self.projectile_touche_hero(projectile, hero, ID, inventaire.stats["Def"], power_up)
            else :
                self.projectiles.pop(ID)

    def mourir(self, zomb, ID, score, inventaire, power_up, boite) :
        '''Vérifie si le zombie est supposé mourir --> le suprime si c'est le cas'''
        if zomb.pv <= 0 :
            score.add(self.all_zombies[zomb.type][2])
            inventaire.add_item(random.choice(self.all_zombies[zomb.type][3]))
            if random.randint(0, 25) == 0 : # <= Plus la deuxième valeur du random.randint() est élevé, moins le zombie a de chance de droper un power up
                power_up.add((zomb.x, zomb.y))
            self.zombies.pop(ID)
            
    def respawn(self, score, temps):
        '''Lorsque le compteur respawn_cooldown atteint 0, on spawn un zombie'''
        if self.respawn_cooldown <= 0 :
            self.zombies.append(self.do_again(random.choice(self.zomb_level[score.niveau][0] + always_spawn + ["ZL"]*(round((temps/100)**1.3))), temps))
            self.respawn_cooldown = random.randint(self.zomb_level[score.niveau][1][0], self.zomb_level[score.niveau][1][1])
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

    def projectile_touche_hero(self, projectile, hero, ID, stat, power_up) :
        '''Le projectile touche-t-il le héro ?'''
        if projectile.get_rect().colliderect(hero.get_rect()) :
            hero.pv -= projectile.attaque*(0.997**(stat + 150*power_up.effet_actif("armure"))) # La boulle de feu ignore en partie l'armure (0.998**stat au lieu de 0.99**stat)
            self.projectiles.pop(ID)

    def touch_balle(self, dt, hero: pygame.Rect, balle_is_balle=True) -> bool :
        '''Si les zombies touchent une balle.'''
        touche_hero = False
        zombie = None
        ID = None
        for zombie in self.zombies :
            if zombie.get_rect().colliderect(hero) :
                if not balle_is_balle :
                    zombie.deplacement_inverse(dt) # cette ligne fait déplacer les zombies dans le sens inverse si ils touchet le héro
                else :
                    zombie.deplacement_inverse(2*dt/3) # cette ligne fait déplacer les zombies dans le sens inverse si ils touchet la balle
                    if self.touch_other_zombi(zombie) :
                        zombie.deplacement(dt)
                touche_hero = True
                ID = self.zombies.index(zombie)
                return touche_hero, ID, zombie.type
        return touche_hero, ID, zombie


    # les déplacements des zombies selon le mouvement du joueur:
    def haut(self, dt) :
        for zomb in self.zombies + self.projectiles :
            zomb.haut(dt)

    def bas(self, dt) :
        for zomb in self.zombies + self.projectiles :
            zomb.bas(dt)

    def gauche(self, dt) :
        for zomb in self.zombies + self.projectiles :
            zomb.gauche(dt)

    def droite(self, dt) :
        for zomb in self.zombies + self.projectiles :
            zomb.droite(dt)
    
    def touch_other_zombi(self, zomb) :
        rect = zomb.get_rect()
        for zombie in self.zombies :
            if zombie == zomb :
                continue
            elif zombie.get_rect().colliderect(rect) :
                return True
        return False

def main() :
    '''Fonction de test des zombies.  \n
    ATTENTION : n'est plus à jour, génère des erreurs !!!'''
    grass = Grass()
    score = Score_actuel()
    temps = Temps()
    inventaire = Inventaire()
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
        zombies.display(dt, marche_arret.game_state(), score, inventaire, temps)
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
        temps.display(marche_arret.game_state() and not inventaire.ouvert, score)
        zombies.actualiser_all_zombies(temps.time)
        pygame.display.flip()
        #zombies.add(3)

if __name__ == '__main__' :
    main()