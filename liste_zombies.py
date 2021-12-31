def actualiser(temps) :

    # Definition de tous les zombies {"nom_d_appel" : ["nom_fichier_png", [vie, vitesse, attaque, régénération(pas encore fonctionnel)], score, [loot_table]]}
    all_zombie_type = {"Z1" : ["Zombie_type_1", [100, 0.3, 0.25, 1], 250, [""]*400 + ["Vieille botte"]*10 + ["Vieille veste"]*10 + ["Bottes"]*2 + ["Armure avec cape"]*2 + ["Armure dorée"]*1],
                    "Z2" : ["Zombie_type_2", [150, 0.36, 0.4, 2.5], 400, [""]*350 + ["ADN de mutant"]*3 + ["Rune du vent"]*1 + ["Armure dorée"]*2 + ["Armure avec cape"]*2 + ["Bottes"]*4 + ["Grand coeur"]*1 + ["Trèfle à 4 feuilles"]*1],
                    "Z3" : ["Zombie_type_3", [225, 0.42, 0.65, 5], 650, [""]*300 + ["Epée corrompue"]*1 + ["Chapeau corrompu"]*1 + ["Trèfle à 4 feuilles"]*3 + ["Bouclier du paladin"]*4 + ["Âme des flammes"]*2 + ["Rune anti-vie"]*1],
                    "ZL" : ["Zombie_lessive", [(temps//60)*150+250, (temps//60)*0.01+0.38, (temps//60)*0.1+0.4, (temps//60)*4+10], round((temps//60)*250+400), [""]*1000 + ["[REDACTED]"]*1 + ["Epée corrompue"]*6 + ["Rune du vent"]*9 + ["Pierre philosophale"]*2],
                    "ZD" : ["Zombie_demon", [500, 0.25, 1, 10], 1250, [""]*750 + ["Armure des enfers"]*3 + ["Âme des flammes"]*10 + ["Rune anti-vie"]*6 + ["Pierre philosophale"]*1]}
    
    return all_zombie_type




# Quels zombies apparraissent en fonction de la dificulté
# n° Vague : [[Spawn_liste], [temps_respawn_min, temps_respawn_max], temps_requis_pour_début_vague]
zombie_wave_spawn_rate = {0: [["Z1"]*100, [200, 400], 0],
                        1: [["Z1"]*95 + ["Z2"]*5, [180, 390], 0.25],
                        2: [["Z1"]*90 + ["Z2"]*10, [160, 375], 0.5],
                        3: [["Z1"]*80 + ["Z2"]*20, [130, 355], 1],
                        4: [["Z1"]*61 + ["Z2"]*35 + ["Z3"]*4, [100, 330], 1.5],
                        5: [["Z1"]*43 + ["Z2"]*45 + ["Z3"]*10 + ["ZD"]*2, [70, 300], 2],
                        6: [["Z1"]*34 + ["Z2"]*45 + ["Z3"]*16 + ["ZD"]*5, [40, 275], 2.5],
                        7: [["Z1"]*22 + ["Z2"]*45 + ["Z3"]*24 + ["ZD"]*9, [10, 250], 3],
                        8: [["Z1"]*10 + ["Z2"]*40 + ["Z3"]*36 + ["ZD"]*14, [0, 225], 4],
                        9: [["Z2"]*31 + ["Z3"]*50 + ["ZD"]*19, [0, 200], 5],
                        10: [["Z2"]*15 + ["Z3"]*60 + ["ZD"]*25, [0, 175], 6.5],
                        11: [["Z3"]*68 + ["ZD"]*32, [0, 150], 8],
                        12: [["Z3"]*60 + ["ZD"]*40, [0, 100], 10],
                        13: [["ZD"]*1, [0, 0], float('inf')]}



always_spawn = []