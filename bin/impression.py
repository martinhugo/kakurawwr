#!/usr/bin/python3
# -*- encoding: utf-8 -*

""" Module d'impression du produit.
    Ce module permet l'implémentation de la fonctionnalité Impression.

    Celle ci possède une méthode:
        - afficher(): affiche l'écran d'Impression.

    Modules importés:
        - pygame: utilisé pour l'affichage
        - boutons: utilisé pour manier les boutons de l'écran
        - constantes: utilisé par toutes les méthodes
"""
import os
import pygame
from pygame.locals import *
import pygame.freetype
import boutons
import pdf
from constantes import *



class Impression:
    """ Classe Impression, permet d'implémenter l'Impression.
        Cette classe possède 7 attributs:
            - _fenetre: la fenêtre de jeu
            - _grille: la grille à imprimer
            - nom_fichier: le nom donné par le joueur
            - indication: l'indication donné au joueur
            - zone_saisie: la zone de saisie
            - bouton_valider: bouton permettant de valider l'impression
            - bouton_retour: bouton permettant de revenir au jeu
    """

    def __init__(self, fenetre, grille):
        """ Initialise les attributs de la classe.
            La fenetre d'affichage est passée en paramètre.
            Les autres éléments sont des boutons, qui seront initialisés dans l'affichage de l'écran d'Impression.
        """

        self._fenetre = fenetre
        self._grille = grille
        self.nom_fichier = ""
        self.indication = INDICATION_SAUVEGARDE
        self.zone_saisie = boutons.ZoneSaisie()
        self.bouton_valider = boutons.Bouton(TITRE_BOUTON_VALIDER)
        self.bouton_retour = boutons.Bouton(TITRE_BOUTON_RETOUR)

    def afficher(self):
        """ Méthode permettant d'afficher l'écran d'impression à l'écran.
            Chacun des boutons de l'écran est affiché, ainsi que leur titre correspondant.
            La zone de saisie est aussi affichée au cours de cette étape.
        """

        img_saisie = pygame.image.load(CHEMIN_IMAGE_ZONE_SAISIE).convert()
        font_bouton = pygame.freetype.Font(CHEMIN_FICHIER_POLICE, TAILLE_POLICE_BOUTON)
        font_saisie = pygame.freetype.Font(CHEMIN_FICHIER_POLICE, TAILLE_POLICE_SAISIE)
        bouton_img = pygame.image.load(CHEMIN_IMAGE_BOUTON).convert_alpha()

        self.bouton_valider.afficher(self._fenetre, bouton_img, font_bouton, POSITION_BOUTON_SOLUTION)
        self.bouton_retour.afficher(self._fenetre, bouton_img, font_bouton, POSITION_BOUTON_RETOUR)
        self.zone_saisie.afficher(self._fenetre, img_saisie, font_saisie, POSITION_ZONE_SAISIE)

        self._fenetre.blit(font_saisie.render(self.indication, COULEUR_POLICE)[0], POSITION_INDICATION_SAUVEGARDE)

    def impression(self):
        """ Méthode permettant d'imprimer la grille.
            La méthode attend un événement et lance le fonctionnement associé a cette événement.
            L'utilisateur peut quitter l'impression pour revenir au jeu, ou quitter simplement le jeu.
        """
        
        while True:

            self._fenetre.fill(COULEUR_FOND)
            self.afficher()

            pygame.display.flip()

            for event in pygame.event.get():

                if event.type == QUIT:
                    pygame.quit()

                if event.type == MOUSEBUTTONUP and event.button == 1:
                    curseur = pygame.Rect(event.pos, (0,0))

                    if self.bouton_retour.clicked(curseur):
                        return

                    if self.zone_saisie.clicked(curseur):
                        self.nom_fichier = self.zone_saisie.saisie(self._fenetre, pygame.freetype.Font(CHEMIN_FICHIER_POLICE, TAILLE_POLICE_SAISIE))
                    
                    if self.bouton_valider.clicked(curseur):
                        self.valider()
                        return
                   
    def valider(self):
        """ Méthode permettant de valider l'impression.
            La chaine est formatée et la méthode d'impression de la grille est appellée.
        """
        if self.nom_fichier:
            if not os.path.isdir(CHEMIN_DOSSIER_IMPRESSION):
                os.mkdir(CHEMIN_DOSSIER_IMPRESSION)
            self.nom_fichier = self.nom_fichier.lower()
            self.nom_fichier = CHEMIN_DOSSIER_IMPRESSION + self.nom_fichier + EXTENSION_FICHIER_IMPRESSION

            pdf_creator = pdf.PDF()
            pdf_creator.generer_pdf(self._grille, self.nom_fichier)

            return True
        else:
            return False


