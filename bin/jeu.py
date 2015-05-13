#!/usr/bin/python3
# -*- encoding: utf-8 -*

""" Module de jeu du produit.
    Ce module permet l'implémentation de la fonctionnalité de Jeu.
    Ce module possède une unique classe Jeu.

    Celle ci possède deux méthodes:
        - afficher(): affiche l'écran de jeu
        - jouer(): permet de jouer la grille

    Module importé:
        - pygame: utilisé pour l'affichage de l'écran de jeu et jeu d'une grille
        - grille, cases: utilisé pour manier la grille de jeu
        - sauvegarde: utilisé pour la sauvegarde et le chargement des grilles
        - boutons: utilisé pour manier les boutons de l'écran
        - solution: utilisé pour renvoyer le joueur vers l'écran de solution de la grille
        - constantes: utilisé par toutes les méthodes
        - exceptions: gestion des erreurs
"""

import pygame
from pygame.locals import *
import pygame.freetype
import grille
import sauvegarde
import impression
import boutons
import cases
import solution
from constantes import *
from exceptions import *

class Jeu:
    """ Modèle de donnée utilisé pour modéliser la phase de jeu, dans sa représentation graphique aussi bien que dans son fontionnement.
        Cette classe possède 8 attributs:
            - _fenetre: la fenetre d'affichage de l'écran
            - grille: la grille de jeu
            - bouton_reset: bouton permettant de reinitialiser la grille
            - bouton_retour: bouton permettant de retourner au menu
            - bouton_solution: bouton permettant de demander la solution d'une grille
            - bouton_sauvegarde: bouton permettant d'acceder à la fonctionnalité sauvegarde
            - bouton_impression: bouton permettant d'acceder à la fonctionnalité impression
            - barre_erreur: zone permettant d'afficher les erreurs de la grille
    """

    def __init__(self, fenetre, grille):
        """ Initialise les attributs de la classe.
            Une grille est fournie à l'interface de jeu, dans le but d'être jouée.
            La fenetre d'affichage est aussi passée en paramètre.
            La barre d'erreur est initialisée avec la position définie dans les constantes et un objet de type Font.
            Les autres éléments sont des boutons, qui seront complétés dans l'affichage de l'écran de jeu.
        """


        self._fenetre = fenetre
        self.grille = grille
        self.bouton_sauvegarde = boutons.Bouton(TITRE_BOUTON_SAUVEGARDE)
        self.bouton_impression = boutons.Bouton(TITRE_BOUTON_IMPRESSION)
        self.bouton_reset = boutons.Bouton(TITRE_BOUTON_RECOMMENCER)
        self.bouton_retour = boutons.Bouton(TITRE_BOUTON_MENU)
        self.bouton_solution = boutons.Bouton(TITRE_BOUTON_SOLUTION)

        self.barre_erreur = boutons.BarreErreur(pygame.freetype.Font(CHEMIN_FICHIER_POLICE, TAILLE_POLICE_BOUTON))


    def afficher(self):
        """ Méthode permettant d'afficher l'écran de jeu.
            Chacun des boutons de jeu est affiché.
            La zone d'affichage des erreurs est créée mais aucune image n'y est associée.
            La grille est par la suite affichée.
        """

        titre_bouton = pygame.freetype.Font(CHEMIN_FICHIER_POLICE, TAILLE_POLICE_BOUTON)
        bouton_img = pygame.image.load(CHEMIN_IMAGE_BOUTON).convert_alpha()

        self.bouton_sauvegarde.afficher(self._fenetre, bouton_img, titre_bouton, POSITION_BOUTON_SAUVEGARDE)
        self.bouton_impression.afficher(self._fenetre, bouton_img, titre_bouton, POSITION_BOUTON_IMPRESSION)
        self.bouton_reset.afficher(self._fenetre, bouton_img, titre_bouton, POSITION_BOUTON_RESET)
        if self.grille.solved:
            self.bouton_solution.afficher(self._fenetre, bouton_img, titre_bouton, POSITION_BOUTON_SOLUTION)
        self.bouton_retour.afficher(self._fenetre, bouton_img, titre_bouton, POSITION_BOUTON_RETOUR)
        self.grille.afficher_grille(self._fenetre)


    def jouer(self):
        """ Méthode permettant de jouer la grille.
            La méthode attend un événement et lance les méthodes associées à cet evenement.
            La méthode affiche la grille et ses éventuelles erreurs à chaque itération.
            L'utilisateur peut quitter le jeu en cours
        """

        while True:

            self._fenetre.fill(COULEUR_FOND)
            self.afficher()

            try:
                if self.grille.validate() and self.grille.victoire():
                    ecran_solution = solution.Solution(self._fenetre, self.grille, True)
                    ecran_solution.attente_evenement()
                    return
            except ExceptionMixte as em:
                self.barre_erreur.afficher_erreur(self._fenetre, em.message_erreur, COULEUR_ERREUR)
            except DoublonException as dbe:
                self.barre_erreur.afficher_erreur(self._fenetre, dbe.message_erreur, COULEUR_ERREUR)
            except SommeIncorrecteException as sie:
                self.barre_erreur.afficher_erreur(self._fenetre, sie.message_erreur, COULEUR_ERREUR)

            pygame.display.flip()

            for event in pygame.event.get():

                if event.type == QUIT:
                    pygame.quit()

                if event.type == MOUSEBUTTONUP and event.button == 1:
                    curseur = pygame.Rect(event.pos, (0,0))

                    if self.bouton_retour.clicked(curseur):
                        return

                    if self.bouton_reset.clicked(curseur):
                        self.grille.reinitialiser()

                    if self.grille.solved and self.bouton_solution.clicked(curseur):
                        self.grille.solve()
                        ecran_solution = solution.Solution(self._fenetre, self.grille, False)
                        ecran_solution.attente_evenement()
                        return

                    if self.bouton_sauvegarde.clicked(curseur):
                        ecran_sauvegarde = sauvegarde.Sauvegarde(self._fenetre, self.grille)
                        ecran_sauvegarde.sauvegarde()

                    if self.bouton_impression.clicked(curseur):
                        ecran_impression = impression.Impression(self._fenetre, self.grille)
                        ecran_impression.impression()

                    for(i,j) in self.grille.keys():
                        if type(self.grille[i,j]) == cases.CaseVide and self.grille[i,j].clicked(curseur):
                            self.grille[i,j].saisie_valeur(pygame.freetype.Font(CHEMIN_FICHIER_POLICE, TAILLE_POLICE_CASEVIDE), self._fenetre)
