# -*- coding: utf-8 -*-

#A faire :
# Complétion sans changer les majuscules
# Accepter les caractères chelous
# Curseur au bon endroit => regarder complétion
# Edition de promenade et d'observation
# Vérifier que le même oiseau est pas encore saisi

# Fait :
# Afficher les dates dès qu'on clique sur la ville (sans passer par 'valider')
# Attention : n'enregistre PAS le dernier oiseau
# Trier les dates dans l'ordre décroissant


from Tkinter import *
import tkMessageBox
from fonction_oiseau import *
import pickle
from fonction_check_entries import*
#Module pour l'auto completion
from auto_completion import *


class InterfaceCreate(Frame):
    """On crée une classe qui hérite du frame
        Crée une fenêtre, tous les widgets sont des attributs de cette fenetre"""
    # On appelle le constructeur de la classe :
    def __init__(self, fenetre, **kwargs):
        # On appelle le constructeur du Frame pour l'associer à la fenetre
        Frame.__init__(self, fenetre, **kwargs)
        
        # On grid() (positionne et affiche le cadre)
        self.grid(row = 0)

        #On crée les Widgets :
        #creation de promenade
        self.B_prom = Button(self, text = "Nouvelle promenade",\
                             command = lambda : self.add_prom(fenetre))
        self.B_prom.grid(row = 1, column = 0, padx=10, pady=10)
        #creation d'observation
        self.B_obs = Button(self, text = "Nouvelle observation",\
                            command = lambda : self.add_bird(fenetre))
        self.B_obs.grid(row = 2, column = 0, padx=10, pady=10)

        self.B_quit= Button(self, text = "Quitter",\
                            command = fenetre.destroy)
        self.B_quit.grid(row = 3, column = 0, padx=10, pady=10)

    def add_prom(self, fenetre):
        """Méthode qui lance l'affichage de la fenêtre 'Balade'"""
        fenetre.destroy()
        fen_prom = Tk()
        fen_prom.title("Informations sur la promenade")
        interface_prom = InterfaceProm(fen_prom)
        interface_prom.mainloop()

    def add_bird(self, fenetre):
        fenetre.destroy()
        fen_choix_prom = Tk()
        fen_choix_prom.title("Choix de la promenade")
        interface_choix_prom = InterfaceChoixProm(fen_choix_prom)
        interface_choix_prom.mainloop()


class InterfaceProm(Frame):
    """On crée une classe qui hérite du frame
        Crée une fenêtre, tous les widgets sont des attributs de cette fenetre"""

    # On appelle le constructeur de la classe :
    def __init__(self, fen_prom, **kwargs):
        
        # On appelle le constructeur du Frame pour l'associer à la fenetre
        Frame.__init__(self, fen_prom, **kwargs)
        
        # On grid() (positionne et affiche le cadre)
        self.grid(row = 0)

        #On récupère les balades pour l'auto-complétion
        recup_bal = retrieve_lieu()
        recup_bal = [elt.lower() for elt in recup_bal]

        #On crée les Widgets :
        # Largeur des Entry
        large = 40
        #Lieu :
        self.L_lieu = Label(text = "Lieu de la balade").grid(row = 0, column = 0, sticky = W)
        lieu = StringVar()
