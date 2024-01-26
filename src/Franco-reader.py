"""
Crée par Etienne Pacault le 19 janvier 2024.
Ce programme python permet de lire les fichiers franco au format .frl
"""

#On importe la bibliothèque sys, qui nous permettera de charger un fichier passé en paramètre.
import sys

if len(sys.argv) > 1:
    filepath = sys.argv[1]
else:
    filepath = input("Veuillez entrer un nom de fichier à lire : ")
#On charge le fichier test.frl
fichier = open(filepath,'rt')
ligne = 0
#Et on le lit
for value in fichier.readlines():
  ligne = ligne + 1
  #Et si une ligne du fichier commence par afficher...
  if value.startswith('afficher("'):
    fin = 10
    try:
      while value[fin] != '"':
        fin = fin + 1
        truc = value[10:fin]
        #On affiche quelque chose
      print(truc)
    except IndexError:
       print("Une erreur s'est produite.")
       print(f"Avez-vous fermé l'instruction ligne {ligne} par des guillemets ?")
#On finit le programme en fermant le fichier
fichier.close()