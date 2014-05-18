# -*- coding: utf-8 -*-

import Tkinter
import tkMessageBox
import datetime

def check_entries_prom(lieu, date, t_deb, t_fin):

  res_test = False
  fin_test = False

  while fin_test != True:

    ########
    # LIEU #
    ########

    #Le lieu est entré
    lieu = str(lieu)
    if lieu == "":
      tkMessageBox.showwarning("Attention", "Le lieu n'a pas été saisi")
      res_test = False
      return res_test
    else:
      res_test = True

    ########
    # DATE #
    ########
    
    #Vérification de la date
    date_act = datetime.datetime.now()
    date_act = str(date_act)
  
    jour = date[0:2]
    jour_act = date_act[8:10]
    jour_act = int(jour_act)
    mois = date[3:5]
    mois_act = date_act[5:7]
    mois_act = int(mois_act)
    annee = date[6:10]
    annee_check = str(annee)
    annee_act = date_act[0:4]
    annee_act = int(annee_act)

    ##Vérifs générales
    #La taille est 10"
    if len(date) != 10:
      tkMessageBox.showwarning("Attention", "Mauvais format de date")
      res_test = False
      break
    else:
      res_test = True
      
    #Les slash sont aux bons endroits
    if (date[2] == "/") and (date[5] == "/"):
      res_test = True
    else:
      tkMessageBox.showwarning("Attention", "Mauvais format de date\n\
(attention aux '/')")
      res_test = False
      break
    
    ##MOIS
    #Le mois est un int
    try:
      mois = int(mois)
      res_test = True
    except:
      tkMessageBox.showwarning("Attention", "Mauvais format pour le mois")
      res_test = False
      break
    #Le mois est inférieur à 12 et supérieur à 0
    if mois < 13 and mois >0:
      res_test = True
    else:
      res_test = False
      tkMessageBox.showwarning("Attention", "Mauvais format pour le mois\n\
Les mois sont comprise entre 1 et 12")
      break

    ##JOUR
    #le jour est un int
    try:
      jour = int(jour)
      res_test = True
    except:
      tkMessageBox.showwarning("Attention", "Mauvais format pour le jour")
      res_test = False
      break
    #Le jour est <= à 30, et >0
    if (jour <= 31) and (jour >0):
      res_test = True
    else:
      tkMessageBox.showwarning("Attention", "Mauvais format pour le jour\n\
(Il y a entre 1 et 31 jours)")
      res_test = False
      break
    #Si le mois est 2 : il n'y a que 29 jours max
    if (mois == 3) and (jour > 29):
      tkMessageBox.showwarning("Attention", "Mauvais format pour le jour\
                                \n(février n'a pas 30 jours)")
      res_test = False
      break
    else:
      res_test = True

    ##ANNEE
    #L'année est un int
    try:
      annee = int(annee)
      res_test = True
    except:
      tkMessageBox.showwarning("Attention", "Mauvais format pour l'année")
      res_test = False
      break
    #l'année est cohérente (entre 1900 et 2099)
    if (annee_check[0] == '1' and annee_check[1] == '9') \
       or (annee_check[0] == '2' and annee_check[1] == '0'):
      res_test = True
    else:
      tkMessageBox.showwarning("Attention", "Choisir une année cohérente")
      res_test = False
      break
    
    #la date est inférieur à l'actuelle
    if annee > annee_act:
      tkMessageBox.showwarning("Attention", \
                               "L'année est supérieure à la date actuelle")
      res_test = False
      break
    elif (annee == annee_act) and (mois > mois_act):
      tkMessageBox.showwarning("Attention",\
                               "Le mois est supérieur à la date actuelle")
      res_test = False
      break
    elif (annee == annee_act) and (mois == mois_act) and (jour > jour_act):
      res_test = False
      tkMessageBox.showwarning("Attention",\
                               "Le jour est supérieur au jour actuel")
      break
    else:
      res_test = True

		
    ##################
    # Heure de début #
    ##################

    
    #On extrait les heures et les minutes
    m_deb = t_deb[3:5]
    h_deb = t_deb[0:2]
    #la taille fait 5
    if len(t_deb) == 5:
      res_test == True
    else:
      res_test = show_error("Mauvais format d'heure de début")
      break
    #Les deux points sont au milieu
    if t_deb[2] == ":":
      res_test = True
    else:
      res_test = show_error("Mauvais format d'heure de début\n(Attention aux ':')")
      break
    ##Heure de début
    #c'est un 'int'
    try:
      h_deb = int(h_deb)
      res_test = True
    except:
      res_test = show_error("Mauvais format d'heure de début")
      break
    #l'heure est comprise entre 0 et 23
    if (h_deb >= 0) and (h_deb <= 23):
      res_test = True
    else:
      res_test = show_error("Erreur dans l'heure de début\n(doit être comprise entre 0 et 23)")
      break
    ##Minute de début
    #C'est un 'int'
    try:
      m_deb = int(m_deb)
      res_test = True
    except:
      res_test = show_error("Mauvais format des minutes de l'heure de début")
      break
    #les minutes sont comprises entre 0 et 59
    if (m_deb >= 0) and (m_deb <= 59):
      res_test = True
    else:
      res_test = show_error("Erreur dans l'heure de début\n(doit être comprise entre 0 et 59")
      break


    ################
    # Heure de fin #
    ################

    
    #On extrait les heures et les minutes
    m_fin = t_fin[3:5]
    h_fin = t_fin[0:2]
    #la taille fait 5
    if len(t_fin) == 5:
      res_test == True
    else:
      res_test = show_error("Mauvais format d'heure de fin")
      break
    #Les deux points sont au milieu
    if t_fin[2] == ":":
      res_test = True
    else:
      res_test = show_error("Mauvais format d'heure de début\n(Attention aux ':')")
      break
    ##Heure de début
    #c'est un 'int'
    try:
      h_fin = int(h_fin)
      res_test = True
    except:
      res_test = show_error("Mauvais format d'heure de fin")
      break
    #l'heure est comprise entre 0 et 23
    if (h_fin >= 0) and (h_fin <= 23):
      res_test = True
    else:
      res_test = show_error("Erreur dans l'heure de fin\n(doit être comprise entre 0 et 23)")
      break
    ##Minute de début
    #C'est un 'int'
    try:
      m_fin = int(m_fin)
      res_test = True
    except:
      res_test = show_error("Mauvais format des minutes de l'heure de fin")
      break
    #les minutes sont comprises entre 0 et 59
    if (m_fin >= 0) and (m_fin <= 59):
      res_test = True
    else:
      res_test = show_error("Erreur dans l'heure de fin\n(doit être comprise entre 0 et 59")
      break
    ##Comparaison avec l'heure de début
    if (h_deb > h_fin) or ((h_deb == h_fin) and (m_deb > m_fin)):
      res_test = show_error("Heure de fin antérieure à l'heure de début")
      break
    else:
      res_test = True
      
    #Le test est fini
    fin_test = True
    
  return res_test


def show_error(text):
  res_test = False
  tkMessageBox.showwarning("Attention", text)
  return res_test

def check_entries_bird(Number):
  number = Number.get()
  res_test = False
  test_int = False
  fin_test = False
  while fin_test == False:
    try:
      number = int(number)
      test_int = True
    except:
      test_int = False

    if (number != "+") and (number != "++")\
        and (number != "+++") and (number != "++++")\
        and (test_int == False) and (number != ""):
      res_test = show_error("Mauvais format du nombre d'oiseaux")
      break
    else:
      res_test = True

    fin_test = True

  ##VERIFIER SI L'OISEAU EXISTE DEJA
  return res_test

    








