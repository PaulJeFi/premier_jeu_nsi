'''
Ce script est là exclusivement pour créer des objets personnalisés.

Pour ce faire, suivez les instructions suivantes :
  -  Cette liste étant en réalité un dictionaire, il vous faudra écrire en clé le nom de votre objet.
     Ce nom sera affiché au joueur, et sera utilisé dans l'inventaire non-visuel (la liste contenant tous les objets).
  -  Après avoir mis le symbole " : ", il faudra que vous mettez une liste [].
     -  En premier élément de cette liste, vous mettrez les nom du fichier png du sprite de votre objet (sans mettre le .png).
        Votre image doit avoir pour chemin " ./src/images/inventaire/objets ".
     -  En deuxième élément vous pouvez entrer une description de votre objet que pourra lire le joueur.
        Vous pouvez simplement entrer "" si vous ne voulez pas en mettre.
        Pour afficher le texte sur plusieurs lignes tapez "|" sans espaces.
     -  Le dernier élement est le plus important : il vous faudra créer de nouveau une liste [].
        Dans celle-ci vous pourrez insérer les stats que donne votre objet.
        Pour se faire, entrez la stat à modifier, un espace puis la valeur suplémentaire (vous pouvez ajoutez un +/- devant la valeur pour la rendre positive ou négative).

En résumé, vous devriez obtenir quelque chose de cette forme :
    "L'armure démoniaque" : ["armure_enfer", "Cette armure provient des abisses de l'enfer", ["Vie -15", "Def +30", "Spe + 0.05"]]

Pour le moment, les stats sont :
  -  "Spe" pour la vitesse : La vitesse de base est de 1.
  -  "Def" pour la défence : Réduit tous les dommages reçus en les multipliant par " 0.99**<valeur_défence> ". La défence de base est 0.
  -  "Vie" pour la vie maximale : La vie maximale de base est 100. Réduit aussi le malus de régénération lorsque l'on prend des dégats (voir "Reg").
  -  "Reg" pour la régénération naturelle de pv : Chaque seconde, redonne <Reg> pv. Prendre des dégats réduit temporairement la régénération. La régénération naturelle de base est 1.
'''



stats_de_base = {"Spe" : 1, "Def" : 0, "Vie" : 100, "Reg" : 1, "Agi" : 0} # Stats de base du héro



definition_de_tous_les_objets = {"Bottes" : ["bottes", "De simples bottes...|Parfaites pour courrir de|longues distances !", ["Spe +0.06", "Def +4"]],
            "Armure dorée" : ["armure_doree", "Une splendide armure que|seuls les plus grands|capitaines ont portée.", ["Spe -0.02", "Def +20", "Agi +10"]],
            "Armure avec cape" : ["armure_cape", "Une armure ornée d'une|cape.", ["Spe +0.02", "Def +8", "Vie +8", "Agi +5"]],
            "Grand coeur" : ["grand_coeur", "Un vrai bonheur <3", ["Vie +24", "Reg +1"]],
            "Trèfle à 4 feuilles" : ["trefle_4_feuilles", "Quelle chance !", ["Spe +0.04", "Reg +0.5", "Agi +5"]],
            "Rune anti-vie" : ["anti_coeur", "Une puissance maléfique|l'aurait créée...|Serait-il raisonnable de|l'équiper ?", ["Spe +0.24", "Vie +150", "Reg -2.5"]],
            "Âme des flammes" : ["ame_feu", "Le pouvoir du démon des|flammes demeure dans ce|mystérieux fragment.", ["Spe +0.12", "Vie -15", "Reg +0.25", "Agi +5"]],
            "Bouclier du paladin" : ["bouclier_paladin", "Un splendide bouclier|qui vous protégera|face à toutes menaces.", ["Spe -0.12", "Def +28", "Vie +12", "Reg +0.25"]],
            "WINDOWS" : ["windows", "ERREUR FATALE||Si j'étais vous je|n'utiliserais pas cet|objet...", ["Spe +1.5", "Vie -10000"]],
            "Chapeau corrompu" : ["corruption", "Un simple chapeau...|Avec de la corruption|dessus.", ["Spe +0.2", "Agi +10", "Def -35"]],
            "Epée corrompue" : ["epee_corrompue", "Epée mytique du|grand Corrumpus.", ["Spe +0.04", "Vie +20", "Def +12", "Agi -15"]],
            "ADN de mutant" : ["genne_x", "De l'ADN provenant|d'un muttant...|Pour faire quoi ?|Aucune idée.", ["Vie +100", "Reg -0.5", "Def -10", "Agi -30"]],
            "[REDACTED]" : ["lessive", "Malheur à celui qui|oserait l'équiper !||Votre collègue en a|payé les frais.", []],
            "Pierre philosophale" : ["pierre_philosophale", "UN BEAU CAILLOU !|Mais surtout un super|atout pour votre quête.", ["Spe +0.04", "Vie +20", "Def +10", "Reg +0.25", "Agi +10"]],
            "Rune du vent" : ["rune", "Avec cette rune vous|devriez pouvoir aller un|peu plus vite...|Voir même très vite !", ["Spe +0.2", "Def -15", "Vie -5", "Agi -15"]],
            "Vieille veste" : ["vieille_veste", "Une veste très abimmé.|C'est mieux que rien.", ["Def +6", "Vie +6"]],
            "Vieille botte" : ["vieille_botte", "Une seule botte...|Espérons trouver|l'autre.", ["Spe +0.05"]],
            "Lunettes de gamer" : ["gamer_glasses", "YOLO SWAG M8|360° NO SCOPE|GAMER FOR EVER|2 STRONG 4 U", ["Spe +0.1", "Agi +30", "Vie -50"]],
            "Armure des enfers" : ["armure_demon", "Une armure forgée|au plus profond des|enfers.", ["Spe -0.1", "Reg -1", "Def +50"]]}