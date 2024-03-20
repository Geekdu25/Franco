#!/usr/bin/python3
"""
Crée par Etienne Pacault et Lenny Couturier le 26 janvier 2024.
Ce programme python permet de lire les fichiers franco au format .frl
"""

#On importe la bibliothèque sys, qui nous permettera de charger un fichier passé en paramètre.
import sys

#On initialise quelques variables (numéro de ligne, la liste des variables, celle des fonctions...)
ligne = 0
current_variable = ""
variables = {}
commence = False
numt = 0
checksum = 0
current_checksum = 0
sauvegarde = None
fonctions = {}
recordVariable = False
mode_si = False


def read_frl(fichier):
  """
  Fonction qui décompose un fichier .frl ligne par ligne
  ----------------------------------------------------------
  fichier -> fichier
  return -> bool
  """
  #On rend certaines variables globales utilisables dans la fonction.
  global ligne, current_variable, variables, commence, checksum, sauvegarde, fonctions, recordVariable, mode_si, current_checksum, numt
  #On décompose le fichier en plusieurs lignes (qu'on appelle truc).
  for truc in fichier.read().splitlines():
    ligne = ligne + 1
    #Et on exécute cette ligne via la fonction execute_ligne
    #On stocke dans la variable result, un booléen. True si l'exécution de la ligne n'a pas déclenché d'erreur, False sinon.
    if not mode_si and not f"tmp{numt-1}" in fonctions.keys():
      result = execute_ligne(truc)
      #Et si jamais la fonction nous renvoie une erreur, on arrête le programme
      if result==False:
          return False
    else:
      if "{" in truc:
        checksum = checksum + 1
      if "}" in truc:
        checksum = checksum - 1
      if checksum == current_checksum and mode_si:
        mode_si = False
      elif checksum == current_checksum and f"tmp{numt-1}" in fonctions.keys():
        fonctions[f"tmp{numt-1}"][2] = ligne
        while analyse_expression(fonctions[f"tmp{numt-1}"][0]):
            file = open(filepath, "rt", encoding="UTF-8")
            lignen = fonctions[f"tmp{numt-1}"][1]
            for truc in file.read().splitlines()[fonctions[f"tmp{numt-1}"][1]:fonctions[f"tmp{numt-1}"][2]]:
                lignen = lignen + 1
                execute_ligne(truc)
                if lignen == fonctions[f"tmp{numt-1}"][2]:
                    break
        del fonctions[f"tmp{numt-1}"]
        numt = numt - 1
  #Et si tout s'est bien passé on renvoie True
  return True

