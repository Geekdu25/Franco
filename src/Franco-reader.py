"""
Crée par Etienne Pacault et Lenny Couturier le 26 janvier 2024.
Ce programme python permet de lire les fichiers franco au format .frl
"""

#On importe la bibliothèque sys, qui nous permettera de charger un fichier passé en paramètre.
import sys
#Ainsi que la bibliothèque pygame, pour crée des jeux
import pygame

def read_frl():
    """
    Fonction qui permet de lire un fichier .frl
    -------------------------------------------
    return -> bool
    """
    #On vérifie si l'utilisateurs a passé un nom de fichier en paramètre
    #Si oui, on le charge, sinon, on lui demande un chemin d'accès.
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        filepath = input("Veuillez entrer un nom de fichier à lire : ")
    #On charge le fichier.
    fichier = open(filepath,'rt')
    #On initialise quelques variables (numéro de ligne, mode jeu...)
    ligne = 0
    current_variable = ""
    variables = {}
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
        pass
      #Si jamais une ligne commence par un #, c'est un commentaire.    
      if mots[0].startswith("#"):
            pass
      #Si l'utilisateur l'a souhaité, on active le mode jeu.    
      if mots[0] == "mode" and mots[1] == "jeu":
        #On initialise pygame et quelques calques.  
        mode_jeu = True
        pygame.init()
        calque1 = pygame.sprite.Group()
        calque2 = pygame.sprite.Group()
        calque3 = pygame.sprite.Group()
        calque4 = pygame.sprite.Group()
      if len(mots) > 1 and not mode_jeu:
        #Si le programmeur souhaite afficher quelque chose...  
        if mots[0] == 'afficher':
          #On saute une ligne...  
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
        elif not mots[0] in variables and len(mots)>2:
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
                  if mots[2].isdigit() and len(mots)==3:
                      variables[current_variable] = int(mots[2])
                  elif mots[2].isdigit() and len(mots)==5:
                    if mots[4].isdigit():
                      if mots[3] == "+":
                        variables[current_variable] = int(mots[2]) + int(mots[4])
                      elif mots[3] == "-":
                        variables[current_variable] = int(mots[2]) - int(mots[4])
                      elif mots[3] == "*":
                        variables[current_variable] = int(mots[2]) * int(mots[4])
                      elif mots[3] == "/":
                        variables[current_variable] = int(mots[2]) / int(mots[4])
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
      elif len(mots) > 3 and mode_jeu:
        if mots[0] == "couleur":
            try:
                background_color = (int(mots[1]), int(mots[2]), int(mots[3]))
            except:
                print(f"Erreur ligne {ligne}")
                print("Veuillez définir une couleur à l'aide de trois nombres entiers : Rouge Vert Bleu")
                return False
    #On finit le programme en fermant le fichier
    fichier.close()
    if mode_jeu:
        screen = pygame.display.set_mode((500, 500))
        pygame.display.set_caption("Jeu crée avec le Franco")
        boucle_de_jeu = True
        while boucle_de_jeu:
            screen.fill(background_color)
            calque1.draw(screen)
            calque2.draw(screen)
            calque3.draw(screen)
            calque4.draw(screen)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    boucle_de_jeu = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        boucle_de_jeu = False
    return True

print("Les développeurs du langage Franco vous saluent !")
ok = read_frl()
print()
if ok:
    print("Le programme s'est terminé sans problème")
else:
    print("Une erreur nous a forcé à interrompre le programme.")
