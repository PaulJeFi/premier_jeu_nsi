'''
Définition de toutes les armes du jeu
all_weapons = {"Nom de l'arme" : [["chemin relatif de l'image de l'arme", "chemin relatif de l'image du projectile", taille du projectile], [[durée de vie minimale du projectile, durée de vie maximale du projectile], nombre de projectiles tirées par coup, [dispersion suplémentaire par tir, dispersion minimale, dispersion maximale], [vitesse minimale du projectile, vitesse maximale du projectile], dégats infligés par le projectile]]}
'''

all_weapons = {"Pistolet mitrailleur" : [["./images/armes/Mitraillette/Mitraillette.png", "./images/armes/Projectiles/Projectile.png", 40], [[45, 60], 1, [15, 0, 30], [1.5, 2], 50]],
            "Fusil de chasse" : [["./images/armes/Fusil_a_pompe/Fusil_a_pompe.png", "./images/armes/Projectiles/Projectile_petit.png", 20], [[15, 30], 9, [25, 15, 50], [1.1, 1.8], 9]]}