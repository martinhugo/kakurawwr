#!/usr/bin/python3
# -*- encoding: utf-8 -*

""" Module d'impression du produit.
    Ce module permet l'implémentation de la fonctionnalité Impression.

    Celle ci possède trois méthodes:
        - positionnement: permet de définir le décalage à placer pour afficher les indicatrices
        - creer_grille: permet de générer la grille dans le document pdf
        - generer_pdf: permet de générer le pdf

    Modules importés:
        - constantes: utilisé dans chaque méthode
        - grille: utilisé pour tester les méthodes d'impression
        - fpdf: utilisé pour la génération d'un fichier pdf
"""

#Appel de la librairie
from constantes import *
import cases
from impression import *
from fpdf import *



class PDF(FPDF):

    """ Classe PDF, permet d'implémenter PDF.
        Cette classe ne possède qu'un seul attribut:
            - la grille qu'on lui envoie à partir de la classe Impression
    """

    def __init__(self):
        """ Méthode qui initialise la classe.
        """ 
        FPDF.__init__(self) 
             
    def header(self):
        """ Méthode qui permet de structurer l'ensemble de l'en-tête du document pdf.
            C'est aussi ici qu'on ajoutera l'image de jeu qui servira de titre au document.
        """

        self.set_font('Arial', 'B', 48)
        self.image(CHEMIN_IMAGE_KAKURAWWR, 20, 10, 170, 50)
        self.ln(20) 

    def footer(self):
        """ Méthode qui sert à définir le pied de page.
            On positionne donc le pied de page à 1,5cm du bas.
        """

        self.set_y(-15)
        self.set_font('Arial', 'B', 50)

    def positionnement(self, x, y, decalage):
        """ Méthode qui créée un décalage pour les valeurs des cases indicatrices.
            Elle contient une condition pour savoir si les abscisses et ordonnées sont des valeurs d'indicatrice de droite 
            ou d'indicatrice du bas.
        """

        if decalage == "droite":
            x += DECALAGE_X_DROIT
            y += DECALAGE_Y_DROIT
        elif decalage == "bas":
            x += DECALAGE_X_BAS
            y += DECALAGE_Y_BAS
        return x,y

    def creer_grille(self, grille):
        """ Méthode qui va générer la grille. Elle contient deux boucles lui permettant de parcourir toutes les lignes et les colonnes de la grille.
            Copie l'image des cases en fonction que celles-ci sont des cases noires, vides ou indicatrices.
            Dans le cas de cette dernière, on appelle une méthode précédement définie (positionnement) pour pouvoir avoir des abscisses et
            des ordonnées avec une position propre à la case indicatrice où seront affichées les valeurs.
        """
        
        #On place le début de la grille à la position (100,16) de la page
        x = 20
        y = 70
        i,j = 0,0

        while j < NB_LIGNE_GRILLE :

            i=0

            while i < NB_COLONNE_GRILLE:

                #Condition pour copier la valeur d'une indicatrice
                if type(grille[i,j]) == cases.Indicatrice:

                    #Copie de l'image indicatrice
                    self.image(CHEMIN_IMAGE_INDICATRICE, x, y, LARGEUR, HAUTEUR)

                    #Copie les valeurs de l'indicatrice dans la case correspondante.
                    x_droite, y_droite = self.positionnement(x, y, "droite")
                    x_bas, y_bas = self.positionnement(x, y, "bas")
                    self.text(x_droite, y_droite, str(grille[i,j].valeur_droite))
                    self.text(x_bas, y_bas, str(grille[i,j].valeur_bas))

                    x += 17

                #Copie l'image d'une case blanche
                elif type(grille[i,j]) == cases.CaseVide:
                    self.image(CHEMIN_IMAGE_CASEVIDE, x, y, LARGEUR, HAUTEUR)
                    x += 17

                #Copie l'image d'une case noire
                else :
                    self.image(CHEMIN_IMAGE_CASENOIRE,x,y, LARGEUR, HAUTEUR)
                    x += 17

                i += 1

            j += 1
            y += 17 #On descend d'une ligne
            x = 20 #On réinitialise à la valeur de base

    def generer_pdf(self, grille, nom_fichier):
        """ Méthode qui permet de générer le pdf.
        """
        self.add_page()
        self.set_font("Arial", size=12)
        self.creer_grille(grille)
        self.output(nom_fichier)


