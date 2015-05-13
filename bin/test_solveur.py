#!/usr/bin/python3
# -*- encoding:utf-8 -*


""" Module effectuant les tests unitaire du module solveur
    Ce module est composé d'une unique classe SolveurTest, dont les méthodes effectuent les tests unitaires des méthodes de solveur correspondante.

    Module utilisé:
        - pygame: tests unitaires des méthodes de jeu
        - unittest: utilisé pour effectuer les tests unitaires
        - grille: utilisé pour tester ses méthodes
        - exceptions: utilisé pour les méthodes de validation
        - constantes: utilisé dans chaque méthode
        - cases: utilisé pour tester les types de la grille
        - solveur: utilisé pour tester ses méthodes
        - exceptions: permet de tester qu'une grille sans solution lève bien l'exception attendu
"""

import pygame
import pygame.freetype
from pygame.locals import *
import unittest
import grille
import cases
import solveur
from constantes import *
from exceptions import *

class SolveurTest(unittest.TestCase):
    """Classe permettant de tester les fonctionnement des méthodes de la classe Editeur"""

    def setUp(self):
        """ Méthode appellée avant chaque test, permettant d'initialiser le test.
            Un attribut solveur, contenant un objet de type Solveur est ajouté, pour permettre de tester ses méthodes.
        """
        self.solveur = solveur.Solveur(0,0)
        
    def test_change_message(self):
        """ Methode permettant de tester le comportement de change_message.
            Le message courant est stocké dans une variable. La méthode est appelé pour le compteur initialisé à 1.
            Le message ne doit pas avoir changé.
            Le compteur de changement de message est mis a VAL_CHANGEMENT_MESSAGE - 1. La méthode est appelée.
            Le message doit avoir changé.
        """

        message = self.solveur.message
        self.solveur.change_message()
        self.assertEqual(self.solveur.message, message)

        self.solveur.compteur_changement_message = VAL_CHANGEMENT_MESSAGE - 1
        self.solveur.change_message()
        self.assertTrue(self.solveur.message != message)

    def test_correction_grille(self):
        """ Méthode permettant de tester le comportement de correction_grille. 
            Une grille vide est générée, on verifie que toutes ses cases sont bien des cases vides.
            La méthode est appelée, on verifie bien qui suite à l'appel, toutes les cases sont bien des cases noires.
        """

        self.solveur._fenetre = pygame.display.set_mode(TAILLE_FENETRE_TEST)
        self.solveur._grille = grille.Grille()
        self.solveur._grille.generer_grille_vide()

        for (i,j) in self.solveur._grille.keys():
            self.assertEqual(type(self.solveur._grille[i,j]), cases.CaseVide)

        self.solveur.correction_grille()

        for (i,j) in self.solveur._grille.keys():
            self.assertEqual(type(self.solveur._grille[i,j]), cases.CaseNoire)

    def test_has_solution(self):
        """ Méthode permettant de tester le comportement de has_solution.
            Ce test est divisé en deux parties.

            Une grille vide est generée.
            Un compteur est initialisé a 0.
            Pour chacune de ces cases, le domaine est modifié par un set contenant uniquement la valeur du compteur, qui est ensuite incrémenté. 
            La méthode est appelé et le compteur remis à 0.
            La grille est à nouveau parcouru. 
            La valeur saisie ne doit jamais être -1 et être égale au compteur, qui est ensuite incrémenté.

            Le domaine de chacune des cases vides est ensuite initialisé à un set vide.
            La méthode est appelée est doit lever une NoSolutionException.
        """

        self.solveur._fenetre = pygame.display.set_mode(TAILLE_FENETRE_TEST)
        self.solveur._grille = grille.Grille()
        self.solveur._grille.generer_grille_vide()

        compteur = 0
        for (i,j) in self.solveur._grille.keys():
            self.solveur._grille[i,j].domaine ={compteur}
            compteur += 1

        self.solveur.has_solution() 

        compteur = 0
        for (i,j) in self.solveur._grille.keys():
            self.assertTrue(self.solveur._grille[i,j].valeur_saisie == compteur and self.solveur._grille[i,j].domaine == {compteur})
            self.solveur._grille[i,j].domaine = set()
            self.solveur._grille[i,j].valeur_saisie = -1
            compteur += 1

        with self.assertRaises(NoSolutionException):
            self.solveur.has_solution()



if __name__ == "__main__":
    pygame.init()
    pygame.freetype.init()
    unittest.main()