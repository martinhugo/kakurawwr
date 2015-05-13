#!/usr/bin/python3
# -*- encoding:utf-8 -*


""" Module contenant les classes Widget, Bouton et BarreErreur
    Ce module est utilisé pour implémenter l'ensemble des écrans d'affichage.

    Modules importés:
       - constantes: utilisé dans chaque méthode
       - pygame: utilisé pour l'affichage du bouton, de son titre est des erreurs

    La classe Bouton est utilisée pour afficher un bouton cliquable sur un écran d'affichage.
    La classe BarreErreur sera utilisé dans les écrans d'éditions et de jeu pour implémenter les entraves aux règles et les erreurs de saisie.
"""

from constantes import *
import pygame
from pygame.locals import *


class Widget:
    """ Classe modélisant un objet cliquable. Cette classe servira de classe mère pour tout les objets cliquables du jeu """

    def __init__(self):
        """ Le constructeur initialise le rect du widget à 0,0
        """
        self.rect = 0,0

    def clicked(self, curseur):
        """ Verifie si le widget a été cliqué.
            Prend curseur, un argument de type rect et verifie si son attribut rect le contient.
            Est typiquement appelé sur un événement MOUSEBUTTONUP
        """
        return self.rect.contains(curseur)




class Bouton(Widget):
    """ Classe modélisant le comportement d'un bouton. Cette classe est utilisée pour tous les écrans d'affichage.
        Elle possède deux attributs:
            - le rect principal, sa surface cliquable
            - le rect de texte, ou est affiché le texte de l'image
    """

    def __init__(self, texte):
        """ Le constructeur initialise chacun de ses rect a 0,0. 
            Il donne à l'attribut texte la valeur du texte passée en paramètre.
        """
        Widget.__init__(self)
        self.rect_texte = 0,0
        self.titre = texte

    def afficher(self, fenetre, image, font_titre, position):
        """ Affichage de l'image sur la fenetre passée en paramètre à la position spécifiée """
        fenetre.blit(image, position)
        self.rect =  pygame.Rect(position, (image.get_rect().width, image.get_rect().height))
        texte = font_titre.render(self.titre, COULEUR_POLICE)[0]
        
        if len(self.titre) > TAILLE_TITRE_COURT:
            self.rect_texte = self.rect.move(DECALAGE_TITRE_BOUTON_LONG)
        else:
            self.rect_texte = self.rect.move(DECALAGE_TITRE_BOUTON_COURT)
        fenetre.blit(texte, self.rect_texte)

        




    
        
class BarreErreur:
    """ Classe modélisant une barre de texte, utilisée pour l'affichage d'erreurs.
        Cette barre d'erreur comprend un objet de type Font, permettant d'écrire les erreurs à l'ecran.
    """

    def __init__(self, font_erreur):
        """ Initialise la zone d'affichage de la barre d'erreur avec le paramètre position.
            Prend en paramètre un objet de classe Font permettant d'écrire les erreurs.
        """
        self.font_erreur = font_erreur
        
    def afficher_erreur(self, fenetre, texte, couleur):
        """ Affiche une erreur dans la fenetre à la zone prévue par self.position, dans la couleur passée en argument. 
            Les erreurs sont affichées selon leur longueur en partant de ERREUR_POSITION_DEPART.
            On soustrait à cette valeur la longueur de l'erreur multiplié par FACTEUR_DECALAGE_ERREUR.
            L'erreur est alors correctement positionnée.
        """
        erreur = self.font_erreur.render(texte, couleur, style = pygame.freetype.STYLE_STRONG)[0]
        position_x = ERREUR_POSITION_DEPART - (len(texte) * FACTEUR_DECALAGE_ERREUR)
        fenetre.blit(erreur, (position_x, ERREUR_POSITION_Y))






class OptionEditeur(Widget):
    """ Classe modélisant les options selectionnables dans l'édition.
        Cette classe contient un attribut selected, et un rect.
        Elle hérite de la méthode clicked de Widget.
        Elle a également une méthode d'affichage.
    """

    def __init__(self):
        """ Initialise l'attribut rect à (0,0) et affecte leurs valeurs par défaut aux attributs graphiques"""
        Widget.__init__(self)
        self.is_enlarged = False
        self.skew=0


    def afficher(self, fenetre, image, position):
        """ Affichage de l'image sur la fenetre passée en paramètre à la position spécifiée """
        if self.is_enlarged:
            # on elargit et rote l'image
            image = pygame.transform.rotozoom(image, self.skew, 1.2)
            # on la recentre
            (pos_x, pos_y) = position
            #Ici, le +5 vient du fait que COTE_IMAGE_CASE_ENLARGED est inexact a cause de la rotation de l'image.
            decalage = ((COTE_IMAGE_CASE_ENLARGED-COTE_IMAGE_CASE)/2)+5
            position = (pos_x-decalage, pos_y-decalage)
        
        fenetre.blit(image, position)
        self.rect =  pygame.Rect(position, (image.get_rect().width, image.get_rect().height))




class ZoneSaisie(Widget):
    """ Classe modélisant une zone de saisie permettant de saisir un nom de fichier 
        Cette classe contient un attribut rect et un attribut valeur contenant la chaine saisie.
    """

    def __init__(self):
        """ Initialise l'attribut rect à (0,0) et la valeur à une chaine vide. """
        Widget.__init__(self)
        self.rect_saisie = (0,0)
        self.valeur = ""

    def afficher(self, fenetre, image, font_saisie, position,):
        """ Affiche l'image passée en paramètre à la position précisée.
            Cette méthode met à jour l'attribut rect.
        """
        fenetre.blit(image, position)
        if (self.rect == 0,0):
            self.rect =  pygame.Rect(position, (image.get_rect().width, image.get_rect().height))
            self.rect_saisie = self.init_rect_saisie()
        affichage_val = font_saisie.render(self.valeur, COULEUR_POLICE)[0]
        fenetre.blit(affichage_val, self.rect_saisie)

    def saisie(self, fenetre, font_saisie):
        """ Permet de saisir une chaine de caractères et de la retourner une fois validée"""

        continuer = True
        while continuer:
            for event in pygame.event.get():

                if event.type == QUIT:
                    pygame.quit()
                elif event.type == MOUSEBUTTONUP:
                    continuer = False

                elif event.type == KEYDOWN:

                    if event.unicode.isalnum() and len(self.valeur) < TAILLE_NOM_FICHIER_MAX:
                        self.valeur += event.unicode
                    elif event.key == K_BACKSPACE:
                        self.valeur = self.valeur[:-1]
                    elif event.key == K_RETURN:
                        continuer = False

                fenetre.fill(COULEUR_FOND_CASE, self.rect_saisie)
                affichage_val = font_saisie.render(self.valeur, COULEUR_SAISIE)[0]
                fenetre.blit(affichage_val, self.rect_saisie)
                pygame.display.flip()

        return self.valeur

    def init_rect_saisie(self):
        """ Permet de creer le rect de saisie """
        rect = self.rect.move(DECALAGE_ZONE_SAISIE)
        pos_x, pos_y = rect.left, rect.top
        return pygame.Rect((pos_x, pos_y), DIMENSION_SAISIE_SAUVEGARDE)


