# The lessived
https://github.com/PaulJeFi/premier_jeu_nsi/blob/main/trailer.mp4

---

Notre premier jeu en NSI

---

Fichier "Image" :
- textures utilisés pour le jeu, sentez vous libre d'en ajouter
- ne sont en aucun cas obligées d'être intégrées au jeu

---

Je propose d'ajouter cette section pour inclure ce qui a été modifié.

 - j'ai (Paul) renommé les fichiers de Térence. En effet, Python ne lit pas toujours correctement les '-' et les espaces, ou les carractères spéciaux comme 'à'.

 - j'ai (Paul) créé un fichier main.py dans lequel je commence à créer l'arrière-plan.
 - j'ai fini pour l'animation de l'herbe. Je pense qu'il faudra changer l'image de l'herbe, le rendu est un peu dégueu.
 - j'ai (Térence) ajouté la majorité des images de ce projet.
 - (Paul) : Ajout de la barre de score et des trousses de soins. La détection de la collision entre le joueur et la trousse n'est pas fonctionnelle.
 - Ajout (Paul) d'une base d'intro, pour faire patienter pendant le chargement du jeu, que peut devenir lon avec l'initialisation des polices et des sons.
---

Idées et concepts pour le jeu :

---

 - Le jeu serait un survival zombie type "CoD (Call of Duty) zombie mode".
 - Il faut bien sûr les basiques :
     - Un grand arsenal d'armes
     - Pleins de zombies différents
     - Pas mal d'objets utiles (grenades, trousse de secours, potion de vitesse/force, armure, etc...)
     - Un mini tutoriel (écrit ou jouable)
---
 - La plupart des zombies attaquent au corps à corps.
 - Certains zombies ont des effets spéciaux, d'autres des attaques à distance.
 - Idées d'effets de zombie :
     - Un zombie qui en invoque d'autres faibles
     - Un autre qui peut lancer des projectiles explosifs / laser (pour diférencier de ceux avec les armes)
     - Un big boss avec des grosses stats
     - Un zombie tanky, un autre rapide, un qui est casiment invisible à moi que tu lui tire dessus, etc...
 - Les zombies peuvent dropent des objets, les plus forts ont plus de chance d'en drop.
---
 - Ce serait interressant d'avoir un système de pièces afin de pouvoir acheter des munitions et armes.
 - Il faudrait donc des armes de corps à corps ou un pistolet avec munition infinie (celui de base).
 - Il faudrait un compteur de score (1 pièce récupéré = 1 point gagné).
 - Tu ne perd bien sur pas de points lorsque tu dépense tes pièces.
 - Un système de high score.
 - Un petit plus un système d'archivements (vraiment pas obligé).
---
 - Tu pourrais trouver des caisses aléatoirement dans la map :
     - Les caisses apparaissent près du joueur, et disparaissent après un certain temps ou utilisation
     - La plupart te donneraient des pièces et munitions
     - D'autre te proposent d'achetter avec tes pièces des armes, armures, munitions et objets
     - Tu peux acheter seulement certains objets dans les caisses, définis aléatoirements
     - Certaines te donnent du stuff gratuit pas très puissant mais très pratique au début, ou des pièces et munitions
---
 - Un système de dificulté progressive :
     - Lorsque tu passes un certain palier de score, la dificulté augmente
     - Par exemple, plus de zombies forts apparaissent
     - Un brouillard assombrit les côtés de l'écran, rendant les zombies moins visibles
     - Plus la dificulté est élevée, plus les caisses proposent des articles interressant, mais à plus haut prix
     - Les ennemis spéciaux dropent plus d'argent
 - Quelque chose qui rendrait le jeu VRAIMENT SYMPA ça serait une ambiance de plus en plus horeur au fur et à mesure que la dificulté augmente.
    
     - Creer des animations en débuts et fin de jeu differents en fonction des du niveaux difficulté du jeu.
     - Ajouter des sons réagissant avec les actions dans le jeu 