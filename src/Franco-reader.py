"""
Crée par Etienne Pacault et Lenny Couturier le 26 janvier 2024.
Ce programme python permet de lire les fichiers franco au format .frl
"""

#On importe la bibliothèque sys, qui nous permettera de charger un fichier passé en paramètre.
import sys

def read_frl(fichier, debut=0, fin=0):
    """
    Fonction qui permet de lire un fichier .frl
    -------------------------------------------
    return -> bool
    """
    #On initialise quelques variables (numéro de ligne...)
    ligne = 0
    current_variable = ""
    variables = {}
    checksum = 0
    if fin == 0:
        fin = len(fichier.readlines())
    fonctions = {}
    affichage = False
    recordVariable = False
    mots = []
    mode_jeu = False
    background_color = (0, 0, 0)
    #Et on lit le fichier...
    #En le décomposant d'abord ligne par ligne...
    for value in fichier.readlines():
      ligne = ligne + 1
      mots = []
      #Puis mot par mot...
      for mot in value.split():
        if mot != "":
          mots.append(mot)
      if len(mots) == 0:
        continue
      #Si jamais une ligne commence par un #, c'est un commentaire.
      if mots[0].startswith("#"):
            pass
      elif mots[0] == "}" and checksum == 1:
        for fonction in fonctions:
            if fonction[1] == None:
                fonction[1] = ligne
                checksum = 0
      if checksum == 0:
          #Si le programmeur souhaite afficher quelque chose...
          if mots[0] == 'afficher':
            #On saute une ligne...
            affichage = True
            print()
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
          if mot[0] in fonctions:
            read_frl(fonctions[mot[0]][0], fonctions[mot[0]][1])

          elif mots[0] not in variables:
            if mots[0] == "definir" and mots[2]=="{":
              fonctions[mots[1]] = [ligne, None]
              checksum = checksum + 1
              continue
            elif mots[0][0].isdigit():
              print(f"Erreur à la ligne {ligne}.")
              print("Le nom d'une variable ne doit pas commencer par un chiffre.")
              return False
            if len(mots)>2:
              variables[mots[0]] = None
              current_variable = mots[0]
              recordVariable = True
              if mots[1] != "=":
                print(f"Erreur ligne {ligne}.")
                print("Attention ! Vous essayez de définir une variable sans utiliser le signe =")
                return False
              else:
                  recordVariable = False
                  if mots[2][0].isdigit() and len(mots)== 3 and not "." in mots[2]:
                      variables[current_variable] = int(mots[2])
                  elif mots[2][0].isdigit() and len(mots) == 3 and "." in mots[2]:
                      variables[current_variable] = float(mots[2])
                  elif mots[2][0].isdigit() and len(mots)==5:
                    if mots[4][0].isdigit():
                      if mots[3] == "+":
                        variables[current_variable] = float(mots[2]) + float(mots[4])
                      elif mots[3] == "-":
                        variables[current_variable] = float(mots[2]) - float(mots[4])
                      elif mots[3] == "*":
                        variables[current_variable] = float(mots[2]) * float(mots[4])
                      elif mots[3] == "/":
                        variables[current_variable] = float(mots[2]) / float(mots[4])
                      else:
                        print(f"Erreur ligne {ligne}")
                        print("Opération mathématique non reconnue")
                        return False
                    else:
                      print(f"Erreur ligne {ligne}")
                      print("Pour faire une opération avec un nombre, il faut un deuxième nombre.")
                      return False
                  elif mots[2].startswith('"') and mots[len(mots)-1].endswith('"'):
                      tmp = mots[2:len(mots)]
                      str_vide = ""
                      for truc in tmp:
                          if truc != tmp[len(tmp)-1]:
                            str_vide = str_vide + truc + " "
                          else:
                            str_vide = str_vide + truc
                      variables[current_variable] = str(str_vide[1:len(str_vide)-1])
                  elif mots[2].startswith('"') and not mots[len(mots)-1].endswith('"'):
                      print(f"Erreur ligne {ligne}")
                      print("Veuillez fermer votre chaîne de caractères par un guillemet.")
                      return False
                  if mots[2] in variables:
                      variables[current_variable] = variables[mots[2]]

      else:
          print(f"Erreur ligne {ligne}")
          print("Une erreur de syntaxe s'est produite.")
          return False
    #On finit le programme en fermant le fichier
    return True

print("Les développeurs du langage Franco vous saluent !")
#On vérifie si l'utilisateurs a passé un nom de fichier en paramètre
#Si oui, on le charge, sinon, on lui demande un chemin d'accès.
if len(sys.argv) > 1:
    filepath = sys.argv[1]
else:
    filepath = input("Veuillez entrer un nom de fichier à lire : ")
#On charge le fichier.
fichier = open(filepath,'rt')
ok = read_frl(fichier)
fichier.close()
print()
if ok:
    print("Le programme s'est terminé sans problème")
else:
    print("Une erreur nous a forcé à interrompre le programme.")
