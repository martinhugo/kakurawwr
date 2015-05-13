#!/usr/bin/python3
# -*- encoding: utf-8 -*

""" Module de generation de grille du produit.
    Ce module est l'implémentation de l'ecran de choix de difficulté.
    Ce module possède une unique classe Generation.

    Celle ci possède deux méthodes:
        - afficher(): affiche l'écran de choix de difficulté
        - choisir_difficulte(): boucle événementielle détectant la difficulté choisie par le joueur

    Modules importés:
        - pygame: utilisé pour l'affichage
        - boutons: utilisé pour manier les boutons de l'écran
        - grille, jeu: permettent le déclenchement d'une partie de Kakuro
        - constantes: utilisé par toutes les méthodes
"""

import pygame
from pygame.locals import *
import pygame.freetype
import boutons
import grille
import jeu
from constantes import *

class Generation:
    """ Classe Generation, modélise l'écran de choix de difficulté et génère la grille.
        Cette classe possède 4 attributs:
            - _fenetre: la fenetre d'affichage de l'écran
            - bouton_facile: bouton permettant de generer une grille de difficulté facile
            - bouton_moyen: bouton permettant de generer une grille de difficulté moyenne
            - bouton_difficile: bouton permettant de générer une grille de difficulté difficile
            - bouton_mdft: bouton permettant de générer une grille de difficulté maitre des flans ténébreux
    """

    def __init__(self, fenetre):
        """ Initialise les attributs de la classe.
            La fenetre d'affichage est passée en paramètre.
            Les autres éléments sont des boutons, qui seront complétés dans l'affichage.
        """

        self._fenetre = fenetre
        self.bouton_retour = boutons.Bouton(TITRE_BOUTON_MENU)        
        self.bouton_facile = boutons.Bouton(TITRE_BOUTON_FACILE)
        self.bouton_moyen = boutons.Bouton(TITRE_BOUTON_MOYEN)
        self.bouton_difficile = boutons.Bouton(TITRE_BOUTON_DIFFICILE)
        self.bouton_mdft = boutons.Bouton(TITRE_BOUTON_MDFT)



    def afficher(self):
        """ Méthode permettant d'afficher le menu à l'écran.
            Chacun des boutons du menu est affiché.
            La grille est affichée par la suite.
        """
        self._fenetre.fill(COULEUR_FOND)
        titre_bouton = pygame.freetype.Font(CHEMIN_FICHIER_POLICE, TAILLE_POLICE_BOUTON)
        bouton_img = pygame.image.load(CHEMIN_IMAGE_BOUTON).convert_alpha()
        self.bouton_retour.afficher(self._fenetre, bouton_img, titre_bouton, POSITION_BOUTON_RETOUR)                                        
        self.bouton_facile.afficher(self._fenetre, bouton_img, titre_bouton, POSITION_BOUTON_FACILE)
        self.bouton_moyen.afficher(self._fenetre, bouton_img, titre_bouton, POSITION_BOUTON_MOYEN)
        self.bouton_difficile.afficher(self._fenetre, bouton_img, titre_bouton, POSITION_BOUTON_DIFFICILE)
        self.bouton_mdft.afficher(self._fenetre, bouton_img, titre_bouton, POSITION_BOUTON_MDFT)


    def choisir_difficulte(self):
        """ Méthode permettant au joueur de choisir sa difficulté par l'intermédiaire d'une boucle événementielle.
            Lors d'un clic sur un niveau de difficulté, une grille du niveau de difficulté corespondant est proposée au joueur.
        """
        # Boucle infinie
        while True:
            
            self._fenetre.fill(COULEUR_FOND)
            self.afficher()
            pygame.display.flip()

            ecran_jeu = jeu.Jeu(self._fenetre, grille.Grille())
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    
                # Traitement des clics boutons
                elif event.type == MOUSEBUTTONUP and event.button == 1:
                    
                    curseur = pygame.Rect(event.pos, (0,0))

                    if self.bouton_retour.clicked(curseur):
                        return
                    
                    if self.bouton_facile.clicked(curseur):
                        ecran_jeu.grille.generer_grille("facile")
                        ecran_jeu.jouer()
                        return
                        
                    elif self.bouton_moyen.clicked(curseur):
                        ecran_jeu.grille.generer_grille("moyen")
                        ecran_jeu.jouer()
                        return
                        
                    elif self.bouton_difficile.clicked(curseur):
                        ecran_jeu.grille.generer_grille("difficile")
                        ecran_jeu.jouer()
                        return
                        
                    elif self.bouton_mdft.clicked(curseur):
                        ecran_jeu.grille.generer_grille("mdft")
                        ecran_jeu.jouer()
                        return



    
        
        
        
