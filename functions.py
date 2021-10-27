from ctypes import c_float, c_int32, cast, byref, POINTER
import math
import pygame

SPEED = 0.4

def Q_rsqrt(number):
    '''FISR : Fast Invert Square Root
    f(x) = 1/√x
    Pour référence, voir :
    https://fr.wikipedia.org/wiki/Racine_carrée_inverse_rapide
    https://en.wikipedia.org/wiki/Fast_inverse_square_root
    https://www.youtube.com/watch?v=p8u_k2LIZyo
    https://github.com/ajcr/ajcr.github.io/blob/master/_posts/2016-04-01-fast-inverse-square-root-python.md'''
    threehalfs = 1.5
    x2 = number * 0.5
    y = c_float(number)

    i = cast(byref(y), POINTER(c_int32)).contents.value
    i = c_int32(0x5f3759df - (i >> 1))
    y = cast(byref(i), POINTER(c_float)).contents.value

    y = y * (1.5 - (x2 * y * y))
    return y

def text(screen, font, string, color, pos) :
    """Permet d'afficher un texte de façon simplifiée"""
    textsurface = font.render(string, False, color)
    screen.blit(textsurface, pos)

def draw_rect(screen, position, size, color) :
    '''Permet de tracer un rectangle'''
    pygame.draw.rect(screen, color, (position[0], position[1], size[0], size[1]))

def sound(sound) :
    '''Permet de jouer un son de façon simplifiée'''
    pygame.mixer.Sound.play(sound)
    pygame.mixer.music.stop()

def curseur(screen) :
    '''Affichage du curseur personnalisé'''
    pos = pygame.mouse.get_pos()
    size = (30, 30)
    image = pygame.image.load('./images/curseur/Croix_avec_carre.png')
    image = pygame.transform.scale(image,(size[0], size[1]))
    screen.blit(image, (int(pos[0]-size[0]/2), int(pos[1]-size[1]/2)))

def convert_degrees(angle) :
    '''Convertit un angle en radians en degrés.'''
    return angle*180/math.pi

def convert_radians(angle) :
    '''Convertit un angle en degrés en radians.'''
    return angle*math.pi/180

def collisions(sprite, groupe_de_sprite):
    '''Permet de vérifier si il y a colision entre un objet et un groupe d'objet'''
    return pygame.sprite.spritecollide(sprite, groupe_de_sprite, False, pygame.sprite.collide_mask)

class deplace() :
    '''Classe de base pour le déplacement. Est wrappé par d'audres classes.'''
    def droite(self, dt) :
        self.x -= SPEED*dt
    
    def haut(self, dt) :
        self.y -= SPEED*dt

    def gauche(self, dt) :
        self.x += SPEED*dt
    
    def bas(self, dt) :
        self.y += SPEED*dt