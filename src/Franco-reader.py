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
    mots = []
    #Et on le lit
    for value in fichier.readlines():
      ligne = ligne + 1
      mots = []
      for mot in value.split():
        mots.append(mot)
      if mots[0].startswith("#"):
            pass  
      if len(mots) > 1:
        if mots[0] == 'afficher':
          print()  
          affichage = True
          if mots[1].startswith('"'):
              try:
                truc = ""
                num  = 10
                while value[num] != '"':
                    truc += value[num]
                    num = num + 1
                print(truc, end="")
              except:
                  print(f"Erreur, ligne {ligne}")
                  print("Chaine de caractère non fermée.")
                  return False
          else:
              if mots[1] in variables:
                  print(variables[mots[1]], end="")
              else:
                  print(f"Erreur, ligne {ligne}")
                  print(f"{mots[1]}, n'est pas défini.")
                  return False
        elif not mots[0] in variables:
          if mots[0][0].isdigit():
            print(f"Erreur à la ligne {ligne}.")
            print("Le nom d'une variable ne doit pas commencer par un chiffre.")
            return False
          else:
            variables[mots[0]] = None
            current_variable = mots[0]
            recordVariable = True
            if mots[1] != "=":
              print(f"Erreur ligne {ligne}.")
              print("Attention ! Vous essayez de définir une variable sans utiliser le signe =")
              return False
            else:
              recordVariable = False
              if mots[2].isdigit():
                  variables[current_variable] = int(mots[2])
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
    #On finit le programme en fermant le fichier
    fichier.close()
    return True

print("Les développeurs du langage Franco vous saluent !")
ok = read_frl()
print()
if ok:
    print("Le programme s'est terminé sans problème")
else:
    print("Une erreur nous a forcé à interrompre le programme.")
