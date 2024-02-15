#!/usr/bin/python3
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
    result = execute_ligne(truc)
    if result==False:
        return False
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
            if mots[2].isdigit() and not "." in mots[2]:
                variables[mots[0]] = int(mots[2])
            elif mots[2].isdigit() and "." in mots[2]:
                variables[mots[0]] = float(mots[2])
            elif mots[2].startswith('"'):
                str_vide = ""
                for mot in mots[2:len(mots)]:
                    str_vide = str_vide + mot + " "
                variables[mots[0]] = str_vide[1:len(str_vide)-2]
            elif mots[2] == "entree":
                str_vide = ""
                for mot in mots[3:len(mots)]:
                    str_vide = str_vide + mot + " "
                result = input(str_vide)
                if result.isdigit() and not "." in result:
                    result = int(result)
                elif result.isdigit() and "." in result:
                    result = float(result)
                variables[mots[0]] = result
            elif mots[2].startswith("("):
                variables[mots[0]] = analyse_expression(mots[2:len(mots)])
            else:
                print(f"Erreur ligne {ligne}")
                print("Erreur lors de l'affectation de la variable.")
        elif mots[0] in fonctions:
            file = open(filepath, "rt")
            lignen = fonctions[mots[0]][0]
            for truc in file.read().splitlines()[fonctions[mots[0]][0]:fonctions[mots[0]][1]]:
                lignen = lignen + 1
                execute_ligne(truc)
                if lignen == fonctions[mots[0]][1]:
                    break
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
    test = []
    i = 0
    for truc in expression:
        if i == 0:
            truc = truc[1:len(expression)]
        if i == len(expression) - 1:
            truc = truc[0:len(truc)-1]
        if truc.isdigit() and "." in truc:
            truc = float(truc)
        if truc.isdigit() and not "." in truc:
            truc = int(truc)
        test.append(truc)
        i = i + 1
    if len(test) > 2:
        if test[1] == "+":
            return test[0] + test[2]
        elif test[1] == "-":
            return test[0] - test[2]
        elif test[1] == "*":
            return test[0] * test[2]
        elif test[1] == "/":
            return test[0] / test[2]
        elif test[1] == "%":
          return test[0] % test[2]
        elif test[1] == "//":
          return test[0] // test[2]
        else:
            print(f"Erreur ligne {ligne}")
            print("Opération non reconnue.")
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
