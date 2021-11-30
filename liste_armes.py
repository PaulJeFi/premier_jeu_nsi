'''
Définition de toutes les armes du jeu
all_weapons = {"Nom de l'arme" : [["chemin relatif de l'image de l'arme", "chemin relatif de l'image du projectile", taille du projectile, [décalage droite du projectile, décalage avant du projectile]], [[durée de vie minimale du projectile, durée de vie maximale du projectile], nombre de projectiles tirées par coup, [dispersion suplémentaire par tir, dispersion minimale, dispersion maximale, True(dispersion individuelle) ou False(dispersion commune sauf pour la dispersion minimale)], [vitesse minimale du projectile, vitesse maximale du projectile], dégats infligés par le projectile]]}
'''

all_weapons = {"Pistolet mitrailleur" : [["./images/armes/Mitraillette/Mitraillette.png", "./images/armes/Projectiles/Projectile.png", 40, [32, 90]], [[45, 60], 1, [15, 0, 30, True], [1.5, 2], 50]],
            "Fusil de chasse" : [["./images/armes/Fusil_a_pompe/Fusil_a_pompe.png", "./images/armes/Projectiles/Projectile_petit.png", 20, [32, 90]], [[15, 30], 9, [35, 15, 70, True], [1.1, 1.8], 9]],
            "Supra-fusil" : [["./images/armes/Supra_fusil/Supra_fusil.png", "./images/armes/Projectiles/Laser.png", 20, [32, 90]], [[20, 20], 25, [90, 0, 90, False], [0.5, 2.5], 5]]}