#!/usr/bin/python3
# -*- encoding: utf-8 -*

""" Module de solution du produit.
    Ce module permet l'implémentation de la fonctionnalité Solution.
    Ce module possède une unique classe Solution.

    Celle ci possède deux méthodes:
        - afficher(): affiche l'écran de jeu
        - attente_evenement(): permet de jouer la grille

    Module importé:
        - pygame: utilisé pour l'affichage de l'écran de jeu et jeu d'une grille
        - grille: utilisé pour manier la grille de jeu
        - boutons: utilisé pour manier les boutons de l'écran
        - constantes: utilisé par toutes les méthodes
        - grille: permet l'affichage de la grille résolu
"""

import pygame
from pygame.locals import *
import pygame.freetype
import grille
import boutons
from constantes import *

class Solution:
    """ Classe Solution, permet d'afficher la solution d'une grille.
        Cette classe possède 8 attributs:
            - _fenetre: la fenetre d'affichage de l'écran
            - grille: la grille de jeu
            - bouton_menu: bouton permettant de retourner au menu
            - victoire: boolean permettant de savoir si le joueur à gagner ou à demander la solution
            - barre_erreur: zone permettant d'afficher les erreurs de la grille
    """

    def __init__(self, fenetre, grille, victoire):
        """ Initialise les attributs de la classe.
            Une grille et la fenêtre passé en paramètre initialise les attributs correspondants.
            La barre d'erreur est initialisé avec la position défini dans les constantes et un objet de type Fon
            L'attribut victoire est initialisé avec le paramètre victoire.
            Les autres éléments sont des boutons, qui seront initialisé dans l'affichage de l'écran de jeu.
        """

        
        self._fenetre = fenetre
        self.grille = grille
        self.bouton_menu = boutons.Bouton(TITRE_BOUTON_MENU)
        self.barre_erreur = boutons.BarreErreur(pygame.freetype.Font(CHEMIN_FICHIER_POLICE, TAILLE_POLICE_BOUTON))
        self.victoire = victoire


    def afficher(self):
        """ Méthode permettant d'afficher l'écran de solution à l'écran.
            Le bouton menu est affiché, ainsi que la barre d'erreur et la grille.
        """

        titre_bouton = pygame.freetype.Font(CHEMIN_FICHIER_POLICE, TAILLE_POLICE_BOUTON)
        bouton_img = pygame.image.load(CHEMIN_IMAGE_BOUTON).convert_alpha()
                                                
        self.bouton_menu.afficher(self._fenetre, bouton_img, titre_bouton, POSITION_BOUTON_SOLUTION)
        self.grille.afficher_grille(self._fenetre)

        if self.victoire:
            self.barre_erreur.afficher_erreur(self._fenetre, MESSAGE_VICTOIRE, COULEUR_MESSAGE)
        else:
            self.barre_erreur.afficher_erreur(self._fenetre, MESSAGE_DEFAITE, COULEUR_MESSAGE)


    def attente_evenement(self):
        """ Méthode permettant d'afficher la solution et d'attendre un événement.
            Elle lance le fonctionnement associé à l'événement intercepté.
            Le joueur peut retourner au menu ou quitter le jeu, depuis cette écran. 
            La grille résolu ainsi qu'un message lui est affiché tant qu'il ne déclenche aucune de ces actions.
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
                    if self.bouton_menu.clicked(curseur):
                        return
        
        
        
