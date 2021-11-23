# Definition de tous les zombies {"nom_d_appel" : ["nom_fichier_png", [vie, vitesse, attaque, régénération(pas encore fonctionnel)], score, [loot_table]]}
all_zombie_type = {"Z1" : ["Zombie_type_1", [100, 0.3, 0.25, 0], 250, [""]*200 + ["Bottes"]*2 + ["Armure avec cape"]*2 + ["Armure dorée"]*1],
                   "Z2" : ["Zombie_type_2", [150, 0.35, 0.35, 0], 350, [""]*200 + ["Armure dorée"]*2 + ["Bottes"]*4 + ["Grand coeur"]*1 + ["Trèfle à 4 feuilles"]*1],
                   "Z3" : ["Zombie_type_3", [225, 0.4, 0.5, 0], 500, [""]*150 + ["Trèfle à 4 feuilles"]*1 + ["Bouclier du paladin"]*2 + ["Âme des flammes"]*2 + ["Rune anti-vie"]*1]}



# Quels zombies apparraissent en fonction de la dificulté
zombie_wave_spawn_rate = {0: ["Z1"]*100,
                          1: ["Z1"]*100,
                          2: ["Z1"]*100,
                          3: ["Z1"]*90+["Z2"]*10,
                          4: ["Z1"]*75+["Z2"]*25,
                          5: ["Z1"]*60+["Z2"]*35+["Z3"]*5,
                          6: ["Z1"]*40+["Z2"]*45+["Z3"]*15,
                          7: ["Z1"]*30+["Z2"]*50+["Z3"]*20,
                          8: ["Z1"]*20+["Z2"]*45+["Z3"]*35,
                          9: ["Z1"]*10+["Z2"]*40+["Z3"]*50,
                          10: ["Z2"]*35+["Z3"]*65,
                          11: ["Z2"]*20+["Z3"]*80,
                          12: ["Z2"]*10+["Z3"]*90,
                          13: ["Z3"]*100}