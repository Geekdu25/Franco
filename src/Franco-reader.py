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
  #On rend certaines variables globales utilisables dans la fonction.
  global ligne, current_variable, variables, commence, checksum, sauvegarde, fonctions, recordVariable
  #On décompose le fichier en plusieurs lignes (qu'on appelle truc).
  for truc in fichier.read().splitlines():
    #On incrémente le numéro de ligne
    ligne = ligne + 1
    #Et on exécute cette ligne via la fonction execute_ligne
    #On stocke dans la variable result, un booléen. True si l'exécution de la ligne n'a pas déclenché d'erreur, False sinon.
    result = execute_ligne(truc)
    #Et si jamais la fonction nous renvoie une erreur, on arrête le programme
    if result==False:
        return False
  #Et si tout s'est bien passé on renvoie True    
  return True

def execute_ligne(laligne):
    """
    Fonction qui analyse une ligne passée en paramètre, et qui l'exécute.
    --------------------------------------------------
    laligne -> str
    return -> bool
    """
    #On rend certaines variables globales utilisables dans la fonction.
    global fichier, ligne, current_variable, variables, commence, checksum, sauvegarde, fonctions, recordVariable, filepath
    #On décompose la ligne en mots (qui sont séparés par des espaces).
    test = laligne.split(" ")
    mots = []
    #Et on stocke tous ces mots dans une variable mots.
    for mot in test:
      mots.append(mot)
    #Si l'utilisateur a déjà entré le mot clé debut...   
    if commence:
        #Si le premier mot de la ligne est definir, on indique à l'utilisateur qu'il ne peut pas définir de fonctions aprés avoir écrit debut.
        if mots[0] == "definir":
            print(f"Erreur ligne {ligne}")
            print("Vous ne pouvez pas définir une fonction après l'emploi de debut.")
            return False
        #Sinon, si le mot est afficher, on va afficher la phrase que l'utilisateur souhaite afficher.  
        elif mots[0] == "afficher":
            #Pour chaque mot se trouvant après afficher...
            for mot in mots[1:len(mots)]:
              #On n'a pas affaire à une variable, on va donc afficher le mot plus un espace.
              if not mot.startswith("#"):
                print(mot+" ", end="")
              #Sinon...  
              else:
                #Si le mot se trouve dans le dictionnaire variables...
                if mot[1:len(mot)] in variables:
                  #On affiche le contenu de cette variable et un espace.
                  print(str(variables[mot[1:len(mot)]])+" ", end="")
                else:
                  print(f"Erreur ligne {ligne}")
                  print("La variable n'existe pas.")
                  return False
            #Et on fait un petit retour à la ligne.      
            print()
        #Sinon, s'il y a plus de deux mots et qu'un espace se trouve en seconde position...  
        elif len(mots) > 2 and mots[1] == "=":
            #Si le troisième mot est un nombre entier, on enregistre un nombre entier.
            if mots[2].isdigit() and not "." in mots[2]:
                variables[mots[0]] = int(mots[2])
            #Si il a une virgule on l'enregistre comme un flottant.  
            elif mots[2].isdigit() and "." in mots[2]:
                variables[mots[0]] = float(mots[2])
            #Si il commence par des guillemets...
            #On enregistre cette variable comme une string...
            elif mots[2].startswith('"'):
                str_vide = ""
                for mot in mots[2:len(mots)]:
                    str_vide = str_vide + mot + " "
                variables[mots[0]] = str_vide[1:len(str_vide)-2]
            #Sinon, si le mot entré en troisième position est le mot entree  
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
                return False
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
            truc = truc[1:len(truc)]
        if i == len(expression) - 1:
            truc = truc[0:len(truc)-1]
        if truc.isdigit() and "." in truc:
            truc = float(truc)
        elif truc.isdigit() and not "." in truc:
            truc = int(truc)
        elif truc.startswith("#"):
            truc = variables[truc[1:len(truc)]]
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
