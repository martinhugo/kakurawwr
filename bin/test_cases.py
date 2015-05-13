#!/usr/bin/python3
# -*- encoding:utf-8 -*

""" Module effectuant les tests unitaire du module cases.
    Ce module est constitué de deux classes:
        - CaseTest, effectuant les tests unitaires des méthodes communes des classes CaseVide, CaseNoire et Indicatrice.
        - IndicatriceTest: effectuant les tests unitaires des méthodes spécifiques de la classe Indicatrice.

    Les modules suivants sont utilisés dans ce module:
        - unittest: utilisé pour réaliser les tests unitaires de chaque méthode.
        - pygame: utilisé pour les tests graphiques.
        - cases: utilisé pour tester les méthodes de ces différentes classes.
        - constantes: utilisé pour avoir acces aux constantes des tests unitaires
"""

import unittest
import pygame
import pygame.freetype
from pygame.locals import *
import cases
from constantes import *


class CaseTest(unittest.TestCase):
    """ Classe permettant de tester le fonctionnement des méthodes partagées par chacune des classes du  module cases"""

    def setUp(self):
        """ Méthode appellée avant chaque test, permettant d'initialiser le test.
            Cette méthode ajoute trois attributs:
                -case_vide: un objet de type CaseVide permettant de tester les méthodes de la classe CaseVide
                -indicatrice: un objet de type Indicatrice permettant de tester les méthodes de la classe Indicatrice
                -case_noire: un objet de type CaseNoire permettant de tester les méthodes de la classe CaseNoire
        """
        self.case_vide = cases.CaseVide(2)
        self.indicatrice = cases.Indicatrice()
        self.case_noire = cases.CaseNoire()

       
    def test_clicked(self):
        """ Méthode permettant de tester le comportement de la méthode clicked.
            Cette méthode initialise l'attribut rect de chacun des attributs.
            Deux autres rect sont créés.
            Pour chaque attribut le même test est effectué.
            Un étant inclus dans ce Rect, la méthode clicked doit retourner True.
            Une n'étant pas inclus dans ce Rect, la méthode clicked doit retourner False.
        """

        self.case_vide.rect = pygame.Rect(10,10,10,10)
        self.indicatrice.rect = pygame.Rect(10,10,10,10)
        self.case_noire.rect = pygame.Rect(10,10,10,10)

        rect_in = (10,10,5,5)
        rect_out = (20,20,5,5)

        self.assertTrue(self.case_vide.clicked(rect_in))
        self.assertFalse(self.case_vide.clicked(rect_out))
        self.assertTrue(self.indicatrice.clicked(rect_in))
        self.assertFalse(self.indicatrice.clicked(rect_out))
        self.assertTrue(self.case_noire.clicked(rect_in))
        self.assertFalse(self.case_noire.clicked(rect_out))


class IndicatriceTest(unittest.TestCase):
    """ Classe permettant de tester le fonctionnement des méthodes spécifiques de la classe Indicatrice """

    def setUp(self):
        """ Méthode appellée avant chaque test, permettant de l'initialiser.
            Cette méthode ajoute un attribut indicatrice, de type Indicatrice, permettant de tester les méthodes de cette classe.
        """
        self.indicatrice = cases.Indicatrice()

    def test_get_rect_valeur(self):
        """ Méthode permettant de tester le comportement de get_rect_valeur().
            Cette méthode initialise le rect et lance get_rect_valeur avec en paramètre un décalage.
            Elle verifie ensuite que le rect renvoyé par la méthode est cohérent.
        """
        self.indicatrice.rect = pygame.Rect(10,10,10,10)
        rect = self.indicatrice.get_rect_valeur((5, 5))
        self.assertTrue(rect.top == 15 and rect.left == 15)
        self.assertEqual((rect.width,rect.height), DIMENSION_SAISIE_INDICATRICE)

    def test_clicked_saisie(self):
        """ Méthode permettant de tester le comportement des méthodes clicked_droite et clicked_bas.
            Cette méthode initialise les différents rect de la case indicatrice.
            Elle créé deux rect devant se trouver respectivement et uniquement dans le rect_droite et le rect_bas.
            Elle verifie que le rect_right se trouve bien dans le rect_droite de l'indicatrice, et uniquement dans ce rect.
            Elle verifie que le rect_bottom se trouve bien dans le rect_bas de l'indicatrice, et uniquement dans ce rect.
        """
        self.indicatrice.rect = pygame.Rect(10,10,10,10)

        rect_right = (13,10, 0, 0)
        rect_bottom = (10,13, 0, 0)

        self.indicatrice.rect_bas = self.indicatrice.get_rect_valeur((0,2))
        self.indicatrice.rect_droite = self.indicatrice.get_rect_valeur((2,0))

        self.assertTrue(self.indicatrice.clicked_droite(rect_right))
        self.assertFalse(self.indicatrice.clicked_droite(rect_bottom))
        self.assertTrue(self.indicatrice.clicked_bas(rect_bottom))
        self.assertFalse(self.indicatrice.clicked_bas(rect_right))

if __name__ == "__main__":
    print("Test du module cases")
    unittest.main()