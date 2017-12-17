#!/usr/bin/python3
# -*- encoding:utf-8 -*


""" Module effectuant les tests unitaire du module boutons.
    Ce module est constitué de 3 classes:
        - WidgetTest: effectue les tests unitaires de la classe Widget.
        - BoutonTest: effectue les tests unitaires de la classe Bouton.
        - OptionEditeurTest: effectue les tests unitaires de la classe OptionEditeur


    Les modules suivants sont utilisés dans ce module:
        - unittest: utilisé pour réaliser les tests unitaires de chaque méthode.
        - pygame: utilisé pour les tests graphiques.
        - boutons: utilisé pour tester les méthodes de ces différentes classes.
        - constantes: utilisé pour avoir acces aux constantes des tests unitaires
"""

import unittest
import pygame
import pygame.freetype
from pygame.locals import *
import boutons
from constantes import *


class WidgetTest(unittest.TestCase):
    """ Classe permettant de tester le fonctionnement des méthodes de la classe Widget. """

    def setUp(self):
        """ Méthode appelée avant chaque test, permettant d'initialiser le test.
            Cette méthode ajoute un widget comme attribut à la classe, dans le but de tester le fonctionnement des méthodes sur ses attributs.
        """
        self.widget = boutons.Widget()

    def test_clicked(self):
        """ Méthode permettant de tester le comportement de la méthode clicked.
            Cette méthode initialise l'attribut rect du widget.
            Deux autres rect sont testés.
            Un étant inclus dans ce Rect, la méthode clicked doit retourner True.
            Une n'étant pas inclus dans ce Rect, la méthode clicked doit retourner False.
        """

        self.widget.rect = pygame.Rect(10, 10, 10, 10)
        rect_in = (10, 10, 5, 5)
        rect_out = (20, 20, 5, 5)

        self.assertTrue(self.widget.clicked(rect_in))
        self.assertFalse(self.widget.clicked(rect_out))


class BoutonTest(unittest.TestCase):
    """ Classe permettant de tester le fonctionnement des méthodes de la classe Bouton"""

    def setUp(self):
        """ Méthode appelée avant chaque test, permettant d'initialiser le test.
            Cette méthode ajoute un bouton comme attribut à la classe, dans le but de tester le fonctionnement des méthodes sur ses attributs.
        """
        self.bouton = boutons.Bouton("Test")

    def test_afficher(self):
        """ Méthode permettant de tester le comportement de la méthode afficher.
            Cette méthode verifie que les rect du boutons sont bien modifiés en fonction de la position d'affichage.
        """

        self.assertTrue(self.bouton.rect == (0, 0))
        self.assertTrue(self.bouton.rect_texte == (0, 0))

        # Lancement de la méthode
        fenetre = pygame.display.set_mode(TAILLE_FENETRE_TEST)
        img_test = pygame.image.load(CHEMIN_IMAGE_BOUTON).convert()
        font_texte = pygame.freetype.Font(CHEMIN_FICHIER_POLICE, TAILLE_POLICE_BOUTON)
        self.bouton.afficher(fenetre, img_test, font_texte, POSITION_IMAGE_TEST)

        self.assertEqual(type(self.bouton.rect), pygame.Rect)
        self.assertEqual(type(self.bouton.rect_texte), pygame.Rect)
        self.assertEqual((self.bouton.rect.top, self.bouton.rect.left), POSITION_IMAGE_TEST)


class OptionEditeurTest(unittest.TestCase):
    """ Classe permettant de tester le fonctionnement des méthodes de la classe OptionEditeur """

    def setUp(self):
        """ Méthode appelée avant chaque test. Ajoute un attribut option_editeur, de type OptionEditeur, permettant de tester le fonctionnement de ses méthodes."""
        self.option_editeur = boutons.OptionEditeur()

    def test_afficher(self):
        """ Méthode permettant de tester le comportement de la méthode afficher.
            Cette méthode verifie que les rect de l'option_editeur sont bien modifiés en fonction de la position d'affichage et du fait que l'option soit selectionnée ou non.
            Si l'option n'est pas selectionné, l'affichage est fait a la position passée en argument.
            Sinon, la nouvelle position doit être calculée, converti en entier et comparé à la position du rect.
        """
        ## NON SELECTIONNEE ##
        # Verification du rect avant le lancement de la méthode
        self.assertEqual(self.option_editeur.rect, (0, 0))

        # Lancement de la méthode
        fenetre = pygame.display.set_mode(TAILLE_FENETRE_TEST)
        img_test = pygame.image.load(CHEMIN_IMAGE_BOUTON).convert()
        self.option_editeur.afficher(fenetre, img_test, POSITION_IMAGE_TEST)

        # Verification du reect suite au lancement de la méthode
        self.assertEqual(type(self.option_editeur.rect), pygame.Rect)
        self.assertEqual((self.option_editeur.rect.top, self.option_editeur.rect.left), POSITION_IMAGE_TEST)

        ## SELECTIONNEE ##
        # Selection de l'option
        self.option_editeur.is_enlarged = True
        self.option_editeur.skew = 2

        # Calcul de la position de l'image en fonction du décalage et du recentrage
        (pos_x, pos_y) = POSITION_IMAGE_TEST
        decalage = ((COTE_IMAGE_CASE_ENLARGED - COTE_IMAGE_CASE) / 2) + 5
        position = (int(pos_x - decalage), int(pos_y - decalage))

        # Lancement de la méthode
        fenetre = pygame.display.set_mode(TAILLE_FENETRE_TEST)
        img_test = pygame.image.load(CHEMIN_IMAGE_BOUTON).convert()
        self.option_editeur.afficher(fenetre, img_test, POSITION_IMAGE_TEST)

        # Verification du reect suite au lancement de la méthode
        self.assertEqual(type(self.option_editeur.rect), pygame.Rect)
        self.assertEqual((self.option_editeur.rect.top, self.option_editeur.rect.left), position)


if __name__ == "__main__":
    print("Test du module bouton")
    pygame.init()
    pygame.freetype.init()
    unittest.main()
    pygame.quit()
