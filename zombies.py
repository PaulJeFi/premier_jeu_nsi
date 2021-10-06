import pygame

class Zombies ():

    """ intialisation de classe : image, pv et taille """
    def __init__(self) :
       image = pygame.image.load('images\personages\Zombie_type_1.png') 
       image = pygame.transform.scale(image, (100, 100)
       screen.blit(int(pos[0]-size[0]/2), int(pos[1]-size[1]/2))) 
       self.size = 100
       self.x = 0
       self.y = 0
       self.pv = 30
       self.pv_maxi = 30
       self.rotated = pygame.image.load('images\personages\Zombie_type_1.png')

    def nbrPV (self) : 
        if self.pv > self.pv_maxi:
            self.pv = self.pv_maxi
        else self.pv < 0 :
            self.pv = 0

    def spawn(self) :
        self.x = 0
        self.y = 0
        self.spawn = image()
        self.spawn = (x, y)

    def deplacement (self) :
        if self.x > 540 and self.y > 360 :
            self.x += 2 
            self.y += 1
        if self.x < 540 and self.y < 360 :
            self.x -= 2 
            self.y -= 1

        
