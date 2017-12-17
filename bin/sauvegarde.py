#!/usr/bin/python3
# -*- encoding: utf-8 -*

""" Module de sauvegarde du produit.
    Ce module permet l'implémentation des fonctionnalités de Sauvegarde et Chargement.
    Ce module possède une classe Sauvegarde et une classe Chargement.

    Modules importés:
        - pygame: utilisé pour l'affichage
        - boutons: utilisé pour manier les boutons de l'écran
        - constantes: utilisé par toutes les méthodes
        - grille: utilisé pour intéragir avec la grille à sauvegarder
        - jeu: utilisé pour lancer le jeu d'une grille chargée
"""
import os
import pygame
from pygame.locals import *
import pygame.freetype
import boutons
import grille
import jeu
from constantes import *


class Sauvegarde:
    """ Classe modélisant la sauvegarde, dans son affichage aussi bien que dans son fontionnement.
        Cette classe possède 7 attributs:
            - _fenetre: la fenetre de jeu
            - _grille: la grille à sauvegarder
            - nom_fichier: le nom donné par le joueur
            - indication: l'indication donné au joueur
            - zone_saisie: la zone de saisie
            - bouton_valider: bouton permettant de valider la sauvegarde
            - bouton_retour: bouton permettant de revenir au jeu.
    """

    def __init__(self, fenetre, grille):
        """ Initialise les attributs de la classe.
            La fenetre d'affichage et la grille à imprimer sont passé en paramètre, les attributs correspondant sont initialisé avec ces valeurs.
            Le nom du fichier à sauvegarder est initialisé avec une chaine vide.
            Les autres éléments sont des boutons, qui seront initialisés dans l'affichage de l'écran de Sauvegarde.
            L'indication donnée au joueur est initialisé avec INDICATION_SAUVEGARDE, défini dans les constantes.
            La zone de saisie est initialisé avec un objet ZoneSaisie.
        """

        self._fenetre = fenetre
        self._grille = grille
        self.nom_fichier = ""
        self.indication = INDICATION_SAUVEGARDE
        self.zone_saisie = boutons.ZoneSaisie()
        self.bouton_valider = boutons.Bouton(TITRE_BOUTON_VALIDER)
        self.bouton_retour = boutons.Bouton(TITRE_BOUTON_RETOUR)

    def afficher(self):
        """ Méthode permettant d'afficher l'écran de sauvegarde à l'écran.
            Chacun des boutons de l'écran est affiché, ainsi que leur titre correspondant.
            La zone de saisie est aussi affiché au cours de cette étape.
        """

        img_saisie = pygame.image.load(CHEMIN_IMAGE_ZONE_SAISIE).convert()
        font_bouton = pygame.freetype.Font(CHEMIN_FICHIER_POLICE, TAILLE_POLICE_BOUTON)
        font_saisie = pygame.freetype.Font(CHEMIN_FICHIER_POLICE, TAILLE_POLICE_SAISIE)
        bouton_img = pygame.image.load(CHEMIN_IMAGE_BOUTON).convert_alpha()

        self.bouton_valider.afficher(self._fenetre, bouton_img, font_bouton, POSITION_BOUTON_SOLUTION)
        self.bouton_retour.afficher(self._fenetre, bouton_img, font_bouton, POSITION_BOUTON_RETOUR)
        self.zone_saisie.afficher(self._fenetre, img_saisie, font_saisie, POSITION_ZONE_SAISIE)

        self._fenetre.blit(font_saisie.render(self.indication, COULEUR_POLICE)[0], POSITION_INDICATION_SAUVEGARDE)

    def sauvegarde(self):
        """ Méthode permettant de sauvegarder la grille.
            La méthode attend un événement et lance le fonctionnement associé a cette événement.
            L'utilisateur peut quitter la sauvegarde pour revenir au jeu, ou quitter simplement le jeu.
            Il peut saisir une chaine, qui sera le nom du fichier de sauvegarde.
        """

        while True:

            self._fenetre.fill(COULEUR_FOND)
            self.afficher()

            pygame.display.flip()

            for event in pygame.event.get():

                if event.type == QUIT:
                    pygame.quit()

                if event.type == MOUSEBUTTONUP and event.button == 1:
                    curseur = pygame.Rect(event.pos, (0, 0))

                    if self.bouton_retour.clicked(curseur):
                        return

                    if self.zone_saisie.clicked(curseur):
                        self.nom_fichier = self.zone_saisie.saisie(self._fenetre, pygame.freetype.Font(CHEMIN_FICHIER_POLICE, TAILLE_POLICE_SAISIE))

                    if self.bouton_valider.clicked(curseur):
                        if (self.valider()):
                            return

    def valider(self):
        """ Méthode permettant de valider la sauvegarde.
            La chaine est formatée, l'extension lui est ajouté et le dossier de sauvegarde lui est ajouté.
            La méthode de sauvegarde de la grille est appellée.
        """

        if self.nom_fichier:
            if not os.path.isdir(CHEMIN_DOSSIER_SAUVEGARDE):
                os.mkdir(CHEMIN_DOSSIER_SAUVEGARDE)
            self.nom_fichier = self.nom_fichier.lower()
            self.nom_fichier = CHEMIN_DOSSIER_SAUVEGARDE + self.nom_fichier + EXTENSION_FICHIER_SAUVEGARDE
            self._grille.sauvegarde(self.nom_fichier)
            return True
        else:
            return False


