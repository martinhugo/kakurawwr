#!/usr/bin/python3
# -*- encoding: utf-8 -*

""" Module de menu du produit.
    Ce module permet l'implémentation de la fonctionnalité Menu.
    Ce module possède une unique classe Menu.

    Modules importés:
        - pygame: utilisé pour l'affichage
        - boutons: utilisé pour manier les boutons de l'écran
        - constantes: utilisé par toutes les méthodes
        - generation: utilisé pour acceder à l'écran de génération
        - sauvegarde: utilisé pour acceder à l'écran de sauvegarde
        - editeur: utilisé pour acceder à l'écran d'éditeur
"""

import pygame
from pygame.locals import *
import pygame.freetype
import boutons
import generation
import editeur
import sauvegarde
from constantes import *


class Menu:
    """ Modèle de donnée utilisé pour modéliser le menu, dans sa représentation graphique aussi bien que dans son fontionnement.
        Cette classe possède 4 attributs:
            - _fenetre: la fenetre d'affichage de l'écran
            - bouton_jouer: bouton permettant d'acceder au jouer
            - bouton_editeur: bouton permettant d'acceder a l'editeur
            - bouton_charger: bouton permettant de charger une grille puis de la jouer
    """

    def __init__(self, fenetre):
        """ Initialise les attributs de la classe.
            La fenetre d'affichage est passée en paramètre.
            Les autres éléments sont des boutons, initialisés avec des titres définis dans les constantes.
        """

        self._fenetre = fenetre

        self.bouton_jouer = boutons.Bouton(TITRE_BOUTON_JOUER)
        self.bouton_charger = boutons.Bouton(TITRE_BOUTON_CHARGER)
        self.bouton_editeur = boutons.Bouton(TITRE_BOUTON_EDITEUR)

    def afficher(self):
        """ Méthode permettant d'afficher le menu à l'écran.
            Chacun des boutons du menu est affiché.
            Par la suite, la grille est affichée.

            La méthode afficher de la classe Bouton est utilisée pour afficher les boutons.
        """

        img_kakurawwr = pygame.image.load(CHEMIN_IMAGE_KAKURAWWR).convert_alpha()
        titre_bouton = pygame.freetype.Font(CHEMIN_FICHIER_POLICE, TAILLE_POLICE_BOUTON)
        bouton_img = pygame.image.load(CHEMIN_IMAGE_BOUTON).convert_alpha()

        self._fenetre.blit(img_kakurawwr, POSITION_IMG_KAKURAWWR)
        self.bouton_jouer.afficher(self._fenetre, bouton_img, titre_bouton, POSITION_BOUTON_JOUER)
        self.bouton_charger.afficher(self._fenetre, bouton_img, titre_bouton, POSITION_BOUTON_CHARGER)
        self.bouton_editeur.afficher(self._fenetre, bouton_img, titre_bouton, POSITION_BOUTON_EDITEUR)

    def wait_evenement(self):
        """ Méthode d'attente d'évenements de la classe.
            Cette méthode affiche l'écran et met à jour la fênetre.
            Un evenement est ensuite récupéré, et est traité en conséquence.
            En cliquant sur les boutons correspondants, on peut acceder aux ecrans de:
                - chargement
                - génération
                - édition
        """
        # Boucle infinie - Attente d'évenement
        while True:
            self._fenetre.fill(COULEUR_FOND)
            self.afficher()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                # Traitement des clics boutons
                elif event.type == MOUSEBUTTONUP:

                    curseur = pygame.Rect(event.pos, (0, 0))

                    if self.bouton_jouer.clicked(curseur):
                        ecran_difficulte = generation.Generation(self._fenetre)
                        ecran_difficulte.choisir_difficulte()

                    elif self.bouton_charger.clicked(curseur):
                        ecran_chargement = sauvegarde.Chargement(self._fenetre)
                        ecran_chargement.chargement()

                    elif self.bouton_editeur.clicked(curseur):
                        ecran_editeur = editeur.Editeur(self._fenetre)
                        ecran_editeur.edition()
