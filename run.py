import os
import platform

file_to_run = 'src/menu.py' # Chemin du fichier, depuis premier_jeu_nsi

# Obtention du dossier parent
dir_path = os.path.dirname(os.path.realpath(__file__))

# Obtention du système d'exploitation
system = platform.system()

# La suite n'est peut-être pas utile … à voir
if system == "Darwin" : # Si MacOS
    python = 'python3'
else : # Windoxs ou Linux
    python = 'python'

command2 = f'{python} {file_to_run}' # Commande d'exécution du fichier

os.system(f'{command2}')