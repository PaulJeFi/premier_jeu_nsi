# Historiques des changements majeurs

  - La classe ```deplace``` dans ```main.py``` est une classe de construction servant de base pour d'autres classes, comme ```Zombies``` ou ```Soin```. Son but est d'apporter directement des méthodes de base à ces classes sans avoir à les réécrire. On l'utilise dès la construction des la classe (ex: ```class Soin(deplacer) :```).
  - Des comentaires ont étés ajoutés, la structure générale des fichiers a été modifiés (dans l'ordre : imports, constantes, initialisation de Pygame, classes et fonctions, code principal).
  - Le fichier ```Zombies.py``` est maintenant fonctionnel mais ne sert encore à rien.
  - Ajout d'un fichier ```.gitignore``` pour ignorer les modifications aux dossiers ```__pycache__``` (fichiés pré-compilés Python) et ```.DS_Store``` (des fichiers utilisés par Apple dans le Finder (équivalent de l'Explorateur de fichiers sous Window), qui ne servent pas à l'utilisateur).
  - Les fonctions ont été regroupées dans un nouveau fichier, ```functions.py```, dans lequel a notamment été déplacée la classe ```deplace```.
  - Dans la classe ```Score``` il faut oublier le consepte du brouillard car il cause beaucoup trop de ralentissements (genre sans le brouillard le jeu est ultra fluide)
  - Amélioration du jeu en général et correction de bugs
  - Méga ré-organisation des fichier. Veuillez me prévenir en cas de bug.
  - La création des fichiers de lancement, et la présentation du jeu et les instructions de lancement on été réalisées.