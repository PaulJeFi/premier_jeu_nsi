'''if __name__ == '__main__' :
    from main import Temps'''



# Definition de tous les zombies {"nom_d_appel" : ["nom_fichier_png", [vie, vitesse, attaque, régénération(pas encore fonctionnel)], score, [loot_table]]}
all_zombie_type = {"Z1" : ["Zombie_type_1", [100, 0.3, 0.25, 0], 250, [""]*400 + ["Vieille botte"]*7 + ["Vieille veste"]*7 + ["Bottes"]*2 + ["Armure avec cape"]*2 + ["Armure dorée"]*1],
                   "Z2" : ["Zombie_type_2", [150, 0.35, 0.35, 0], 350, [""]*350 + ["ADN de mutant"]*3 + ["Rune du vent"]*1 + ["Armure dorée"]*2 + ["Armure avec cape"]*2 + ["Bottes"]*4 + ["Grand coeur"]*1 + ["Trèfle à 4 feuilles"]*1],
                   "Z3" : ["Zombie_type_3", [225, 0.4, 0.5, 0], 500, [""]*300 + ["Epée corrompue"]*1 + ["Chapeau corrompu"]*1 + ["Trèfle à 4 feuilles"]*3 + ["Bouclier du paladin"]*4 + ["Âme des flammes"]*2 + ["Rune anti-vie"]*1]}
                   #"NON FONCTIONNEL" : ["Zombie_lessive", [(Temps().time%60)*25+100, (Temps().time%60)*0.02+0.3, (Temps().time%60)*0.04+0.4, (Temps().time%60)*0.5], 700, [""]*500 + ["De la ???????"]*2 + ["Epée corrompue"]*3 + ["Rune du vent"]*5 + ["Pierre PHILOSOPHALE"]*1]}



# Quels zombies apparraissent en fonction de la dificulté
# n° Vague : [[Spawn_liste], [temps_respawn_min, temps_respawn_max], temps_requis_pour_début_vague]
zombie_wave_spawn_rate = {0: [["Z1"]*100, [200, 400], 0],
                          1: [["Z1"]*90+["Z2"]*10, [180, 390], 0.25],
                          2: [["Z1"]*75+["Z2"]*25, [160, 370], 0.5],
                          3: [["Z1"]*60+["Z2"]*35+["Z3"]*5, [130, 345], 1],
                          4: [["Z1"]*40+["Z2"]*45+["Z3"]*15, [100, 310], 1.5],
                          5: [["Z1"]*30+["Z2"]*50+["Z3"]*20, [70, 270], 2],
                          6: [["Z1"]*20+["Z2"]*45+["Z3"]*35, [40, 230], 2.5],
                          7: [["Z1"]*10+["Z2"]*40+["Z3"]*50, [10, 200], 3],
                          8: [["Z2"]*35+["Z3"]*65, [0, 175], 4],
                          9: [["Z2"]*20+["Z3"]*80, [0, 150], 5],
                          10: [["Z2"]*10+["Z3"]*90, [0, 125], 6.5],
                          11: [["Z3"]*100, [0, 100], 8],
                          12: [["Z3"]*1, [0, 0], float('inf')]}