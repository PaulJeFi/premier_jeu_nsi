'''
Définition de toutes les armes du jeu
all_weapons = {"Nom de l'arme" : [["chemin relatif de l'image de l'arme", "chemin relatif de l'image du projectile", [taille du projectile, taille arme], [décalage droite du projectile, décalage avant du projectile]], [[durée de vie minimale du projectile, durée de vie maximale du projectile], nombre de projectiles tirées par coup, [dispersion suplémentaire par tir, dispersion minimale, dispersion maximale, True(dispersion individuelle) ou False(dispersion commune sauf pour la dispersion minimale), dispersion régulière ou non, temps (en frame) avant la réduction du spread], [vitesse minimale du projectile, vitesse maximale du projectile], dégats infligés par le projectile], ["chemin relatif de l'image pour l'inventaire de l'arme", [nombre de munitions minimal, nombre de munitions maximal], chance de spawn]]}
'''

all_weapons = {"No weapon" : [["./src/images/Nothing.png", "./src/images/Nothing.png", [1, 1], [0, 0]], [[0, 0], 0, [0, 0, 0, True, False, 0], [0, 0], 0], ["./src/images/Nothing.png", [0, 0], 0]],
            "Pistolet mitrailleur" : [["./src/images/armes/Mitraillette/Mitraillette.png", "./src/images/armes/Mitraillette/projectile.png", [40, 200], [30, 93]], [[45, 60], 1, [8, 0, 50, True, False, 20], [1.5, 2], 60], ["./src/images/armes/Mitraillette/Mitraillette_inventaire.png", [150, 300], 25]],
            "Fusil de chasse" : [["./src/images/armes/Fusil_a_pompe/Fusil_a_pompe.png", "./src/images/armes/Fusil_a_pompe/projectile.png", [20, 200], [30, 93]], [[5, 45], 9, [25, 15, 70, True, False, 10], [1.1, 1.8], 12], ["./src/images/armes/Fusil_a_pompe/Fusil_a_pompe_inventaire.png", [70, 245], 17]],
            "Supra-fusil" : [["./src/images/armes/Supra_fusil/Supra_fusil.png", "./src/images/armes/Supra_fusil/projectile.png", [20, 200], [30, 93]], [[20, 20], 25, [4, 0, 90, False, False, 100], [0.5, 2.5], 10], ["./src/images/armes/Supra_fusil/Supra_fusil_inventaire.png", [30, 110], 3]],
            "Pistolet" : [["./src/images/armes/Pistolet/pistolet.png", "./src/images/armes/Pistolet/projectile.png", [20, 250], [0, 105]], [[30, 40], 1, [10, 10, 40, True, False, 5], [1.2, 1.6], 40], ["./src/images/armes/Pistolet/pistolet_inventaire.png", [0, 0], 0]],
            "Blastmater" : [["./src/images/armes/Golden_blaster/golden_blaster.png", "./src/images/armes/Golden_blaster/projectile.png", [40, 200], [30, 95]], [[20, 20], 7, [3, 0, 90, True, True, 150], [1.3, 1.3], 28], ["./src/images/armes/Golden_blaster/golden_blaster_inventaire.png", [50, 160], 7]],
            "Arc" : [["./src/images/armes/Arc/arc.png", "./src/images/armes/Arc/projectile.png", [50, 200], [0, 60]], [[20, 40], 4, [20, 20, 80, False, True, 20], [1, 2], 30], ["./src/images/armes/Arc/arc_inventaire.png", [60, 200], 10]],
            "Cidnam" : [["./src/images/armes/The_cidnam/the_cidnam.png", "./src/images/armes/The_cidnam/projectile.png", [12, 250], [50, 100]], [[20, 60], 8, [2, 5, 25, True, False, 20], [1, 2], 40], ["./src/images/armes/The_cidnam/the_cidnam_inventaire.png", [0, 0], 0]]}

weapon_spawn_chance = []
for i in all_weapons :
    for j in range(all_weapons[i][2][2]) :
        weapon_spawn_chance.append(i)