class Chargement:
    """ Classe modélisant le chargement d'une grille.
        Cette classe possède 8 attributs:
            - _fenetre: la fenetre de jeu
            - _grille: la grille à charger
            - nom_fichier: le nom de la grille à charger
            - indication: L'indication donné au joueur
            - zone_saisie: la zone de saisie
            - bouton_valider: bouton permettant de valider le chargement.
            - bouton_retour: bouton permettant de revenir au jeu.
            - barre_erreur: zone d'affichage permettant d'afficher les erreurs à l'écran
    """

    def __init__(self, fenetre):
        """ Initialise les attributs de la classe.
            La fenetre d'affichage est passée en paramètre.
            le nom du fichier à charger est initialisé avec une chaine vide.
            Les autres éléments sont des boutons, qui seront initialisés dans l'affichage de l'écran de Chargement.
            L'indication donnée au joueur est initialisé avec INDICATION_CHARGEMENT, défini dans les constantes.
            La zone de saisie est initialisé avec un objet ZoneSaisie.
        """

        self._fenetre = fenetre
        self._grille = grille.Grille()
        self.nom_fichier = ""
        self.indication = INDICATION_CHARGEMENT
        self.zone_saisie = boutons.ZoneSaisie()
        self.bouton_valider = boutons.Bouton(TITRE_BOUTON_VALIDER)
        self.bouton_retour = boutons.Bouton(TITRE_BOUTON_RETOUR)

        self.barre_erreur = boutons.BarreErreur(pygame.freetype.Font(CHEMIN_FICHIER_POLICE, TAILLE_POLICE_BOUTON))

    def afficher(self):
        """ Méthode permettant d'afficher l'écran de chargement à l'écran.
            Chacun des boutons de l'écran est affiché, ainsi que leur titre correspondant.
            La zone de saisie et l'indication sont affichés dans cette méthode.
        """

        img_saisie = pygame.image.load(CHEMIN_IMAGE_ZONE_SAISIE).convert()
        font_bouton = pygame.freetype.Font(CHEMIN_FICHIER_POLICE, TAILLE_POLICE_BOUTON)
        font_saisie = pygame.freetype.Font(CHEMIN_FICHIER_POLICE, TAILLE_POLICE_SAISIE)
        bouton_img = pygame.image.load(CHEMIN_IMAGE_BOUTON).convert_alpha()

        self.bouton_valider.afficher(self._fenetre, bouton_img, font_bouton, POSITION_BOUTON_SOLUTION)
        self.bouton_retour.afficher(self._fenetre, bouton_img, font_bouton, POSITION_BOUTON_RETOUR)
        self.zone_saisie.afficher(self._fenetre, img_saisie, font_saisie, POSITION_ZONE_SAISIE)

        self._fenetre.blit(font_saisie.render(self.indication, COULEUR_POLICE)[0], POSITION_INDICATION_CHARGEMENT)

    def chargement(self):
        """ Méthode permettant de charger la grille.
            La méthode attend un événement et lance le fonctionnement associé à cet evenement.
            L'utilisateur peut quitter le chargement pour revenir au menu, ou quitter simplement le jeu.
            Il peut saisir un nom, qui sera le nom de fichier à charger.
            La pression du bouton validation lance la méthode validation.
        """

        erreur_saisie = False
        while True:

            self._fenetre.fill(COULEUR_FOND)
            self.afficher()
            if erreur_saisie:
                self.barre_erreur.afficher_erreur(self._fenetre, MESSAGE_ERREUR_NOM_INCORRECT, COULEUR_ERREUR)
            pygame.display.flip()

            for event in pygame.event.get():

                if event.type == QUIT:
                    pygame.quit()

                if event.type == MOUSEBUTTONUP and event.button == 1:
                    curseur = pygame.Rect(event.pos, (0, 0))

                    if self.bouton_retour.clicked(curseur):
                        return

                    if self.zone_saisie.clicked(curseur):
                        erreur_saisie = False
                        self.nom_fichier = self.zone_saisie.saisie(self._fenetre, pygame.freetype.Font(CHEMIN_FICHIER_POLICE, TAILLE_POLICE_SAISIE))

                    if self.bouton_valider.clicked(curseur):
                        if (self.valider()):
                            ecran_jeu = jeu.Jeu(self._fenetre, self._grille)
                            ecran_jeu.jouer()
                            return
                        else:
                            erreur_saisie = True

    def valider(self):
        """ Méthode permettant de valider la sauvegarde.
            La chaine est formatée, l'extension lui est ajouté et le dossier de sauvegarde lui est ajouté.
            La méthode de sauvegarde de la grille est appellée.
        """

        if self.nom_fichier != "":
            if not os.path.isdir(CHEMIN_DOSSIER_SAUVEGARDE):
                os.mkdir(CHEMIN_DOSSIER_SAUVEGARDE)
                return False
            self.nom_fichier = self.nom_fichier.lower()
            self.nom_fichier = CHEMIN_DOSSIER_SAUVEGARDE + self.nom_fichier + EXTENSION_FICHIER_SAUVEGARDE
            try:
                self._grille.chargement(self.nom_fichier)
                self._grille.solved = self._grille.is_solved()
            except Exception as e:
                return False

            return True
        else:
            return False
