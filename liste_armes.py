'''
Définition de toutes les armes du jeu
all_weapons = {"Nom de l'arme" : [["chemin relatif de l'image de l'arme", "chemin relatif de l'image du projectile", [taille du projectile, taille arme], [décalage droite du projectile, décalage avant du projectile]], [[durée de vie minimale du projectile, durée de vie maximale du projectile], nombre de projectiles tirées par coup, [dispersion suplémentaire par tir, dispersion minimale, dispersion maximale, True(dispersion individuelle) ou False(dispersion commune sauf pour la dispersion minimale), dispersion régulière ou non], [vitesse minimale du projectile, vitesse maximale du projectile], dégats infligés par le projectile]]}
'''

all_weapons = {"Pistolet mitrailleur" : [["./images/armes/Mitraillette/Mitraillette.png", "./images/armes/Projectiles/Projectile.png", [40, 200], [30, 93]], [[45, 60], 1, [25, 0, 50, True, False], [1.5, 2], 55]],
            "Fusil de chasse" : [["./images/armes/Fusil_a_pompe/Fusil_a_pompe.png", "./images/armes/Projectiles/Projectile_petit.png", [20, 200], [30, 93]], [[5, 45], 9, [35, 15, 70, True, False], [1.1, 1.8], 9]],
            "Supra-fusil" : [["./images/armes/Supra_fusil/Supra_fusil.png", "./images/armes/Projectiles/Laser.png", [20, 200], [30, 93]], [[20, 20], 25, [90, 0, 90, False, False], [0.5, 2.5], 5]],
            "Pistolet" : [["./images/armes/Pistolet/pistolet.png", "./images/armes/Projectiles/Projectile_pistolet.png", [20, 250], [0, 105]], [[30, 40], 1, [5, 10, 25, True, False], [1.2, 1.6], 40]],
            "Blastmater" : [["./images/armes/Golden_blaster/golden_blaster.png", "./images/armes/Projectiles/Golden_wave.png", [40, 200], [30, 95]], [[20, 20], 7, [50, 0, 90, True, True], [1.3, 1.3], 11]],
            "Arc" : [["./images/armes/Arc/arc.png", "./images/armes/Projectiles/Fleche.png", [50, 200], [0, 60]], [[20, 40], 4, [45, 20, 80, False, True], [1, 2], 20]]}