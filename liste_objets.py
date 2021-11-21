'''
Ce script est là exclusivement pour créer des objets personnlisés.

Pour ce faire, suivez les instructions suivantes :
  -  Cette liste étant en réalité un dictionaire, il vous faudra écrire en clé le nom de votre objet.
     Ce nom sera affiché au joueur, et sera utilisé dans l'inventaire non-visuel (la liste contenant tous les objets).
  -  Après avoir mis le symbole " : ", il faudra que vous mettez une liste [].
     -  En premier argument de cette liste, vous mettrez les nom du fichier png du sprite de votre objet (sans mettre le .png).
        Votre image doit avoir pour chemin " ./images/inventaire/objets ".
     -  En deuxième argument vous pouvez entrer une description de votre objet que pourra lire le joueur.
        Vous pouvez simplement entrer "" si vous ne voulez pas en mettre.
        Pour afficher le texte sur plusieurs lignes tapez "|" sans espaces.
     -  Le dernier argument est le plus important : il vous faudra créer de nouveau une liste [].
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



definition_de_tous_les_objets = {"Bottes" : ["bottes", "De simple bottes...|Parfaites pour courrir de|longues distances !", ["Spe +0.06", "Def +4"]],
            "Armure dorée" : ["armure_doree", "Une splendide armure que|seul les plus grands|capitaines ont portée.", ["Spe -0.02", "Def +20"]],
            "Armure avec cape" : ["armure_cape", "Une armure ornée d'une|cape.", ["Spe +0.02", "Def +8", "Vie +8"]],
            "Grand coeur" : ["grand_coeur", "Un vrai bonheur <3", ["Vie +24", "Reg +1"]],
            "Trèfle à 4 feuilles" : ["trefle_4_feuilles", "Quelle chance !", ["Spe +0.4", "Reg +0.5"]]}