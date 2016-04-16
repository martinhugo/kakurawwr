#!/usr/bin/python3
# -*- encoding:utf-8 -*


"""Module contenant les classes de Cases 

   Contient les classes suivante:
      - CaseVide
      - Indicatrice
      - CaseNoire

    Ce module sera utilisé pour le jeu d'une grille et son édition.

    Modules importés:
        pygame: utilisé lors du jeu ou de l'édition d'une grille.
        constantes: utilisé par toutes les méthodes
        Widget de boutons: classe mère de chacune des classes de ce module

"""

import pygame
import pygame.freetype
from pygame.locals import *
from boutons import Widget
from constantes import *


class CaseVide(Widget):
    """ Classe modélisant une case vide, dans laquelle le joueur saisit une valeur.
        Cet classe contient 5 attributs:
          - valeur_saisie: valeur saisie par le joueur
          - solution_case: solution de la case contenue par le programme
          - rect: la surface cliquable de la classe
          - domaine: le domaine de valeurs que peut prendre la case lors du calcul de sa solvabilité
          - erreur: booleen decrivant si le contenu de la case est erronné
    """

    def __init__(self, data):
        """ Initialise chacun des attributs:
                - _solution_case = valeur
                - valeur_saisie = -1 sera ultérieurement initialisé au cours du jeu
                - rect = (0,0), sera modifié lors de l'affichage de la grille
                - domaine = un set (ensemble) contenant toutes les valeurs entre 1 et 9.
        """
        Widget.__init__(self)
        
        if type(data) is int:
            self._solution_case = data
            self.valeur_saisie =  -1
            self.erreur = False
            self.domaine = set(range(1,10))
            self.degre = 0

        elif type(data) is CaseVide:
            self._solution_case = data._solution_case
            self.valeur_saisie =  data.valeur_saisie
            self.erreur = data.erreur
            self.domaine = set(data.domaine)
            self.degre = data.degre

        
    def __eq__(self, element): 
        """ Méthode permettant de tester l'égalité entre deux cases vides """

        if type(element) is CaseVide:
            return (self._solution_case == element._solution_case and self.valeur_saisie == element.valeur_saisie and self.domaine==element.domaine)
        else:
            return False

    def __ne__(self, element):
        return not self.__eq__(element)
            
    def saisie_valeur(self, font_saisie, fenetre):
        """ Cette méthode propose une zone de saisie dans la case, à l'aide de font_saisie.
            La saisie initialise valeur_saisie.
            L'utilisateur peut entrer des valeurs numériques entre 1 et 9.
            Un clic, ou la pression de la touche entrée permettent de quitter la fonction.
            La pression de la touche backspace permet d'effacer la saisie.
        """
        # Montre a l'utilisateur qu'il a cliqué une case
        fenetre.fill(COULEUR_FOND_CASE, self.rect) 
        pygame.display.flip()

        while True:
            for event in pygame.event.get():

                # Sortie du jeu
                if event.type == QUIT:
                    pygame.quit()

                # Sortie de la saisie
                elif event.type == MOUSEBUTTONUP:
                    return

                # Saisie et validation
                elif event.type == KEYDOWN:
                    if event.unicode.isnumeric() and event.unicode != "0":
                        self.valeur_saisie = int(event.unicode)
                    elif event.key == K_BACKSPACE:
                        self.valeur_saisie = -1
                    elif event.key == K_RETURN:
                        return

                fenetre.fill(COULEUR_FOND_CASE, self.rect)
                # Affichage de la valeur dans la case
                if self.valeur_saisie != -1:
                    valeur = font_saisie.render(str(self.valeur_saisie), COULEUR_POLICE)[0]
                    fenetre.blit(valeur, self.rect.move(DECALAGE_SAISIE_CASE_VIDE))
                pygame.display.flip()

    def affichage(self, fenetre, font_casevide, position, img_case_vide):
        """ Méthode permettant l'affichage d'une case vide et de sa valeur.
            Affiche l'image img_case_vide à la position passée en arguments dans la fenetre elle aussi passée en arguments.
            Si une valeur a été saisie, cette valeur est affichée a l'aide de font_casevide.
            L'affichage met à jour l'attribut rect de la case vide.
        """
        fenetre.blit(img_case_vide, position)
        self.rect = pygame.Rect(position, (COTE_IMAGE_CASE, COTE_IMAGE_CASE))
        if self.erreur:
            couleur = COULEUR_ERREUR
            #if self.valeur_saisie == -1:
            #    self.valeur_saisie = "/"
        else:
            couleur = COULEUR_POLICE
        if self.valeur_saisie != -1:
            valeur = font_casevide.render(str(self.valeur_saisie), couleur)[0]
            fenetre.blit(valeur, self.rect.move(DECALAGE_SAISIE_CASE_VIDE))
            #if self.valeur_saisie == "/":
            #    self.valeur_saisie = -1
                    

    def __str__(self):
        """Chaine retournée lors d'un print ou d'une conversion en str de la classe"""
        return str(self.valeur_saisie)







