#!/usr/bin/python3
# -*- encoding:utf-8 -*


""" Module effectuant les tests unitaire du module sauvegarde.

    Ce module est composé d'une classe SauvegardeChargementTest, dont les méthodes effectuent les tests unitaires des méthodes de Sauvegarde et Chargement correspondantes.

    Module utilisé:
        - os: permet un traitement sur les fichiers créés (suppression)
        - pygame: tests unitaires des méthodes de jeu
        - unittest: utilisé pour effectuer les tests unitaires
        - grille: utilisé pour tester les méthodes de sauvegarde
        - sauvegarde: utilisé pour tester les méthodes
        - constantes: utilisé dans chaque méthode
        - cases: utilisé pour tester les types de la grille
        - constantes: utilisé dans differentes méthodes.
"""
import os
import pygame
import pygame.freetype
from pygame.locals import *
import unittest
import grille
import cases
import sauvegarde
from constantes import *

class SauvegardeChargementTest(unittest.TestCase):
    """Classe permettant de tester les fonctionnement des méthodes de la classe Editeur"""

    def setUp(self):
        """ Méthode appellée avant chaque test, permettant d'initialiser le test.
            Un unique attribut sauvegarde est créé, dont la fenetre est initialisé à (0,0) et la grille à une grille Vide.
        """
        self.sauvegarde = sauvegarde.Sauvegarde((0,0), grille.Grille())
        self.chargement = sauvegarde.Chargement((0,0))

    def test_valider(self, chemin_fichier="test", faux_chemin="incorrect"):
        """ Méthode permettant de tester le comportement des méthodes valider des classes Sauvegarde et Chargement.
            Dans un premier temps, on cherche à sauvegarder la grille avec une chaine vide comme nom de fichier, la méthode doit renvoyer False.
            Ensuite, on essaye d'executer cette sauvegarde avec chemin_fichier, le nom du fichier créé doit être le chemin_fichier, concaténé à l'extension .rawr.
            La méthode doit retourner True.

            Ensuite, on essaye successivement de charger un fichier appellé par la chaine vide, ou par un nom de fichier n'existant pas. Dans chacun de ces cas, la méthode doit retourner False.
            On charge le fichier avec une nom de fichier existant, la méthode doit retourner True.

            Le fichier est ensuite supprimé.
        """
        # Verification de la sauvegarde du fichier
        self.assertFalse(self.sauvegarde.valider())
        self.sauvegarde.nom_fichier = chemin_fichier
        self.assertTrue(self.sauvegarde.valider())

        # Verification de l'existence du fichier
        self.assertEqual(self.sauvegarde.nom_fichier, CHEMIN_DOSSIER_SAUVEGARDE + chemin_fichier + EXTENSION_FICHIER_SAUVEGARDE)

        # Verification du chargement du fichier
        self.assertFalse(self.chargement.valider())
        self.chargement.nom_fichier = faux_chemin
        self.assertFalse(self.chargement.valider())
        self.chargement.nom_fichier = chemin_fichier
        self.assertTrue(self.chargement.valider())

        # Suppression du fichier
        os.remove(CHEMIN_DOSSIER_SAUVEGARDE + chemin_fichier+ EXTENSION_FICHIER_SAUVEGARDE)



if __name__=="__main__":
    pygame.freetype.init()
    print("Test du module sauvegarde: ")
    unittest.main()

    
    
