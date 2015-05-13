#!/usr/bin/python3
# -*- encoding:utf-8 -*


""" Module effectuant les tests unitaire du module editeur

    Ce module est composé d'une unique classe EditeurTest, dont les méthodes effectuent les tests unitaires des méthodes d'editeur correspondantes.

    Module utilisé:
        - pygame: tests unitaires des méthodes de jeu
        - unittest: utilisé pour effectuer les tests unitaires
        - grille: utilisé pour tester ses méthodes
        - exceptions: utilisé pour les méthodes de validation
        - constantes: utilisé dans chaque méthode
        - editeur: utilisé pour tester ses méthodes
        - cases: utilisé pour tester les types de la grille
"""

import pygame
import pygame.freetype
from pygame.locals import *
import unittest
import grille
import cases
import editeur
from constantes import *

class EditeurTest(unittest.TestCase):
    """Classe permettant de tester les fonctionnement des méthodes de la classe Editeur"""

    def setUp(self):
        """ Méthode appellée avant chaque test, permettant d'initialiser le test.
            Une objet editeur, de type Editeur est ajouté.
        """
        self.editeur = editeur.Editeur((0,0))
        
    

    def test_set_mode(self, mode=MODE_CASEVIDE):
        """ Méthode permettant de tester le comportement de set_mode. 
            La méthode set_mode est appelée en passant un mode en paramètre. On verifie que le mode a bien été changé.
            On rappelle cette méthode  avec ce même mode en paramètre, on verifie ensuite que ce mode a bien été annulé.
        """
        self.editeur.set_mode(mode)
        self.assertEqual(self.editeur.mode, mode)
        self.editeur.set_mode(mode)
        self.assertEqual(self.editeur.mode, MODE_SAISIE)

    def test_get_case(self):
        """ Méthode permettant de tester le comportement de get_case.
            Successivement, le mode sera changé dans chaque mode possible et la méthode get_mode sera appellée.
            On verifiera que l'objet renvoyé par la valeur est bien du type attendu.
        """
        self.editeur.set_mode(MODE_CASEVIDE)
        self.assertEqual(type(self.editeur.get_case()), cases.CaseVide)
        self.editeur.set_mode(MODE_CASENOIRE)
        self.assertEqual(type(self.editeur.get_case()), cases.CaseNoire)
        self.editeur.set_mode(MODE_INDICATRICE)
        self.assertEqual(type(self.editeur.get_case()), cases.Indicatrice)

    def test_zoom_on_option(self, mode=MODE_CASENOIRE):
        """ Méthode permettant de tester le comportement de zoom_on_option.
            La méthode zoom_on_option sera appelée sur un mode choisi. 
            On verifiera que le bouton a été marqué comme à zoomer, et que les autres boutons de mode ne l'ont pas été.
            On reappelle la méthode sur ce même mode est on verifie que le bouton n'est plus marqué comme à zoomer.
        """
        self.editeur.zoom_on_option(mode)
        self.assertTrue(self.editeur.option_casenoire.is_enlarged)
        self.assertFalse(self.editeur.option_casevide.is_enlarged)
        self.assertFalse(self.editeur.option_casevide.is_enlarged)
        self.editeur.zoom_on_option(mode)
        self.assertFalse(self.editeur.option_casenoire.is_enlarged)


    def test_randomize_skew(self):
        """ Méthode permettant de tester le comportement de randomize_skew. 
            La méthode randomize_skew est appellée et la valeur de retour est récupérée.
            Cette valeur doit être entière comprise entre -5 et 5 et différente de 0
        """
        valeur = self.editeur.randomize_skew()
        self.assertEqual(type(valeur), int)
        self.assertFalse(valeur == 0)
        self.assertTrue(valeur<=5 and valeur>=-5)

    def test_set_erreur(self):
        """ Méthode permettant de tester le comportement de set_erreur.
            L'erreur est initialisée avec la valeur MESSAGE_ERREUR_NOSOLUTION et set_erreur est appellée avec le paramètre 'click'.
            L'erreur doit être effacée.
            L'erreur est initialisée avec la valeur MESSAGE_ERREUR_NOSOLUTION et set_erreur est appellée avec le paramètre 'validation'.
            L'erreur ne doit pas être effacée.
            L'erreur est ensuite initialisée avec la valeur 'test' (n'importe quelle erreur) et set_erreur est appelée avec le paramètre 'validation'.
            L'erreur doit être effacée.
        """

        self.editeur.erreur = MESSAGE_ERREUR_NOSOLUTION
        self.editeur.set_erreur("click")
        self.assertEqual(self.editeur.erreur, "")

        self.editeur.erreur = "test"
        self.editeur.set_erreur("click")
        self.assertEqual(self.editeur.erreur, "test")

        self.editeur.set_erreur("validation")
        self.assertEqual(self.editeur.erreur, "")


if __name__ == "__main__":
    print("Test du module editeur")
    pygame.init()
    pygame.freetype.init()
    unittest.main()

        

