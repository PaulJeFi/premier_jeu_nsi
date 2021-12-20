'''
Définition de toutes les armes du jeu
all_weapons = {"Nom de l'arme" : [["chemin relatif de l'image de l'arme", "chemin relatif de l'image du projectile", [taille du projectile, taille arme], [décalage droite du projectile, décalage avant du projectile]], [[durée de vie minimale du projectile, durée de vie maximale du projectile], nombre de projectiles tirées par coup, [dispersion suplémentaire par tir, dispersion minimale, dispersion maximale, True(dispersion individuelle) ou False(dispersion commune sauf pour la dispersion minimale), dispersion régulière ou non, temps (en frame) avant la réduction du spread], [vitesse minimale du projectile, vitesse maximale du projectile], dégats infligés par le projectile], ["chemin relatif de l'image pour l'inventaire de l'arme", [nombre de munitions minimal, nombre de munitions maximal], chance de spawn]]}
'''

all_weapons = {"No weapon" : [["./images/Nothing.png", "./images/Nothing.png", [1, 1], [0, 0]], [[0, 0], 0, [0, 0, 0, True, False, 0], [0, 0], 0], ["./images/Nothing.png", [0, 0], 0]],
            "Pistolet mitrailleur" : [["./images/armes/Mitraillette/Mitraillette.png", "./images/armes/Projectiles/Projectile.png", [40, 200], [30, 93]], [[45, 60], 1, [8, 0, 50, True, False, 20], [1.5, 2], 60], ["./images/armes/Mitraillette/Mitraillette_inventaire.png", [40, 120], 25]],
            "Fusil de chasse" : [["./images/armes/Fusil_a_pompe/Fusil_a_pompe.png", "./images/armes/Projectiles/Projectile_petit.png", [20, 200], [30, 93]], [[5, 45], 9, [25, 15, 70, True, False, 10], [1.1, 1.8], 12], ["./images/armes/Fusil_a_pompe/Fusil_a_pompe_inventaire.png", [35, 105], 19]],
            "Supra-fusil" : [["./images/armes/Supra_fusil/Supra_fusil.png", "./images/armes/Projectiles/Laser.png", [20, 200], [30, 93]], [[20, 20], 25, [4, 0, 90, False, False, 100], [0.5, 2.5], 10], ["./images/armes/Supra_fusil/Supra_fusil_inventaire.png", [20, 120], 6]],
            "Pistolet" : [["./images/armes/Pistolet/pistolet.png", "./images/armes/Projectiles/Projectile_pistolet.png", [20, 250], [0, 105]], [[30, 40], 1, [10, 10, 25, True, False, 5], [1.2, 1.6], 40], ["./images/armes/Pistolet/pistolet_inventaire.png", [0, 0], 0]],
            "Blastmater" : [["./images/armes/Golden_blaster/golden_blaster.png", "./images/armes/Projectiles/Golden_wave.png", [40, 200], [30, 95]], [[20, 20], 7, [3, 0, 90, True, True, 100], [1.3, 1.3], 35], ["./images/armes/Golden_blaster/golden_blaster_inventaire.png", [40, 140], 4]],
            "Arc" : [["./images/armes/Arc/arc.png", "./images/armes/Projectiles/Fleche.png", [50, 200], [0, 60]], [[20, 40], 4, [20, 20, 80, False, True, 20], [1, 2], 30], ["./images/armes/Arc/arc_inventaire.png", [30, 110], 10]]}

weapon_spawn_chance = []
for i in all_weapons :
    for j in range(all_weapons[i][2][2]) :
        weapon_spawn_chance.append(i)