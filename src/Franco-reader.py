"""
Crée par Etienne Pacault et Lenny Couturier le 26 janvier 2024.
Ce programme python permet de lire les fichiers franco au format .frl
"""

#On importe la bibliothèque sys, qui nous permettera de charger un fichier passé en paramètre.
import sys

#On initialise quelques variables (numéro de ligne...)
ligne = 0
current_variable = ""
variables = {}
commence = False
checksum = 0
sauvegarde = None
fonctions = {}
recordVariable = False

def read_frl(fichier):
  """
  Fonction qui décompose un fichier .frl ligne par ligne
  ----------------------------------------------------------
  fichier -> fichier
  return -> bool
  """
  global ligne, current_variable, variables, commence, checksum, sauvegarde, fonctions, recordVariable
  for truc in fichier.read().splitlines():
    ligne = ligne + 1
    execute_ligne(truc)
  return True

def execute_ligne(laligne):
    """
    Fonction qui analyse une ligne passée en paramètre.
    --------------------------------------------------
    laligne -> str
    return -> bool
    """
    global fichier, ligne, current_variable, variables, commence, checksum, sauvegarde, fonctions, recordVariable, filepath
    test = laligne.split(" ")
    mots = []
    for mot in test:
      mots.append(mot)
    if commence:
        if mots[0] == "definir":
            print(f"Erreur ligne {ligne}")
            print("Vous ne pouvez pas définir une fonction après l'emploi de debut.")
            return False
        elif mots[0] == "afficher":
            for mot in mots[1:len(mots)]:
              if not mot.startswith("#"):
                print(mot+" ", end="")
              else:
                if mot[1:len(mots)] in variables:
                  print(str(variables[mot[1:len(mots)]])+" ", end="")
                else:
                  print(f"Erreur ligne {ligne}")
                  print("La variable n'existe pas.")
                  return False
            print()
        elif len(mots) > 2 and mots[1] == "=":
            if mots[2].isdigit():
                variables[mots[0]] = int(mots[2])
            elif mots[2].startswith("("):
                variables[mots[0]] = analyse_expression(mots[2:len(mots)])
            else:
                print(f"Erreur ligne {ligne}")
                print("Erreur lors de l'affectation de la variable.")
        elif mots[0] in fonctions:
            file = open(filepath, "rt")
            for loop in range(fonctions[mots[0]][0], fonctions[mots[0]][1]):
                print(fichier.read().splitlines())
                execute_ligne(fichier.read().splitlines()[loop])
    else:
        if mots[0] == "debut":
            commence = True
        elif mots[0] == "definir":
          if len(mots) == 3 and mots[2]=="{":
            fonctions[mots[1]] = [ligne, None]
            checksum = checksum + 1
            sauvegarde = mots[1]
          else:
            print(f"Erreur ligne {ligne}")
            print("Définition de fonction incorrecte")
            return False
        elif mots[0] == "}":
            checksum = checksum - 1
            if checksum == 0 and sauvegarde:
              fonctions[sauvegarde][1] = ligne
              sauvegarde = None

def analyse_expression(expression):
    global ligne, current_variable, variables, commence, checksum, sauvegarde, fonctions, recordVariable
    test = expression
    if len(test) > 2:
        if test[1] == "+":
            return int(test[0][1:len(test[0])]) + int(test[2][0:len(test[2])-1])
        elif test[1] == "-":
            return int(test[0][1:len(test[0])]) - int(test[2][0:len(test[2])-1])
        elif test[1] == "*":
            return int(test[0][1:len(test[0])]) * int(test[2][0:len(test[2])-1])
        elif test[1] == "/":
            return int(test[0][1:len(test[0])]) / int(test[2][0:len(test[2])-1])
        else:
            print(f"Erreur ligne {ligne}")
            print("Opération arithmétique non reconnue.")
    else:
        print(f"Erreur ligne {ligne}")
        print("Expression incorrecte.")

print("Les développeurs du langage Franco vous saluent !")
#On vérifie si l'utilisateurs a passé un nom de fichier en paramètre
#Si oui, on le charge, sinon, on lui demande un chemin d'accès.
if len(sys.argv) > 1:
    filepath = sys.argv[1]
else:
    filepath = input("Veuillez entrer un nom de fichier à lire : ")
#On charge le fichier.
if not filepath.endswith(".frl"):
    print("Le fichier n'a pas une extension correcte.")
    print("Essai d'ouverture...")
try:
  fichier = open(filepath,'rt')
except:
    print("Erreur lors du chargement du fichier.")
ok = read_frl(fichier)
fichier.close()
print()
if ok:
    print("Le programme s'est terminé sans problème")
else:
    print("Une erreur nous a forcé à interrompre le programme.")
