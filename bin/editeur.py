#!/usr/bin/python3
# -*- encoding: utf-8 -*

""" Module d'Editeur du produit.
    Ce module permet l'implémentation de la fonctionnalité Editeur.
    Ce module possède une unique classe Editeur.

    Modules importés:
        - random: utilisé pour des effets graphiques 
        - pygame: utilisé pour l'affichage
        - boutons: utilisé pour manier les boutons de l'écran
        - cases, grille: utilisés pour la grille de l'editeur
        - jeu: pour lancer le jeu directement depuis le menu d'edition
        - solveur: pour verifier que la grille est correcte
        - exceptions: pour la gestion des erreurs
        - constantes: utilisé par toutes les méthodes
"""
import random
import pygame
from pygame.locals import *
import pygame.freetype
import boutons
import cases
import grille
import jeu
import solveur
from exceptions import *
from constantes import *


class Editeur:
    """ Classe Editeur, modélise l'editeur de grilles.
        Cette classe possède 8 attributs:
            - _fenetre: la fenetre d'affichage de l'écran
            - _grille: la grille en cours d'edition
            - bouton_menu: bouton permettant d'acceder au menu
            - bouton_reset: bouton permettant de reinitialiser la grille
            - bouton_verif: bouton permettant de verifier la validité de la grille et de la sauvegarder
            - option_casevide: bouton permettant de placer des cases vides sur la grille
            - option_indicatrice: bouton permettant de placer des indicatrices sur la grille
            - option_casenoire: bouton permettant de placer des cases noires sur la grille
    """

    def __init__(self, fenetre):
        """ Initialise les attributs de la classe.
            La fenetre d'affichage est passée en paramètres.
            La grille sera générée ne contenant que des cases vides.
        """

        self.mode = MODE_SAISIE
        self._fenetre = fenetre
        self._grille = grille.Grille()
        self._grille.generer_grille_vide()

        self.bouton_menu = boutons.Bouton(TITRE_BOUTON_MENU)
        self.bouton_generer = boutons.Bouton(TITRE_BOUTON_GENERER)

        self.bouton_reset = boutons.Bouton(TITRE_BOUTON_RESET)
        self.bouton_verif = boutons.Bouton(TITRE_BOUTON_VERIF)
        self.bouton_jouer = boutons.Bouton(TITRE_BOUTON_JOUER)

        self.option_casevide = boutons.OptionEditeur()
        self.option_indicatrice = boutons.OptionEditeur()
        self.option_casenoire = boutons.OptionEditeur()

        self.barre_erreur = boutons.BarreErreur(pygame.freetype.Font(CHEMIN_FICHIER_POLICE, TAILLE_POLICE_BOUTON))
        self.erreur = ""
        self.changed = False


    def afficher(self):
        """ Affiche l'ecran d'edition.
            La méthode afficher de la classe Bouton est utilisée pour afficher les boutons.
            La méthode afficher_grille de la classe Grille est utilisée pour afficher la grille.
            Les erreurs (ou messages) sont affichés dans la barrer_erreur.
            La couleur de la police d'affichage dépend de la nature de l'erreur (message de confirmation du solveur ou erreur de l'éditeur).
        """

        titre_bouton = pygame.freetype.Font(CHEMIN_FICHIER_POLICE, TAILLE_POLICE_BOUTON)
        bouton_img = pygame.image.load(CHEMIN_IMAGE_BOUTON).convert_alpha()
        vide_img = pygame.image.load(CHEMIN_IMAGE_MODE_CASEVIDE).convert_alpha()
        indic_img = pygame.image.load(CHEMIN_IMAGE_MODE_INDICATRICE).convert_alpha()
        noire_img = pygame.image.load(CHEMIN_IMAGE_MODE_CASENOIRE).convert_alpha()

        self.bouton_menu.afficher(self._fenetre, bouton_img, titre_bouton, POSITION_BOUTON_RETOUR)
        self.bouton_generer.afficher(self._fenetre, bouton_img, titre_bouton, POSITION_BOUTON_GENERER)

        self.bouton_reset.afficher(self._fenetre, bouton_img, titre_bouton, POSITION_BOUTON_RESET)
        self.bouton_verif.afficher(self._fenetre, bouton_img, titre_bouton, POSITION_BOUTON_SAUVEGARDE)
        self.bouton_jouer.afficher(self._fenetre, bouton_img, titre_bouton, POSITION_BOUTON_JOUER_EDITEUR)

        self.option_casevide.afficher(self._fenetre, vide_img, POSITION_MODE_VIDE)
        self.option_indicatrice.afficher(self._fenetre, indic_img, POSITION_MODE_INDIC)
        self.option_casenoire.afficher(self._fenetre, noire_img, POSITION_MODE_NOIRE)

        self._grille.afficher_grille(self._fenetre)

        # Choix de couleur entre erreur/message de fin de solveur
        if self.erreur == MESSAGE_GRILLE_RESOLUE:
            couleur = COULEUR_MESSAGE
        else:
            couleur = COULEUR_ERREUR

        self.barre_erreur.afficher_erreur(self._fenetre, self.erreur , couleur)


    def edition(self):
        """ Méthode permettant de saisir une grille.
            Cette méthode est une boucle infinie attendant un événement. 
            En fonction du mode, l'événement peut être une saisie de valeur ou un remplissage.

            On peut quitter le jeu ou retourner au menu depuis cette méthode.
            Le calcul de la solution peut être demandé, si aucune erreur n'est présente dans la grille.
            On peut aussi acceder au jeu de la grille saisie depuis cette méthode.

        """
        # Boucle infinie
        while True:
            self._fenetre.fill(COULEUR_FOND)
            self.afficher()
            pygame.display.flip()

            try:
                self._grille.validate_saisie()
                self.set_erreur("validation")
            except Exception as e:
                self.erreur = e.message_erreur


            

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()

                ## Clic and drag
                elif (event.type == MOUSEMOTION and event.buttons[0] == 1):
                    self.set_erreur("clic")

                    if self.mode != MODE_SAISIE:
                        curseur = pygame.Rect(event.pos, (0,0))
                        # Remplissage de la grille avec des cases en fonction du mode
                        self.remplir_case(curseur)



                ## Clic 
                elif event.type == MOUSEBUTTONUP and event.button == 1:
                    self.set_erreur("clic")

                    curseur = pygame.Rect(event.pos, (0,0))

                    # Saisie de valeur d'indicatrices
                    if self.mode == MODE_SAISIE:
                        self.saisie_valeur(curseur)
                    else:
                        self.remplir_case(curseur)

                    # Changement de mode
                    if self.option_casevide.clicked(curseur):
                        self.set_mode(MODE_CASEVIDE)
                        self.zoom_on_option(MODE_CASEVIDE)
                    elif self.option_casenoire.clicked(curseur):
                        self.set_mode(MODE_CASENOIRE)
                        self.zoom_on_option(MODE_CASENOIRE)
                    elif self.option_indicatrice.clicked(curseur):
                        self.set_mode(MODE_INDICATRICE)
                        self.zoom_on_option(MODE_INDICATRICE)

                    elif self.bouton_menu.clicked(curseur):
                        return
                        
                    elif self.bouton_reset.clicked(curseur):
                        self._grille.generer_grille_vide()

                    elif self.bouton_generer.clicked(curseur):
                        self._grille = grille.Grille()
                        self._grille.generer_grille("difficile")

                    elif self.bouton_verif.clicked(curseur):
                        if not(self.erreur):
                            try:
                                ecran_solveur = solveur.Solveur(self._fenetre, self._grille)
                                self.erreur = ecran_solveur.loop()
                                self._grille.confirmer_solution()
                                self._grille.solved = True
                            except Exception as e:
                                self._grille.reinitialiser()
                                self.erreur = e.message_erreur

                    elif self.bouton_jouer.clicked(curseur):
                        if not(self.erreur):
                            ecran_jeu = jeu.Jeu(self._fenetre, self._grille)
                            ecran_jeu.jouer()
                            return



    def remplir_case(self, curseur):
        """ Cette méthode verifie si une case a été cliquée.
            Si c'est le cas elle lui affecte une case dont le type dépend du mode d'édition séléctionné.
            Cette méthode est typiquement appelée pour des événements MOUSEMOTION.
        """
        for (i,j) in self._grille.keys():
            if self._grille[i,j].clicked(curseur):
                self._grille[i,j] = self.get_case()
 


    def saisie_valeur(self, curseur):
        """ Cette méthode verifie si une zone de saisie d'une indicatrice a été cliquée.
            Si c'est le cas, une saisie sur cette zone est lancée et la valeur est récupérée dans l'attribut correspondant à la zone.
        """
        for (i,j) in self._grille.keys():
            if type(self._grille[i,j]) is cases.Indicatrice:

                if self._grille[i,j].clicked_droite(curseur):

                    valeur = self._grille[i,j].saisie(self._fenetre, pygame.freetype.Font(CHEMIN_FICHIER_POLICE, TAILLE_POLICE_INDICATRICE), SAISIE_DROITE)
                    if valeur != -1:
                        self._grille[i,j].valeur_droite = valeur

                elif self._grille[i,j].clicked_bas(curseur):

                    valeur =  self._grille[i,j].saisie(self._fenetre, pygame.freetype.Font(CHEMIN_FICHIER_POLICE, TAILLE_POLICE_INDICATRICE), SAISIE_BAS)
                    if valeur != -1: 
                        self._grille[i,j].valeur_bas =  valeur



    def set_mode(self, selected_mode):
        """ Méthode permettant de modifier le mode d'édition en fonction du mode envoyé en paramètres.
            Si le mode envoyé en paramètres est identique au mode d'édition actuel, l'édition passe en mode saisie.
        """
        if selected_mode == self.mode:
            self.mode = MODE_SAISIE
        else:
            self.mode = selected_mode

    def get_case(self):
        """ Méthode retournant une case correspondant au mode actuel. """
        if self.mode == MODE_CASEVIDE:
            return cases.CaseVide(-1)
        elif self.mode == MODE_INDICATRICE:
            return cases.Indicatrice()
        elif self.mode == MODE_CASENOIRE:
            return cases.CaseNoire()


    def zoom_on_option(self, selected_mode):
        """ Méthode permettant de marquer le bouton de mode à elargir. """
        if selected_mode == MODE_CASEVIDE:
            # elargissement de l'image
            self.option_casevide.is_enlarged = not self.option_casevide.is_enlarged
            # rotation
            self.option_casevide.skew = self.randomize_skew()
            # reset des autres
            self.option_indicatrice.is_enlarged = False
            self.option_casenoire.is_enlarged = False

        elif selected_mode == MODE_INDICATRICE:

            self.option_indicatrice.is_enlarged = not self.option_indicatrice.is_enlarged
            self.option_indicatrice.skew = self.randomize_skew()
            self.option_casevide.is_enlarged = False
            self.option_casenoire.is_enlarged = False

        elif selected_mode == MODE_CASENOIRE:

            self.option_casenoire.is_enlarged = not self.option_casenoire.is_enlarged
            self.option_casenoire.skew = self.randomize_skew()  
            self.option_casevide.is_enlarged = False
            self.option_indicatrice.is_enlarged = False

    def set_erreur(self, moment):
        """ Méthode permettant de supprimer l'erreur en cours en fonction du moment d'appel et de la valeur de l'erreur """
        if moment == "validation":
            if self.erreur not in (MESSAGE_ERREUR_NOSOLUTION,MESSAGE_ERREUR_ABANDON, MESSAGE_GRILLE_RESOLUE):
                self.erreur = ""
        else:
            if self.erreur in (MESSAGE_ERREUR_NOSOLUTION, MESSAGE_ERREUR_ABANDON, MESSAGE_GRILLE_RESOLUE):
                self.erreur = ""

    @staticmethod
    def randomize_skew():
        """ Méthode retournant une valeur de rotation aléatoire non nulle comprise entre -5 et 5 degrés"""
        skew = 0
        while skew == 0:
            skew = random.randint(-5, 5)
        return skew