##        self.E_lieu = Entry(fen_prom, width = large, textvariable = lieu)
        self.E_lieu = AutocompleteEntry(fen_prom, width = large, textvariable = lieu)
        self.E_lieu.set_completion_list(recup_bal)
        self.E_lieu.grid(row = 0, column = 1)

        #Date
        self.L_date = Label(text = "Date (jj/mm/aaaa) ").grid(row = 1, column = 0, sticky = W)
        date = StringVar()
        self.E_date = Entry(fen_prom, width = large, textvariable = date).grid(row = 1, column = 1)

        #heure début :
        self.L_deb = Label(text = "Heure début (hh:mm) ").grid(row = 2, column = 0, sticky = W)
        h_deb = StringVar()
        self.E_deb = Entry(fen_prom, width = large, textvariable = h_deb).grid(row = 2, column = 1)

        #heure fin :
        self.L_hfin = Label(text = "Heure fin (hh:mm) ").grid(row = 3, column = 0, sticky = W)
        h_fin = StringVar()
        self.E_fin = Entry(fen_prom, width = large, textvariable = h_fin).grid(row = 3, column = 1)

        #Descprition
        self.L_descr = Label(text = "Description").grid(row = 4, column = 0, sticky = W + N)
        self.T_descr = Text(fen_prom, width = large - 10, height = 15)
        self.T_descr.grid(row = 4, column = 1)
        
        #bouton Quitter
        self.B_quitter = Button(fen_prom, text = "Quitter", height = 2, width = 10,\
                                command = lambda :self.quit_fen_prom(fen_prom)).grid(row = 5, column = 0)

        #bouton creer
        self.B_create = Button(fen_prom, text = "Créer", height = 2, width = 10,\
                               command = lambda : self.create_prom(lieu, date, h_deb, h_fin, self.T_descr, fen_prom))
        self.B_create.grid(row = 5, column = 1)

    def quit_fen_prom(self, fen_prom):
        fen_prom.destroy()
        #On réaffiche la fenêtre principale
        fen_create = Tk()
        fen_create.title("Choisir une action")
        interface_create = InterfaceCreate(fen_create)
        interface_create.mainloop()

    def create_prom(self, lieu, date, h_deb, h_fin, T_descr, fen_prom):
        """ Actions effectuées :
            1) check des données
            2) On vérifie si le fichier data existe"""
        ##On récupère les différentes variables
        Lieu = lieu.get()
        Date = date.get()
        H_deb = h_deb.get()
        H_fin = h_fin.get()
        descr = T_descr.get('1.0', END+'-1c')

        #On vérifie ce qui a été rentré
        test_prom = check_entries_prom(Lieu, Date, H_deb, H_fin)

        #On enregistre seulement si test_prom = True
        if test_prom == True:
            #On met une majuscule au lieu (seulement s'il existe => après le test)
            prem_lettre = Lieu[0].upper()
            Lieu = prem_lettre + Lieu[1:]
            #on enregistre
            save_prom(Lieu, Date, H_deb, H_fin, descr)
            tkMessageBox.showinfo("Info", "Bravo,\n la promenade du {} au {} est enregistrée :)".format(Date, Lieu))
            fen_prom.destroy()
            #On ré-affiche la fenêtre principale
            fen_create = Tk()
            fen_create.title("Choisir une action")
            interface_create = InterfaceCreate(fen_create)
            interface_create.mainloop()


        

