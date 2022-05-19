# The lessived
---

***The lessived*** est notre jeu de zombies. Pour en savoir plus, consultez notrenotebook [en ligne](https://github.com/PaulJeFi/premier_jeu_nsi/blob/main/main.ipynb) ou [en local](main.ipynb).

## Prérequis

Vérifiez pour lancer le jeu que vous ayiez une version de [Python](https://python.org) supérieure ou égale à la *3.6.0*.

Si vous n'avez pas [```Pygame```](https://www.pygame.org/news) avec, ouvrez le dossier du jeu dans un terminal et exécutez la commande suivante :

```
premier_jeu_nsi $ pip install -r requirements.txt
```


## Instruction pour lancer le jeu.

Il existe plusieurs moyens pour lancer notre jeu. Cette section est importante, car prendre un fichier et l'exécuter n'est pas forcément la meilleure chose que vous ayiez à faire.

**Il ne faut en aucun cas exécuter directement des fichiers du dossier ```src``` !**

- Celle que nous recommandons, se rendre dans le dossier du jeu dans un terminal et exécuter la commande suivante :

```
premier_jeu_nsi $ python src/menu.py
```

- Vous pouvez aussi ouvrir ```premier_jeu_nsi``` dans l'IDE de votre choix (nous conseillons fortement [VS Code](https://code.visualstudio.com)), puis chercher ```menu.py``` dans ```src```, et l'exécuter.

- Tout simplement, vous n'avez qu'à double-cliquer sur le fichier correspondant à votre système d'exploitation dans le dossier ```binaries```.

- Lancer ```run.py``` est aussi une bonne option.

- Exécuter les commandes suivantes succèssivement dans un terminal sans avoir téléchargé notre jeu fonctionnera aussi (à supposer que vous ayiez Python et [Git](https://git-scm.com) :

```
git clone https://github.com/PaulJeFi/premier_jeu_nsi.git
cd premier_jeu_nsi
python3 run.py
```
