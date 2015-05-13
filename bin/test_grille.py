#!/usr/bin/python3
# -*- encoding:utf-8 -*


""" Module effectuant les tests unitaire du module grille

    Ce module est composé d'une unique classe GrilleTest, dont les méthodes effectuent les tests unitaires des méthodes de grille correspondantes.

    Module utilisé:
        - os: utilisé pour supprimer les fichiers générés par les tests unitaires des méthodes de sauvegarde/chargement.
        - random: utilisé pour les tests unitaires des méthodes de solveur
        - unittest: utilisé pour effectuer les tests unitaires
        - pygame: utilisé pour les tests unitaires incluant des méthodes graphiques
        - grille: utilisé pour tester ses méthodes
        - exceptions: utilisé pour les méthodes de validation
        - constantes: utilisé dans chaque méthode
        - cases: utilisé pour tester les types de la grille
"""
import os
import unittest
import random

import pygame
import pygame.freetype
from pygame.locals import *

import grille
import cases
import exceptions
from constantes import *

class GrilleTest(unittest.TestCase):
    """Classe permettant de tester les fonctionnement des méthodes de la classe Grille"""


    def setUp(self):
        """ Méthode appellée avant chaque test, permettant d'initialiser le test.
            Un attribut grille, de type Grille est ajouté, permettant de tester ses méthodes.
        """
        self.grille = grille.Grille()
        


    ######################################## Test des méthodes générateurs ################################################

    def test_keys(self, diff="moyen"):
        """ Méthode testant le comportement de la méthode keys()
            Cette méthode verifie bien que seul les clés du dictionnaire sont retournées.
            Elle verifie ensuite le type des clés.
        """
        self.grille.generer_grille(diff)
        for el in self.grille.keys():
            self.assertEqual(type(el), tuple)
            self.assertTrue(len(el) == 2)
            self.assertTrue(type(el[0]) == int and type(el[1]) == int)

            


    def test_values(self, diff="moyen"):
        """ Méthode testant le comportement de la méthode values().
            Cette méthode verifie bien que seul les valeurs du dictionnaire sont retournées.
            Elle verife ensuite leur type
        """

        self.grille.generer_grille(diff)
        for el in self.grille.values():
            self.assertTrue(type(el) == cases.CaseNoire or type(el) == cases.CaseVide or type(el) == cases.Indicatrice)
            



    def test_items(self, diff="moyen"):
        """ Méthode testant le comportement de la méthode items().
            Cette méthode verifie que la méthode retourne les clés et les valeurs.
            Elle verifie ensuite leur type.
        """

        self.grille.generer_grille(diff)
        for el in self.grille.items():       
            # Verifie que la méthode retourne un tuple
            self.assertEqual(type(el), tuple)
            self.assertEqual(len(el), 2)
            
            # Verifie que le premier élément est une clé
            self.assertEqual(type(el[0]), tuple)
            self.assertTrue(len(el[0]) == 2)
            self.assertTrue(type(el[0][0]) == int and type(el[0][1]) == int)
            
            # Verifie que le second élément est une valeur
            self.assertTrue(type(el[1]) == cases.CaseNoire or type(el[1]) == cases.CaseVide or type(el[1]) == cases.Indicatrice)
        


            
    def test_ligne(self, diff="moyen"):
        """ Méthode testant le comportement de la méthode ligne().
            Elle parcourt l'ensemble de la grille et appelle ligne() pour chaque case.
            Elle verifie que chaque élément du générateur est une case vide, et recupère cet élément dans une liste.
            Elle verifie ensuite que chaque élément de la ligne est bien dans la liste récupérée.
        """
        self.grille.generer_grille(diff)
        for(i,j) in self.grille.keys():
            element_ligne = []
            for el in self.grille.ligne(i,j):
                 self.assertEqual(type(el), cases.CaseVide)
                 element_ligne.append(el)
                 
            indice_colonne = i+1
            while indice_colonne < self.grille.nb_colonne and type(self.grille[indice_colonne, j]) is cases.CaseVide:
                self.assertTrue(self.grille[indice_colonne, j] in element_ligne)
                indice_colonne += 1
                     
            indice_colonne = i-1
            while indice_colonne >= 0 and type(self.grille[indice_colonne, j]) is cases.CaseVide:
                self.assertTrue(self.grille[indice_colonne, j] in element_ligne)
                indice_colonne -= 1

                
                


                    
    def test_colonne(self, diff="moyen"):
        """ Méthode testant le comportement de la méthode colonne().
            Elle parcourt l'ensemble de la grille et appelle colonne() pour chaque case.
            Elle verifie que chaque élément du générateur est une case vide, et récupère cet élément dans une liste.
            Elle verifie ensuite que chaque élément de la colonne est bien dans la liste récupérée.
        """

        self.grille.generer_grille(diff)
        for(i,j) in self.grille.keys():
            element_colonne = []
            for el in self.grille.colonne(i,j):
                self.assertEqual(type(el), cases.CaseVide)
                element_colonne.append(el)
                
            indice_ligne = j+1
            while indice_ligne < self.grille.nb_ligne and type(self.grille[i, indice_ligne]) is cases.CaseVide:
                self.assertTrue(self.grille[i, indice_ligne] in element_colonne)
                indice_ligne += 1
                     
            indice_ligne = j-1
            while indice_ligne >= 0 and type(self.grille[i, indice_ligne]) is cases.CaseVide:
                self.assertTrue(self.grille[i, indice_ligne] in element_colonne)
                indice_ligne -= 1

    ############################################ Tests des méthodes de générations de grilles #####################################################


    def test_blocked(self):
        """ Méthode testant le comportement de la méthode blocked().
            Cette méthode prend place après l'appel de _creer_structure.
            Elle parcourt l'ensemble de la grille et verifie qu'un élément bloqué est bien une indicatrice.
            Elle verifie ensuite qu'elle est bien bloquée par une indicatrice/case noire, ou par un bord de la grille.
        """
        self.grille._creer_structure(10)
        for (i,j) in self.grille.keys():
            bloquee = self.grille.blocked(i,j)
            if bloquee == True:
                self.assertEqual(type(self.grille[i,j]), cases.Indicatrice)
                if i < self.grille.nb_colonne - 1:
                    self.assertTrue((i,j) in self.grille.keys())
                if j < self.grille.nb_ligne - 1:
                    self.assertTrue((i,j) in self.grille.keys())
            
                
    def test_non_indicatrice_blocked(self, diff="facile"):
        """ Méthode testant qu'aucune indicatrice n'est bloquée dans une grille générée aléatoirement.
            Applique la méthode blocked à chaque case du tableau et verifie qu'elle ne retourne jamais vrai.
        """
        self.grille.generer_grille(diff)
        for(i,j) in self.grille.keys():
            self.assertFalse(self.grille.blocked(i,j))



    def test__creer_structure(self):
        """ Méthode permettant de tester le comportement de creer_structure().
            Elle parcourt l'ensemble des éléménts qui ont été créé et verifie leur type.
            Elle verifie ensuite que les éléments sont sur le bordures haut et gauche de la grille.
        """
        self.grille._creer_structure(10)
        for(i,j) in self.grille.keys():
            self.assertTrue(type(self.grille[i,j]) in (cases.Indicatrice,cases.CaseNoire))
            self.assertTrue(i <= 2 or j <= 2)




    def test__placer_indicatrices(self):
        """ Méthode permettant de tester le comportement de placer_indicatrices().
            Elle parcourt l'ensemble des éléments qui ont été créé et verifie leur type.
            Elle verifie qu'aucun élément n'est bloqué.
        """
        self.grille._creer_structure(10)
        self.grille._placer_indicatrices(10)
        for(i,j) in self.grille.keys():
            self.assertTrue(type(self.grille[i,j]) in (cases.CaseNoire, cases.Indicatrice))
            self.assertFalse(self.grille.blocked(i,j))




    def test__placer_valeurs(self):
        """ Méthode permettant de tester le comportement de placer_valeurs().
            Elle parcourt l'ensemble des indices que doit contenir la grille et verifie que les cases ont bien été créées.
            Elle verifie ensuite le type des cases.
        """       
        self.grille._creer_structure(10)
        self.grille._placer_indicatrices(10)
        self.grille._placer_valeurs()
        i,j = 0,0
        while i<self.grille.nb_colonne:
            while j<self.grille.nb_ligne:
                self.assertTrue((i,j) in self.grille.keys())
                self.assertTrue(type(self.grille[i,j]) in (cases.Indicatrice, cases.CaseNoire, cases.CaseVide))
                j += 1
            j = 0
            i += 1




    def test_choix_valeur(self):
        """ Méthode permettant de tester le comportement de choix_valeur().
            Ce test prend place suite à l'utilisation de _placer_valeur.
            Elle parcourt la grille et pour chaque case vide demande une valeur avec choix_valeur.
            Elle verifie ensuite que cette valeur n'est pas dans sa ligne ou sa colonne.
        """
        self.grille._creer_structure(10)
        self.grille._placer_indicatrices(10)
        self.grille._placer_valeurs()

        for (i,j) in self.grille.keys():
            if type(self.grille[i,j]) is cases.CaseVide:
                valeur = self.grille.choix_valeur(i,j)
                self.assertTrue(valeur not in self.grille.ligne(i,j) and valeur not in self.grille.colonne(i,j))

                

    def test_noircir(self):
        """ Méthode permettant de tester le comportement de noircir().
            Cette méthode prend place suite à l'appel de noircir().
            Elle parcourt la grille et pour chaque indicatrice, verifie qu'elle n'est pas bloquée.
        """
        self.grille._creer_structure(10)
        self.grille._placer_indicatrices(10)
        self.grille._placer_valeurs()
        self.grille.noircir()
        for (i,j) in self.grille.keys():
            if type(self.grille[i,j]) is cases.Indicatrice:
                self.assertFalse(self.grille.blocked(i,j))

                
        
    def test_somme_indicatrice(self, diff="moyen"):
        """ Méthode permettant de tester le comportement de somme_indicatrice().
            Une grille est généré avec la méthode générer_grille.
            Elle parcourt la grille et pour chaque indicatrice, verifie que la valeur de sa plage bas et plage droite ont bien été mise a jour.
            Elle verifie ensuite que cette valeur est correcte.
        """
        
        self.grille.generer_grille(diff)
        for (i,j) in self.grille.keys():
            if type(self.grille[i,j]) is cases.Indicatrice:
                self.assertTrue(self.grille[i,j].valeur_bas != 0 or self.grille[i,j].valeur_droite != 0)
                self.assertFalse(self.grille[i,j].valeur_bas <= 3 and self.grille[i,j].valeur_bas >= 45)
                self.assertFalse(self.grille[i,j].valeur_droite <= 3 and self.grille[i,j].valeur_droite >= 45)

                # Verification des valeurs des sommes
                somme_droite, somme_bas = 0,0
                if self.grille[i,j].valeur_droite != 0:
                    somme_droite += self.grille[i+1, j]._solution_case
                    for el in self.grille.ligne(i+1,j):
                        somme_droite += el._solution_case
                    self.assertEqual(somme_droite, self.grille[i,j].valeur_droite)
                    
                if self.grille[i,j].valeur_bas != 0:
                    somme_bas += self.grille[i, j+1]._solution_case
                    for el in self.grille.colonne(i,j+1):
                        somme_bas += el._solution_case
                    self.assertEqual(somme_bas, self.grille[i,j].valeur_bas)
                

    ########################################################## Tests des méthodes de jeu d'une grille #######################################################################

    def test_afficher_grille(self, diff="moyen"):
        """ Méthode permettant de tester le comportement de afficher_grille.
            Cette méthode verifie que les rect de chaque grille sont bien initialisé, et ont des valeurs cohérentes.
        """

        pygame.init()
        pygame.freetype.init()
        fenetre = pygame.display.set_mode(TAILLE_FENETRE_TEST)
        self.grille.generer_grille(diff)
        self.grille.afficher_grille(fenetre)
        pygame.quit()
        
        for (i,j) in self.grille.keys():
            self.assertEqual(type(self.grille[i,j].rect), pygame.Rect)
            self.assertTrue(self.grille[i,j].rect.top != 0)
            self.assertTrue(self.grille[i,j].rect.left != 0)
            self.assertTrue(self.grille[i,j].rect.width != 0)
            self.assertTrue(self.grille[i,j].rect.height != 0)
            if type(self.grille[i,j]) == cases.Indicatrice:
                self.assertEqual(type(self.grille[i,j].rect_bas), pygame.Rect)
                self.assertEqual(type(self.grille[i,j].rect_droite), pygame.Rect)

    def test_validate(self, diff="moyen"):
        """ Méthode permettant de tester le comportement de validate.
            Cette méthode verifie qu'une grille sans erreur ne lève aucune exception.
            A l'inverse, une grille comportant des erreurs lève bien l'une des exceptions attendues.
        """
        # test exception mixte
        self.grille.generer_grille(diff)
        self.grille.validate()
        for (i,j) in self.grille.keys():
            if type(self.grille[i,j]) is cases.CaseVide:
                self.grille[i,j].valeur_saisie = 1
        with self.assertRaises(exceptions.ExceptionMixte):
            self.grille.validate()
        #test pas d'exception
        self.grille.solve()
        try:
            self.grille.validate()
        except Exception as i:
            print(i)
            self.fail("solve() a généré une erreur!")

        
        #test exception doublon
        self.grille.reinitialiser() #on ecrase la grille courante
        for (i,j) in self.grille.keys():
            if type(self.grille[i,j]) is cases.CaseVide:
                self.grille[i,j].valeur_saisie = 1

        with self.assertRaises(exceptions.ExceptionMixte):
            self.grille.validate()

        #test exception somme incorrecte
        self.grille.solve()
        for (i,j) in self.grille.keys():
            if type(self.grille[i,j]) is cases.Indicatrice:
                self.grille[i,j].valeur_droite+=1
        with self.assertRaises(exceptions.SommeIncorrecteException):
            self.grille.validate()


    def test_has_fausse_somme_doublon(self, diff="moyen"):
        """ Méthode testant les methodes has_fausse_somme et has_doublon de la classe grille.
            1) application des fonctions à une grille vide. resultat voulu : False, False
            2) application des fonctions à une grille résolue. resultat voulu : False, False
            3) application des fonctions à une grille dont on a propagé la valeur des cases vides. resultat voulu : True, True"""        

        #test 1
        self.grille.generer_grille(diff)
        #j'aimerais tellement avoir une fonction lambda pour les 5 lignes qui suivent :
        for (i,j) in self.grille.keys():
            if (type(self.grille[i,j]) is cases.Indicatrice):
                self.assertFalse(self.grille.has_fausse_somme(i,j))
            elif (type(self.grille[i,j]) is cases.CaseVide):
                self.assertFalse(self.grille.has_doublon(i,j))
        #mais on peut mettrre qu'une seule instruction dans une lambda T_T

        #test 2
        self.grille.solve()
        for (i,j) in self.grille.keys():
            if (type(self.grille[i,j]) is cases.Indicatrice):
                self.assertFalse(self.grille.has_fausse_somme(i,j))
            elif (type(self.grille[i,j]) is cases.CaseVide):
                self.assertFalse(self.grille.has_doublon(i,j))

        #preparatifs pour test 3
        for (i,j) in self.grille.keys():
            #si on est sur case vide et que la case de droite l'est aussi (en s'assurant au passage qu'elle existe)
            if (type(self.grille[i,j]) is cases.CaseVide) and ((i+1,j) in self.grille.keys()) and (type(self.grille[i+1,j]) is cases.CaseVide):
                #on propage les valeur_saisie ce qui créée des doublons et des sommes incorrectes
                self.grille[i+1,j].valeur_saisie=self.grille[i,j].valeur_saisie

        #test 3
        f_somme, doublon = False, False
        for (i,j) in self.grille.keys():
            if (type(self.grille[i,j]) is cases.Indicatrice):
                if self.grille.has_fausse_somme(i,j) :
                    f_somme=True
            elif (type(self.grille[i,j]) is cases.CaseVide):
                if self.grille.has_doublon(i,j) :
                    doublon=True
        self.assertTrue(f_somme)
        self.assertTrue(doublon)


    def test_reinitialiser(self, diff="moyen"):
        """ Méthode permettant de tester le comportement de reinitialiser. 
            A partir d'une grille vide, il remplit toute ses cases vides par 1.
            Elle appelle ensuite reinitialiser et verifie que l'ensemble des cases vides ont pour valeur -1
        """

        self.grille.generer_grille(diff)
        for (i,j) in self.grille.keys():
            if type(self.grille[i,j]) is cases.CaseVide:
                self.grille[i,j].valeur_saisie = 1

        self.grille.reinitialiser()

        for (i,j) in self.grille.keys():
            if type(self.grille[i,j]) is cases.CaseVide:
                self.assertEqual(self.grille[i,j].valeur_saisie, (-1))


    def test_solve(self, diff="moyen"):
        """ Méthode testant le comportement de la méthode solve.
            Une grille est générée alétatoirement. Le test verifie que chacune des valeurs saisies est a -1.
            La méthode solve est lancée, le test verifie que chacune des valeurs saisies est egale a la solution de la case.
        """

        self.grille.generer_grille(diff)
        for(i,j) in self.grille.keys():
            if type(self.grille[i,j]) is cases.CaseVide:
                self.assertEqual(self.grille[i,j].valeur_saisie, -1)
        self.grille.solve()
        for(i,j) in self.grille.keys():
            if type(self.grille[i,j]) is cases.CaseVide:
                self.assertEqual(self.grille[i,j].valeur_saisie, self.grille[i,j]._solution_case)
                

    def test_victoire(self, diff="moyen"):
        """ 
            Méthode permettant de tester le comportement de la méthode victoire().
            Elle genere une grille et verifie qu'elle n'est pas considérée comme finie.
            Elle affecte ensuite la solution a la grille et verifie que cette la grille est considérée comme juste
        """
        self.grille.generer_grille(diff)
        self.assertFalse(self.grille.victoire())
        
        for(i,j) in self.grille.keys():
            if type(self.grille[i,j]) is cases.CaseVide:
                self.grille[i,j].valeur_saisie = self.grille[i,j]._solution_case
        self.grille.validate()
        self.assertTrue(self.grille.victoire()) 



    ###################################################################### Tests des méthodes d'éditions de grille #########################################################

    def test_generer_grille_vide(self):
        """ Méthode permettant de tester le comportement de generer_grille_vide(). 
            Cette méthode génère une grille à l'aide de cette méthode et verifie que pour tout les indices attendus dans la grille, une case vide est bien définie.
        """
        self.grille.generer_grille_vide()
        i, j = 0, 0
        while i < self.grille.nb_ligne:
            while j < self.grille.nb_colonne:
                self.assertEqual(type(self.grille[i,j]), cases.CaseVide)
                j += 1
            j = 0
            i += 1

    def test_longueur(self, diff="moyen"):
        """ Méthode permettant de tester le comportement de longueur().
            Ce test sera effectué à l'aide du générateur keys de Grille.
            Il y a autant de clé dans le dictionnaire que d'élément dans la grille.
            longueur(self.grille.keys()) doit donc être égale à NB_LIGNE_GRILLE * NB_COLONNE_GRILLE, définies dans les constantes.
        """
        self.grille.generer_grille(diff)
        self.assertEqual(self.grille.longueur(self.grille.keys()), NB_LIGNE_GRILLE*NB_COLONNE_GRILLE)


    def test_valeur_min_max(self):
        """ Méthode permettant de tester les comportements des methodes valeur_min et valeur_max.
            Pour chaque longueur entre 1 et 9 est calculé sa valeur minimale et maximale possible, en sommant des nombres strictement différent sur cette longueur.
            La valeur minimale doit être égale à valeur_min de cette longueur.
            La valeur maximale doit être égale à valeur_max de cette longueur.
        """
        for i in range(1, 10):
            valeur = 1
            min = max = 0
            while valeur <= i:
                min += valeur
                max += (10 - valeur)
                valeur += 1
            self.assertEqual(self.grille.valeur_min(i), min)
            self.assertEqual(self.grille.valeur_max(i), max)

    def test_has_fausse_valeur(self, diff="moyen"):
        """ Méthode permettant de tester le comportement de has_fausse_valeur.
            Une grille est généré aléatoirement.
            Pour chaque indicatrice, has_fausse_valeur est appelé et doit retourner False.
            Ensuite, sa valeur bas prend la valeur inférieure à sa valeur minimale possible, has_fausse_valeur doit retourner True.
            Ensuite sa valeur droite prend la valeur supérieure à sa valeur maximale possible, has_fausse_valeur doit aussi retourner True.
        """

        self.grille.generer_grille(diff)
        for (i,j) in self.grille.keys():
            if type(self.grille[i,j]) is cases.Indicatrice:
                self.assertFalse(self.grille.has_fausse_valeur(i,j))

                # Initialisation des variables utilisées
                valeur_bas = self.grille[i,j].valeur_bas

                # Modification de la valeur de la plage bas
                if (i,j+1) in self.grille.keys() and type(self.grille[i,j+1]) is cases.CaseVide:
                    longueur_plage_bas = self.grille.longueur(self.grille.colonne(i,j+1)) + 1

                    self.grille[i,j].valeur_bas = (self.grille.valeur_min(longueur_plage_bas) - 1)
                else:
                    self.grille[i,j].valeur_bas = 1 

                self.assertTrue(self.grille.has_fausse_valeur(i,j))
                self.assertTrue(self.grille[i,j].erreur_bas)

                
                # Reinitialisation de la plage bas
                self.grille[i,j].valeur_bas = valeur_bas
                self.grille[i,j].erreur_bas = False

                # Modification de la valeur de la plage droite
                if (i+1,j) in self.grille.keys() and type(self.grille[i+1,j]) is cases.CaseVide:
                    longueur_plage_droite = self.grille.longueur(self.grille.ligne(i+1,j)) + 1
                    self.grille[i,j].valeur_droite = (self.grille.valeur_max(longueur_plage_droite) + 1)
                else:
                    self.grille[i,j].valeur_droite = 1
                    
                self.assertTrue(self.grille.has_fausse_valeur(i,j))
                self.assertTrue(self.grille[i,j].erreur_droite)

    def test_validate_saisie(self, diff="moyen"):
        """ Méthode permettant de tester le comportement de validate_saisie.
            Une première grille est générée, toutes ses cases vides sont noircies et les indicatrices ont des valeurs nulles.
            Sa validation doit lever une BlockedException.
            Une seconde grille est générée, toutes ses indicatrices ont des valeurs impossibles.
            Sa validation doit lever une ValeurIncorrecteException.
            Une dernière grille est générée, seules ses cases vides sont noircies.
            Sa validation doit lever une ExceptionMixte.
        """
        self.grille.generer_grille(diff)

        # Noircir toutes les cases et mettre a 0 les valeurs des indicatrices
        for(i,j) in self.grille.keys():
            if type(self.grille[i,j]) is cases.CaseVide:
                self.grille[i,j] = cases.CaseNoire()
            if type(self.grille[i,j]) is cases.Indicatrice:
                self.grille[i,j].valeur_bas = self.grille[i,j].valeur_droite = 0

        with self.assertRaises(exceptions.BlockedException):
            self.grille.validate_saisie()

        self.grille._grid = {}
        self.grille.generer_grille(diff)

        # Modifier uniquement les valeurs des indicatrices
        for (i,j) in self.grille.keys():
            if type(self.grille[i,j]) is cases.Indicatrice:
                self.grille[i,j].valeur_bas = 0
                self.grille[i,j].valeur_droite = 46

        with self.assertRaises(exceptions.ValeurIncorrecteException):
            self.grille.validate_saisie()  

        # Noircir uniquement les cases en laissant les valeurs des indicatrices
        for(i,j) in self.grille.keys():
            if type(self.grille[i,j]) is cases.CaseVide:
                self.grille[i,j] = cases.CaseNoire()
        with self.assertRaises(exceptions.ExceptionMixte):
            self.grille.validate_saisie()


    ######################################### Test des méthodes de chargement et sauvegarde d'une grille ######################################################

    def test_sauvegarde_chargement(self, diff="moyen", nom_fichier="TU_save_load"):
        """ Méthode permettant de tester le comportement des methodes sauvegarde et chargement d'une grille.
            Cette méthode génère une grille aléatoire et la sauvegarde dans un fichier.
            Elle stocke l'attribut grid dans une variable grille de la grille actuelle et recharge la grille du fichier sauvegardé.
            L'attribut grille de la grille et la variable grille doivent être égale.
        """

        self.grille.generer_grille(diff)
        grille = self.grille._grid

        self.grille.sauvegarde(nom_fichier)
        self.grille.chargement(nom_fichier)

        self.assertEqual(self.grille._grid, grille)
        os.remove(nom_fichier)


    ######################################## Test des méthode sdu solveur ##############################################################################################

    def test_confirmer_solution(self):
        """ Méthode permettant de tester le comportement de confirmer_solution.
            Une grille vide est générée, l'ensemble des valeurs saisies des cases vides est mise à 2.
            confirmer_solution est ensuite appelée.
            La grille est parcourue, pour chacune des cases la valeur saisie doit être -1 et la valeur de la case doit être 2, la valeur_saisie avant l'appel.
        """
        self.grille.generer_grille_vide()
        for (i,j) in self.grille.keys():
            self.grille[i,j].valeur_saisie = 2
        self.grille.confirmer_solution()
        for (i,j) in self.grille.keys():
            self.assertEqual(self.grille[i,j].valeur_saisie, -1)
            self.assertEqual(self.grille[i,j]._solution_case, 2)

    def test_get_domaine(self):
        """ Méthode permettant de tester le comportement de get_domaine.
            Une valeur est tirée entre 1 et 45 et une longueur entre 1 et 9. On calcule le domaine possible sur cette valeur avec cette longueur.
            Si le taille du domaine est égale a la longueur courante, la somme des éléments du domaine est calculée et doit être égale à la valeur courante.
        """
        valeur = random.choice(range(1,46))
        longueur = random.choice(range(1,10))

        domaine = self.grille.get_domaine(valeur,longueur)

        if len(domaine) == longueur:
            somme = 0
            for el in domaine:
                somme += el
            self.assertEqual(somme, valeur)

    def test_has_indicatrice(self, diff="mdft"):
        """ Méthode permettant de tester le comportement de has_indicatrice.
            Une grille vide est générée, la méthode est lancée sur chacune des cases et doit retourner False dans tout les cas.
            Une grille de jeu est ensuite générée, la méthode est lancée sur chacune des cases vides et doit retourner True dans tout les cas.
        """

        self.grille.generer_grille_vide()
        for (i,j) in self.grille.keys():
            self.assertFalse(self.grille.has_indicatrice(i,j))

        self.grille.generer_grille(diff)
        for (i,j) in self.grille.keys():
            if type(self.grille[i,j]) is cases.CaseVide:
                self.assertTrue(self.grille.has_indicatrice(i,j))






        
                
if __name__ == "__main__":
    print("Test du module grille")
    unittest.main()



    