class InterfaceChoixProm(Frame):
    """Fenetre de choix de la promenade concernée par l'obs"""
    def __init__(self, fen_choix_prom, **kwargs):
        # On appelle le constructeur du Frame pour l'associer à la fenetre
        Frame.__init__(self, fen_choix_prom, **kwargs)

        # On grid() (positionne et affiche le cadre)
        self.grid(row = 0)  

        ##Récupération des lieux et dates :
        recup_bal = retrieve_lieu()
        
        ##Affichage du lieu
        #Label
        self.L_prom = Label(fen_choix_prom, text = "Choisir un lieu : ")
        self.L_prom.grid(row = 0, column = 0, sticky = W+N)
        #ListBox pour choisir la balade (avec Scrollbar)
        self.scrollbar_prom = Scrollbar(fen_choix_prom)
        self.LB_lieu = Listbox(fen_choix_prom, yscrollcommand = self.scrollbar_prom.set,\
                                height = 5, width = 35)
        self.scrollbar_prom.grid(row = 0, column = 2, sticky = W)
        self.scrollbar_prom.config( command = self.LB_lieu.yview)
        #Remplissage de la Listbox
        for elt in recup_bal:
            self.LB_lieu.insert(END, elt)
        #On associe 'get_clic' à la listbox
        self.LB_lieu.bind('<ButtonRelease-1>', self.clic)
        self.LB_lieu.grid(row = 0, column = 1, pady = 10)

        ##Affichage de la date
        #Label
        self.L_date = Label(fen_choix_prom, text = "Choisir une date : ")
        self.L_date.grid(row = 1, column = 0, sticky = W+N)
        #ListBox pour choisir la balade (avec Scrollbar)
        self.scrollbar_date = Scrollbar(fen_choix_prom)
        self.LB_date = Listbox(fen_choix_prom, yscrollcommand = self.scrollbar_date.set,\
                                height = 5, width = 35)
        self.scrollbar_date.grid(row = 1, column = 2, sticky = W)
        self.scrollbar_date.config(command = self.LB_date.yview)
        #Remplissage de la Listbox
        self.LB_date.grid(row = 1, column = 1, padx = 10, pady = 10)

        ##Bouton pour valider
        self.B_val_prom = Button(fen_choix_prom, text = "Valider le choix de promenade", \
                                 command = lambda : self.val_prom(fen_choix_prom))
        self.B_val_prom.grid(row = 2, column = 1, padx = 10)

        #Bouton pour quitter
        self.B_quit = Button(fen_choix_prom, text = "Quitter",\
                             command = lambda : self.quit_fen_choix_prom(fen_choix_prom))
        self.B_quit.grid(row = 2, column = 0, pady = 15)
        
    def clic(self, evt):
        index_prom = self.LB_lieu.curselection()
        index_prom = int(index_prom[0])
        self.LB_lieu.activate(index_prom)
        lieu = self.LB_lieu.get("active")

        with open("data_obs.txt", "r") as fichier:
            self.LB_date.delete(0, END)
            contenu = fichier.readlines()
            #readlines renvoie une liste avec une ligne par élément
            #Les lignes sont des string
            date = []
            for elt in contenu:
                #On enlève les \n en fin de ligne avec rstrip
                ligne = elt.rstrip('\n\r')
                #On sépare les éléments séparés par ';'
                mot = ligne.split(";")
                if mot[0] == lieu:
                    date.append(mot[1])
        #On trie la date :
        #inversion du format de date
        date_temp = ["{}/{}/{}".format(elt[6:10], elt[3:5], elt[0:2]) for elt in date]
        date_temp.sort()
        date = ["{}/{}/{}".format(elt[8:10], elt[5:7], elt[0:4]) for elt in date_temp]
        for elt in date:
            self.LB_date.insert(END, elt)

    def val_prom(self, fenetre):
        #Pas dangeureux de définir en global, car ils sont modifiés à chaque noueau choix de balade
        lieu = self.LB_lieu.get("active")
        date = self.LB_date.get("active")
        if date == "":
            tkMessageBox.showwarning("Attention", "Date non sélectionnée")
        else:
            choix = tkMessageBox.askokcancel("Info", "Promenade sélectionnée : \nLieu : {}\nDate : {}"\
                                  .format(lieu, date))
            if choix == True:
                #On enregistre le choix de lieu et de date, pour le récupérer après
                with open("temp", "wb") as fichier:
                    pickler = pickle.Pickler(fichier)
                    pickler.dump(lieu)
                    pickler.dump(date)
                fenetre.destroy()
                #On affiche la nouvelle fenêtre
                fen_bird = Tk()
                fen_bird.title("Ajout d'une observation")
                interface_bird = InterfaceBird(fen_bird)
                interface_bird.mainloop()

    def quit_fen_choix_prom(self, fenetre):
        fenetre.destroy()
        #On réaffiche la fenêtre principale
        fen_create = Tk()
        fen_create.title("Choisir une action")
        interface_create = InterfaceCreate(fen_create)
        interface_create.mainloop()