class CaseNoire(Widget):
    """ Classe modélisant une case noire, qui masque les cases n'appartenant n'appartenant pas au jeu de la grille.
        Cette classe possède un attribut hérité de Widget, le rect de l'image, correspondant a sa surface cliquable.
    """

    def __init__(self):
        """ Initialise les attributs de la classe Widget """
        Widget.__init__(self)

    def __str__(self):
        """Chaine retournée lors d'un print ou d'une conversion en str de la classe"""
        return 'Noire'

    def __eq__(self, element):
        """ Méthode permettant de tester l'égalité entre deux cases noires"""
        return type(element) == CaseNoire

    def __ne__(self, element):
        return not self.__eq__(element)










class Indicatrice(Widget):
    """ Classe modélisant une case indicatrice, qui indique au joueur les valeurs des blocs rattachés.
        Cette classe contient 3 attributs:
           - valeur_bas: la somme des valeurs de la plage bas
           - valeur_droite: la somme des valeurs de la plage droite
           - rect: la surface cliquable de la case.
           - rect_bas: la surface cliquable de l'indication de la plage bas
           - rect_droite: la surface cliquable de l'indication de la plage droite
           - erreur_bas: booléen déterminant si la plage bas contient une erreur 
           - erreur_droite: booléen détérminant si la plage droite contient une erreur
    """

    def __init__(self, case=None):
        """ Les attribus valeur_bas, valeur_droite sont initialisées a 0.
            Les attributs rect, rect_bas, rect_droite sont initialisés à 0,0.
            Les attributs erreur_bas et erreur_droite sont initialisés a False.
            Ces valeurs seront modifiées ultérieurement, lors de la génération, de la saisie, et de l'affichage de la grille.
        """
        Widget.__init__(self)
        if case != None:
            self.valeur_bas = case.valeur_bas
            self.valeur_droite = case.valeur_droite
            self.rect_bas = case.rect_bas
            self.rect_droite = case.rect_droite
            self.erreur_droite = case.erreur_droite
            self.erreur_bas = case.erreur_bas
            self.domaine_bas = [list(el) for el in case.domaine_bas]
            self.domaine_droite = [list(el) for el in case.domaine_droite]

        else:
            self.valeur_bas = 0
            self.valeur_droite = 0
            self.rect_bas = 0,0
            self.rect_droite = 0,0
            self.erreur_droite = False
            self.erreur_bas = False
            self.domaine_bas = []
            self.domaine_droite = []

    def __str__(self):
        """Chaine retournée lors d'une conversion en str ou d'un print"""
        return (str(self.valeur_bas) + "\\" + str(self.valeur_droite))

    def __eq__(self, element):
        """ Méthode permettant de tester l'égalité entre deux indicatrices """
        if type(element) is Indicatrice:
            return (self.valeur_bas == element.valeur_bas) and (self.valeur_droite == element.valeur_droite)
        else:
            return False

    def __ne__(self, element):
        return not self.__eq__(element)

 
    def affichage(self, fenetre, font_indicatrice, position, img_indicatrice):
        """ Affiche l'img_case_vide à la position passée en arguments dans la fenetre passée en arguments.
            Les valeurs de l'indicatrice sont affichées grâce a font_indicatrice.
            La position d'affichage de ces valeurs est calculée en se décalant du coin haut gauche de la case.
            Le décalage se fait selon les constantes DECALAGE_INDICATRICE_VALDROITE et DECALAGE_INDICATRICE_VALBAS.
            L'affichage met à jour l'attribut rect de la case.
        """

        fenetre.blit(img_indicatrice, position)
        self.rect = pygame.Rect(position, (COTE_IMAGE_CASE, COTE_IMAGE_CASE))

        # Positionnement des valeurs des indicatrices
        if self.erreur_droite:
            couleur = COULEUR_ERREUR
        else:
            couleur = COULEUR_POLICE

        # Position de la valeur droite
        valeur_droite = font_indicatrice.render(str(self.valeur_droite),  couleur)[0]
        self.rect_droite = self.get_rect_valeur(DECALAGE_INDICATRICE_VALDROITE)
        fenetre.blit(valeur_droite, self.rect_droite)

        if self.erreur_bas:
            couleur = COULEUR_ERREUR
        else:
            couleur = COULEUR_POLICE

        #Position de la valeur bas
        valeur_bas = font_indicatrice.render(str(self.valeur_bas), couleur)[0]
        self.rect_bas = self.get_rect_valeur(DECALAGE_INDICATRICE_VALBAS)
        fenetre.blit(valeur_bas, self.rect_bas)

        
    def get_rect_valeur(self, decalage):
        """ Permet de calculer la position des rect de saisie en fonction du décalage passée en argument. """
        rect = self.rect.move(decalage)
        pos_x, pos_y = rect.left, rect.top
        return pygame.Rect((pos_x, pos_y), DIMENSION_SAISIE_INDICATRICE)


    def clicked_bas(self, curseur):
        """ Verifie si la zone de saisie bas a été cliquée. 
            Prend curseur, un argument de type rect et verifie si son attribut rect le contient.
            Appelé sur un événement MOUSEBUTTONUP.
        """
        return self.rect_bas.contains(curseur)

    def clicked_droite(self, curseur):
        """ Verifie si la zone de saisie droite a été cliquée. 
            Prend curseur, un argument de type rect et verifie si son attribut rect le contient.
            Appelé sur un événement MOUSEBUTTONUP.
        """
        return self.rect_droite.contains(curseur)



    def saisie(self, fenetre, font_saisie, position):
        """ Fonction permettant de saisir, au clavier, la valeur droite de l'indicatrice.
            Le paramètre position permet de parametre a quel endroit sera saisie la valeur. 
            Ce paramètre peut avoir les valeurs "bas" et "droite".
            La valeur sera affichée sur la fenetre, grâce au font_saisie.
            Le rect ou sera affichée la valeur est détérminé en fonction du paramètre position.
        """
        if position == SAISIE_BAS:
            rect = self.rect_bas

        else: 
            rect = self.rect_droite

        valeur = ""
        continuer = True
        while continuer:
            for event in pygame.event.get():

                if event.type == QUIT:
                    pygame.quit()
                elif event.type == MOUSEBUTTONUP:
                    continuer = False

                elif event.type == KEYDOWN:

                    if event.unicode.isnumeric() and len(valeur) < 2:
                        valeur += event.unicode
                    elif event.key == K_BACKSPACE:
                        valeur = valeur[:-1]
                    elif event.key == K_RETURN:
                        continuer = False

                fenetre.fill(COULEUR_FOND_CASE, rect)
                affichage_val = font_saisie.render(valeur, COULEUR_SAISIE_INDICATRICE)[0]
                fenetre.blit(affichage_val, rect)
                pygame.display.flip()

        if valeur != "":
            return int(valeur)
        else:
            return -1

