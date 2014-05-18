# -*- coding: utf-8 -*-

import os
from Tkinter import *
from class_oiseau import *
import pickle

def save_prom(lieu, date, h_deb, h_fin, descr):
    """Fonction qui ajoute la promenade au fichier 'data_obs'"""
    with open("data_obs.txt", "a") as fichier_obs:
        fichier_obs.write("\n\n{};{};{};{};{}".\
                          format(lieu, date, h_deb, h_fin, descr))

def save_bird(bird, number, com):
    """Fonction qui ajoute l'obs au fichier 'data_obs.txt'"""
    #On récupère le lieu et la date
    with open("temp", "rb") as fichier:
        unpickler = pickle.Unpickler(fichier)
        lieu = unpickler.load()
        date = unpickler.load()
    #On enlève le saut de ligne
        Bird = bird.strip("\n")

    #On ajoute l'obs au bon endroit
    last_line = True
    with open("data_obs.txt", "r") as fichier_obs:
        idx1 = 0
        contenu = fichier_obs.readlines()
        for elt in contenu:
            mot = elt.split(";")
            if mot[0] == lieu and mot[1] == date:
                #idx1 est l'indice de la ligne avec le lieu
                #On repère l'indice de la ligne concernée (sans effacer idx1)
                idx2 = idx1
                #On vérifie que l'oiseau n'existe pas dans la liste de cette promenade
                #On cherche la première ligne vide
                for i in range(idx1, len(contenu)):
                    ligne = contenu[idx2].rstrip('\n')
                    mot = ligne.split(",")
                    if mot[0] == "":
                        last_line = False
                        #on récupère la partie AVANT la ligne à ajouter
                        part_1 = contenu[0:idx2]#idx2 non inclus => ok
                        #on récupère la partie APRES la ligne à ajouter
                        part_2 = contenu[idx2+1:]
                        #On ajoute la ligne à la fin de "part_1"
                        #Avec un saut de ligne après
                        part_1.append("{};{};{}\n\n"\
                                      .format(Bird, number, com))
                        #On ré-assemble les deux parties
                        part_1 += part_2
                        #On quitte la boucle
                        break
                    idx2 += 1
            #On met l'indice à jour
            idx1 += 1
    #On regarde 'last_line' pour voir s'il une ligne vide a été trouvée,
    #ou s'il faut ajouter à la fin
    if last_line == True:
        #Il faut ajouter à la fin
        with open("data_obs.txt", "a") as fichier:
            fichier.write("\n{};{};{}".\
                              format(Bird, number, com))
    else:
        #On remplace tout le fichier par part_1
        with open("data_obs.txt", "w") as fichier:
            for elt in part_1:
                fichier.write(elt)


def retrieve_lieu():
    """Fonction qui récupère les lieux des balades déjà entrées"""
    with open("data_obs.txt", "r") as fichier:
        toto = fichier.readlines()
        #readlines renvoie une liste avec une ligne par élément
        #Les lignes sont des string
        balade_temp = []
        for i in range(len(toto)-1):
            #On enlève les \n en fin de ligne avec rstrip
            ligne = toto[i].rstrip('\n\r')
            ligne1 = toto[i+1].rstrip('\n\r')
            #On sépare les éléments séparés par ';'
            mot = ligne.split(";")
            mot1 = ligne1.split(";")
            if mot[0] == "" and mot1[0] != "":
                balade_temp.append(mot1[0])
    balade = list(set(balade_temp))
    balade.sort()
    return balade