class InterfaceBird(Frame):
    """On crée une classe qui hérite du frame
        Crée une fenêtre, tous les widgets sont des attributs de cette fenetre"""

    # On appelle le constructeur de la classe :
    def __init__(self, fen_bird, **kwargs):
        
        # On appelle le constructeur du Frame pour l'associer à la fenetre
        Frame.__init__(self, fen_bird, **kwargs)
        
        # On grid() (positionne et affiche le cadre)
        self.grid(row = 0)

        #Test pour l'affichage des oiseaux
        self.test_fin_fam = False
        #Test pour vérifier si le TOUT DERNIER est déjà enregistré (sinon pb...)
        self.test_add_last_bird = False
        
        #On ouvre la liste de familles et d'oiseau
        global l_fam
        #On définit la liste d'oiseau comme un attribut
        self.l_bird = []
        self.l_bird_disp = []
        #On met les index à 0
        self.idx_fam = 0
        self.idx_ois = 0
        with open("data_oiseau", "rb") as data_ois:
            mon_unpickler = pickle.Unpickler(data_ois)
            l_fam = mon_unpickler.load()
            self.l_bird = mon_unpickler.load()
                        
        ##On crée les Widgets :
        #Bouton famille précédente :
        self.B_prev_fam = Button(fen_bird, text = "famille précédente",\
                                 command = self.disp_fam_prev)
        self.B_prev_fam.grid(row = 0, column = 0, padx=10, pady=10)
        #Bouton famille suivante :
        self.B_next_fam = Button(fen_bird, text = "famille suivante", command = self.disp_fam_suiv)
        self.B_next_fam.grid(row = 0, column = 1, padx=10, pady=10)
        #Label famille :
        self.L_fam = Label(fen_bird, text = "Nom de la famille : ")
        self.L_fam.grid(row = 1, column = 0)
        #Entry Famille :
        self.E_fam = Entry(fen_bird, width = 30)
        self.E_fam.insert(0, l_fam[self.idx_fam])
        self.E_fam.grid(row = 1, column = 1, pady=10)
        #Bouton 'oiseau précédent
        self.B_prev_bird = Button(fen_bird, text = "oiseau précédent",\
                             command = self.disp_bird_prev)
        self.B_prev_bird.grid(row = 2, column = 0, padx=10, pady=10)
        #Bouton 'oiseau suivant'
        self.B_next_bird = Button(fen_bird, text = "oiseau suivant",\
                             command = self.disp_bird_suiv)
        self.B_next_bird.grid(row = 2, column = 1, padx=10, pady=10)

        ##Entry nom de l'oiseau
        self.L_bird = Label(fen_bird, text = "Nom de l'oiseau : ")
        self.L_bird.grid(row = 3, column = 0)
        name_bird = StringVar()
        self.E_bird = Entry(fen_bird, width = 30, textvariable = name_bird)
        #Affiche direct le nom de l'oiseau
        self.E_bird.insert(0, self.l_bird[self.idx_fam][self.idx_ois])
        self.E_bird.grid(row = 3, column = 1)

        ##Entry nombre d'oiseaux
        self.L_number = Label(fen_bird, text = "Nombre d'oiseaux\n+ : 3-6\n++ : 6-11\
\n+++ : 11-20\n++++ : >20")
        self.L_number.grid(row = 4, column = 0)
        number_bird = StringVar()
        self.E_number = Entry(fen_bird, textvariable = number_bird, width = 30)
        self.E_number.grid(row = 4, column = 1, sticky = W)

        ##Text commentaire
        self.L_com = Label(fen_bird, text = "Commentaire")
        self.L_com.grid(row = 5, column = 0, sticky = N + W)
        self.T_com = Text(fen_bird, width = 22, height = 10)
        self.T_com.grid(row = 5, column = 1, sticky = N + W)

        #Bouton quitter
        self.B_quit = Button(fen_bird, text = "Quitter",\
                             command = lambda : self.quit_fen_bird(fen_bird))
        self.B_quit.grid(row = 6, column = 0, padx=10, pady=10)

        #Bouton ajouter
        self.B_add = Button(fen_bird, text = "Ajouter observation", \
                            command = lambda : self.add_bird(name_bird, number_bird))
        self.B_add.grid(row = 6, column = 1, padx=10, pady=10)

    def quit_fen_bird(self, fen_bird):
        fen_bird.destroy()
        #On réaffiche la fenêtre principale
        fen_create = Tk()
        fen_create.title("Choisir une action")
        interface_create = InterfaceCreate(fen_create)
        interface_create.mainloop()

    def disp_fam_suiv(self):
        #On remet à zéro
        self.idx_ois = 0
        self.E_bird.delete(0, END)
        self.E_number.delete(0, END)
        self.T_com.delete(1.0, END)

        self.idx_fam += 1
        if self.idx_fam > len(l_fam)-1:
            self.idx_fam = len(l_fam)-1
            #On est à la fin => affichage du 1er oiseau de la dernière liste
            self.E_bird.insert(0, self.l_bird_disp[0])
            tkMessageBox.showinfo("Info", "Fin des familles")
            self.test_fin_fam = True
        else:
            self.E_fam.delete(0, END)
            self.E_fam.insert(0, l_fam[self.idx_fam])
            self.l_bird_disp = self.l_bird[self.idx_fam]
            #On remet l'oiseau à jour
            self.E_bird.insert(0, self.l_bird_disp[self.idx_ois])
        
    def disp_fam_prev(self):
        self.idx_fam -= 1
        #On remet à zéro
        self.E_bird.delete(0, END)
        self.E_number.delete(0, END)
        self.T_com.delete(1.0, END)
        #On procède normalement
        if self.idx_fam < 0:
            #On est au tout début => affichage du 1er oiseau
            self.idx_fam = 0
            self.E_bird.insert(0, self.l_bird[self.idx_fam][self.idx_ois])
            tkMessageBox.showinfo("Info", "Déjà au début")
        else:
            #Si on était pas au début, on affiche le premier oiseau de la famille
            self.E_fam.delete(0, END)
            self.E_fam.insert(0, l_fam[self.idx_fam])
            self.l_bird_disp = self.l_bird[self.idx_fam]
            self.E_bird.insert(0, self.l_bird_disp[0])
            
    def disp_fam_prev_special(self):
        """methode qui met à jour l'affichage dans le cas où
            le nouvel oiseau est dans une famille AVANT, et s'il
            n'est PAS le premier oiseau"""
        #On remet à zéro
        self.E_fam.delete(0, END)
        self.E_bird.delete(0, END)
        self.E_number.delete(0, END)
        self.T_com.delete(1.0, END)
        #On remplit avec les bonnes données
        self.idx_ois = (len(self.l_bird[self.idx_fam])-1)
        self.E_bird.insert(0, self.l_bird[self.idx_fam][self.idx_ois])
        self.E_fam.insert(0, l_fam[self.idx_fam])

    def disp_bird_suiv(self):
        """Méthode pour gérer l'affichage de l'Entry 'oiseau'"""
        #Toutes les cases sont vidées
        self.E_bird.delete(0, END)
        self.E_number.delete(0, END)
        self.T_com.delete(1.0, END)
        #On itere idx_ois
        self.idx_ois += 1
        if self.idx_ois >= len(self.l_bird[self.idx_fam][:]):
            #On est à la fin de la famille, on passe à la famille suivante
            self.disp_fam_suiv()
        else:
            #sinon on affiche l'oiseau suivant
            self.E_bird.insert(0, self.l_bird[self.idx_fam][self.idx_ois])


    def disp_bird_prev(self):
        """Méthode pour gérer l'affichage de l'Entry 'oiseau'"""
        #Toutes les cases sont vidées
        self.E_bird.delete(0, END)
        self.E_number.delete(0, END)
        self.T_com.delete(1.0, END)
        #On itere idx_ois
        self.idx_ois -= 1
        #Si self.idx_ois est <0, on est au début d'une famille, soit tout début, soit pas
        if self.idx_ois < 0:
            #Soit on est au tout début
            if self.idx_fam <= 0:
                #On remet l'index des oiseaux à 0
                self.idx_ois = 0
                #On lance l'affichage de la famille précédente, qui détecte le début
                self.disp_fam_prev()
            #Soit on est pas au tout début
            else:
                #On affiche la famille précédente, avec le dernier oiseau de cette famille
                self.idx_fam -= 1
                self.disp_fam_prev_special()
        #Soit on est pas du tout à la fin d'une famille et tout va bien :)
        else:
            #On affiche la même famille, mais un oiseau avant
            self.E_bird.insert(0, self.l_bird[self.idx_fam][self.idx_ois])


    def add_bird(self, name, number):
        """Méthode pour ajouter un oiseau dans la base de donnée"""
        Name = name.get()
        Number = number.get()
        Com = self.T_com.get('1.0', END+'-1c')

        #On vérifie les données
        test_add_bird = check_entries_bird(number)
        if test_add_bird == True:
            #On enregistre les infos
            save_bird(Name, Number, Com)
            #on passe à l'oiseau suivant
            self.disp_bird_suiv()