def execute_ligne(laligne):
    """
    Fonction qui analyse une ligne passée en paramètre, et qui l'exécute.
    --------------------------------------------------
    laligne -> str
    return -> bool
    """
    global fichier, ligne, current_variable, variables, commence, checksum, sauvegarde, fonctions, recordVariable, filepath, mode_si, current_checksum, numt
    #On décompose la ligne en mots (qui sont séparés par des espaces).
    test = laligne.split(" ")
    mots = []
    #Et on stocke tous ces mots dans une variable mots.
    for mot in test:
      if mot != "":
        mots.append(mot)
    if len(mots) > 0:
        if commence:
            #-------------------DEFINITION INTERDITE----------------------------
            if mots[0] == "definir":
                print(f"Erreur ligne {ligne}")
                print("Vous ne pouvez pas définir une fonction après l'emploi de debut.")
                return False
            elif mots[0] ==  "}":
              if checksum > 0:
                checksum = checksum - 1
              else:
                checksum = 0
            elif mots[0] == "si" and len(mots) > 2:
              if not mots[len(mots)-1] == "{":
                print(f"Erreur ligne {ligne}")
                print("Il faut finir une ligne conditionnelle avec un {.")
                return False
              current_checksum = checksum
              checksum = checksum + 1
              expression = mots[1:len(mots)-1]
              alors = analyse_expression(expression)
              if not alors:
                mode_si = True
            #---------------------------AFFICHER------------------------------
            elif mots[0] == "afficher":
                for mot in mots[1:len(mots)]:
                  if not mot.startswith("#"):
                    print(mot+" ", end="")
                  else:
                    if mot[1:len(mot)] in variables:
                      if type(variables[mot[1:len(mot)]]) is int():
                        print(str(round(variables[mot[1:len(mot)]]))+" ", end="")
                      else:
                        print(str(variables[mot[1:len(mot)]])+" ", end="")
                    else:
                      print(f"Erreur ligne {ligne}")
                      print("La variable n'existe pas.")
                      return False
                print()
            #----------------AFFECTATION DE VARIABLE--------------------
            elif len(mots) > 2 and mots[1] == "=":
                if mots[2].isdigit():
                    variables[mots[0]] = float(mots[2])
                elif mots[2].startswith("#"):
                  try:
                    variables[mots[0]] = variables[mots[2][1:len(mots[2])]]
                  except:
                    print(f"Erreur ligne {ligne}")
                    print(f"La variable {mots[2][1:len(mots[2])]}, n'existe pas.")
                    return False
                elif mots[2] == "Vrai" or mots[2] == "Faux":
                  variables[mots[0]] = mots[2]
                #--------------------INPUT----------------------------------
                elif mots[2] == "entree":
                    str_vide = ""
                    if len(mots) > 3:
                      for mot in mots[3:len(mots)]:
                          str_vide = str_vide + mot + " "
                    result = input(str_vide)
                    if result.isdigit():
                        result = float(result)
                    variables[mots[0]] = result
                #-----------------------EXPRESSION-------------------------
                elif mots[2].startswith("("):
                    variables[mots[0]] = int(analyse_expression(mots[2:len(mots)]))
                else:
                    print(f"Erreur ligne {ligne}")
                    print("Erreur lors de l'affectation de la variable.")
                    return False
            #--------------------EXECUTION DE FONCTION---------------------
            elif mots[0] in fonctions:
                file = open(filepath, "rt", encoding="UTF-8")
                lignen = fonctions[mots[0]][0]
                for truc in file.read().splitlines()[fonctions[mots[0]][0]:fonctions[mots[0]][1]]:
                    lignen = lignen + 1
                    execute_ligne(truc)
                    if lignen == fonctions[mots[0]][1]:
                        break
            elif mots[0] == "tant_que" and len(mots) > 2 and mots[len(mots)-1] == "{":
              fonctions[f"tmp{numt}"] = [mots[1:len(mots)-1], ligne, None]
              numt = numt + 1
              checksum = checksum + 1
        #Le programme n'a pas encore commencé
        else:
            #------------------DEBUT-----------------
            if mots[0] == "debut":
                commence = True
            #----------------DEFINITION DE FONCTION---------------------
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
    """
    Fonction qui analyse une expression passée en paramètre.
    --------------------------------------------------------
    expression -> list
    return -> int ou bool
    """
    global ligne, current_variable, variables, commence, checksum, sauvegarde, fonctions, recordVariable
    test = []
    i = 0
    #On traite de manière différente chaque élément de l'expression (un nombre par exemple...)
    for truc in expression:
        if i == 0:
            truc = truc[1:len(truc)]
        if i == len(expression) - 1:
            truc = truc[0:len(truc)-1]
        if truc.isdigit():
            truc = float(truc)
        elif truc.startswith("#"):
            truc = variables[truc[1:len(truc)]]
            if truc == "Vrai":
              truc = True
            elif truc == "Faux":
              truc = False
        test.append(truc)
        i = i + 1
    partie1 = None
    partie2 = None
    #Si nous avons un booléen...
    if len(test) == 1:
      if test[0] == "Vrai":
        return True
      elif test[0] == "Faux":
        return False
      else:
        print(f"Erreur ligne {ligne}")
        print("Booléen non reconnu")
    #Si nous avons affaire à un calcul simple...on calcule.
    elif len(test) > 2:
      if partie1 == None:
        if test[1] == "+":
            partie1 = test[0] + test[2]
        elif test[1] == "-":
            partie1 =  test[0] - test[2]
        elif test[1] == "*":
            partie1 =  test[0] * test[2]
        elif test[1] == "/":
            partie1 =  test[0] / test[2]
        elif test[1] == "%":
          partie1 =  test[0] % test[2]
        elif test[1] == "//":
          partie1 =  test[0] // test[2]
        elif test[1] == "=":
          partie1 =  test[0] == test[2]
        elif test[1] == "!":
          partie1 =  test[0] != test[2]
        elif test[1] == ">":
          partie1 =  test[0] > test[2]
        elif test[1] == "<":
          partie1 =  test[0] < test[2]
        elif test[1] == "<=":
          partie1 =  test[0] <= test[2]
        elif test[1] == ">=":
          partie1 =  test[0] >= test[2]
        elif test[1] == "**":
          partie1 =  test[0] ** test[2]
        else:
            print(f"Erreur ligne {ligne}")
            print("Opération non reconnue.")
      if partie2 == None and len(test) > 6:
        if test[5] == "+":
            partie2 = test[4] + test[6]
        elif test[5] == "-":
            partie2 =  test[4] - test[6]
        elif test[5] == "*":
            partie2 =  test[4] * test[6]
        elif test[5] == "/":
            partie2 =  test[4] / test[6]
        elif test[5] == "%":
          partie2 =  test[4] % test[6]
        elif test[5] == "//":
          partie2 =  test[4] // test[6]
        elif test[5] == "=":
          partie2 =  test[4] == test[6]
        elif test[5] == "!":
          partie2 =  test[4] != test[6]
        elif test[5] == ">":
          partie2 =  test[4] > test[6]
        elif test[5] == "<":
          partie2 =  test[4] < test[6]
        elif test[5] == "<=":
          partie2 =  test[4] <= test[6]
        elif test[5] == ">=":
          partie2 =  test[4] >= test[6]
        elif test[5] == "**":
          partie2 =  test[4] ** test[6]
        else:
            print(f"Erreur ligne {ligne}")
            print("Opération non reconnue.")
      if len(test) == 3:
          return partie1
      elif len(test) == 7:
          if test[3] == "et":
            return partie1 and partie2
          elif test[3] == "ou":
            return partie1 or partie2
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
  fichier = open(filepath,'rt', encoding="UTF-8")
except:
    print("! Erreur lors du chargement du fichier !")
else:
  ok = read_frl(fichier)
  fichier.close()
  print()
  if ok:
      print("Le programme s'est terminé sans problème")
  else:
      print("Une erreur nous a forcé à interrompre le programme.")
input("Appuyez sur une touche pour continuer...")
