"""
Crée par Etienne Pacault le 19 janvier 2024.
Ce programme python permet de lire les fichiers franco au format .frl
"""

#On importe la bibliothèque sys, qui nous permettera de charger un fichier passé en paramètre.
import sys


def read_frl():
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        filepath = input("Veuillez entrer un nom de fichier à lire : ")
    #On charge le fichier test.frl
    fichier = open(filepath,'rt')
    ligne = 0
    current_variable = ""
    variables = {}
    affichage = False
    recordVariable = False
    nb_mots = 0
    #Et on le lit
    for value in fichier.readlines():
      ligne = ligne + 1
      nb_mots = 0
      for mot in value.split():
        nb_mots = nb_mots + 1
        #Et si une ligne du fichier commence par afficher...
        if mot == 'afficher':
            affichage = True
        elif mot.startswith('"') and affichage:
          affichage = False
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
             return False
        elif not mot.startswith('"') and affichage:
            if mot in variables:
                print(variables[mot])
            else:
                print(f"Erreur ligne {ligne}")
                print(f"Vous utilisez le nom {mot}. Or ce nom n'est pas défini.")
                return False
        elif not mot in variables and nb_mots == 1:
          if mot[0].isdigit():
            print(f"Erreur à la ligne {ligne}.")
            print("Le nom d'une variable ne doit pas commencer par un chiffre.")
            return False
          else:
            variables[mot] = None
            current_variable = mot
            recordVariable = True
        elif recordVariable and nb_mots == 2:
          if mot != "=":
            print(f"Erreur ligne {ligne}.")
            print("Attention ! Vous essayez de définir une variable sans utiliser le signe =")
            return False
        elif recordVariable and nb_mots == 3:
            recordVariable = False
            if mot.isdigit():
                variables[current_variable] = int(mot)
    #On finit le programme en fermant le fichier
    fichier.close()
    return True

print("Les développeurs du langage Franco vous saluent !")
ok = read_frl()
if ok:
    print("Le programme s'est terminé sans problème")
else:
    print("Une erreur nous a forcé à interrompre le programme.")