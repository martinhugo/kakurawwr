#!/usr/bin/python3
# -*- encoding: utf-8 -*

""" Module Solveur du produit.
    Ce module permet l'implémentation de la fonctionnalité Solveur.
    Ce module possède une unique classe Solveur.

    Modules importés:
        - pygame: utilisé pour l'affichage
        - boutons: utilisé pour  afficher les informations à l'écran
        - constantes: utilisé par toutes les méthodes
        - cases : utilisé lors du calcul de la solution
        - grille : utilisé lors du calcul de la solution
        - random : utilisé lors du calcul de la solution
        - exception: utilisé pour les grilles sans solutions

"""
import random
import pygame
from pygame.locals import *
import pygame.freetype
import cases
import jeu
import boutons
from grille import *
from exceptions import *
from constantes import *


class Solveur:
    """ Classe permettant de calculer la solution d'une grille tout en affichant les différentes étapes de calcul à l'utilisateur.
        Cette classe possède 4 attributs:
            - _fenetre: la fenetre d'affichage de l'écran
            - _grille: la grille en cours d'edition
            - bouton_abandon: bouton permettant d'arreter le calcul de la solution
            - barre_erreur: zone d'affichage
            - message: message devant être affiché à l'utilisateur      
    """

    def __init__(self, fenetre, grille):
        """ Initialise les attributs de la classe.
            La fenetre d'affichage et la grille à calculer sont passées en paramètre.
            Le bouton d'abandon, la barre d'erreur sont initialisées. 
            Le compteur de message est initialisé à 0.
        """

        self._fenetre = fenetre
        self._grille = grille
        self.bouton_abandon = boutons.Bouton(TITRE_BOUTON_ABANDON)
        self.barre_erreur = boutons.BarreErreur(pygame.freetype.Font(CHEMIN_FICHIER_POLICE, TAILLE_POLICE_BOUTON))
        self.compteur_changement_message = 0
        self.message = ""

    def afficher(self):
        """ Affiche l'ecran du solveur.
            La grille est affiché ainsi que le bouton d'abandon.
            Le message est affiché par la barre_erreur.
        """
        titre_bouton = pygame.freetype.Font(CHEMIN_FICHIER_POLICE, TAILLE_POLICE_BOUTON)
        bouton_img = pygame.image.load(CHEMIN_IMAGE_BOUTON).convert_alpha()

        self.bouton_abandon.afficher(self._fenetre, bouton_img, titre_bouton, POSITION_BOUTON_RETOUR)
        self._grille.afficher_grille(self._fenetre)
        self.barre_erreur.afficher_erreur(self._fenetre, self.message , COULEUR_POLICE)


    def calculate_solution(self):
        """ Méthode permettant de calculer la solution d'une grille.
            Dans un premier temps, la grille est mis dans une forme calculable.
            Cette méthode calcule l'ensemble des domaines de valeurs pour chaque plage et affecte à domaine leur intersection.
            Elle verifie ensuite si la grille à une solution.
            Elle appelle le solveur sur la première case si c'est le cas
        """
        self.message = MESSAGE_CORRECTION_GRILLE
        self.correction_grille()
        self.message = MESSAGE_ENSEMBLES_POSSIBLES
        self.distribuer_domaine()
        self.message = MESSAGE_SOLVABILITE
        self.has_solution()
        self.message = MESSAGE_CALCUL
        self.solveur(0,0)
        return MESSAGE_GRILLE_RESOLUE



    def correction_grille(self):
        """ Méthode permettant de corriger les éventuelles erreurs laissées par l'utilisateur lors de la saisie de la grille. 
            Les cases vides n'étant rattachées à aucune indicatrice sont transformées en case noire.
        """

        for (i,j) in self._grille.keys():
            self._fenetre.fill(COULEUR_FOND)
            self.afficher()
            pygame.display.flip()
            self.gestion_evenement()

            if type(self._grille[i,j]) is cases.CaseVide and not(self._grille.has_indicatrice(i,j)):
                self._grille[i,j] = cases.CaseNoire()



    def solveur(self, i, j):
        """ Méthode permettant de générer la solution d'une grille. 
            Cette méthode est récursive et s'appelle sur les cases de la grille.

            Si la case courante est une case vide, elle essaye de lui affecter comme valeur une de ses valeurs_possibles.
            Si ce n'est pas possible elle retourne False et remet sa valeur a -1. Si la grille est finie après avoir entré cette valeur, elle retourne True.

            Elle lance ensuite l'appel sur la case suivante (en fonction de la position dans la grille) tant qu'il ne retourne pas true ou qu'il reste des valeurs à affecter.
            Si cet appel retourne faux, elle change sa propre valeur. 
            Si il n'y a plus de valeurs possibles, elle retourne alors elle-même faux après avoir remis sa valeur à -1. 
            Si cet appel retourne vrai, elle le retourne.

            Si ce n'est pas une case vide n'ayant pas de valeurs saisies, elle lance simplement l'appel sur la case suivante et retourne son retour.
        """
        # Affichage
        self.change_message()
        self._fenetre.fill(COULEUR_FOND)
        self.afficher()
        pygame.display.flip()
        self.gestion_evenement()

        # Cas d'une case vide
        if type(self._grille[i,j]) is cases.CaseVide and self._grille[i,j].valeur_saisie == -1:
            valeurs_possibles = list(self._grille[i,j].domaine)
            erreur = True
            fin = False

            # On teste chaque valeur jusqu'a ce qu'une marche
            while erreur and len(valeurs_possibles) != 0:
                self._grille[i,j].valeur_saisie = random.choice(valeurs_possibles)
                try:
                    self._grille.validate()
                    erreur = False
                except:
                    valeurs_possibles.remove(self._grille[i,j].valeur_saisie)
                    erreur = True

            # Si aucune ne marche, on retourne False. La grille n'a pas de solutions en l'état
            if erreur:
                self._grille[i,j].valeur_saisie = -1
                return False

            # Si la grille est fini, on retourne la solution
            elif self._grille.victoire():
                return True

            
            # Partie recursive
            while not(fin) and len(valeurs_possibles) != 0:

                if i < self._grille.nb_colonne - 1:
                    fin = self.solveur(i+1, j)

                elif j < self._grille.nb_ligne - 1:
                    fin = self.solveur(0,j+1)

                if not(fin):
                    valeurs_possibles.remove(self._grille[i,j].valeur_saisie)
                    if len(valeurs_possibles) != 0:
                        self._grille[i,j].valeur_saisie = random.choice(valeurs_possibles)


            if fin:
                return True
            else:
                self._grille[i,j].valeur_saisie = -1
                return False
              
        # Cas d'une case noire/indicatrice, on réitère simplement l'appel
        else:
            if self._grille.victoire():
                return True

            if i < self._grille.nb_colonne - 1:
                return self.solveur(i+1, j)
            elif j < self._grille.nb_ligne - 1:
               return self.solveur(0,j+1)



    def distribuer_domaine(self):
        """ Méthode permettant d'affecter à chaque case vide son domaine de valeur possible.
            Cet ensemble permettrait de donner une solution à la grille.
            Pour chaque indicatrice, elle calcule le domaine de valeur de sa plage bas et droite, en fonction de ses valeurs bas et droites et des longueurs de chaque plage.
            Pour chaque case de la plage bas, l'intersection entre le domaine_bas et son domaine existant est affecté à la case.
            Pour chaque case de la plage droite, l'intersection entre le domaine_droite et son domaine existant est affecté à la case.
        """
        # Affichage
        self._fenetre.fill(COULEUR_FOND)
        self.afficher()
        pygame.display.flip()

        
        for (i,j) in self._grille.keys():

            self.gestion_evenement()

            if type(self._grille[i,j]) is cases.Indicatrice:

                if self._grille[i,j].valeur_droite != 0:
                    # Calcul du nouveau domaine possible
                    longueur_droite = Grille.longueur(self._grille.ligne(i+1,j)) + 1
                    domaine_droite = Grille.get_domaine(self._grille[i,j].valeur_droite, longueur_droite)

                    # Intersection entre domaines
                    self._grille[i+1, j].domaine = set.intersection(self._grille[i+1,j].domaine, domaine_droite)
                    for el in self._grille.ligne(i+1, j):
                            el.domaine = set.intersection(el.domaine,domaine_droite)

                if self._grille[i,j].valeur_bas != 0:
                    # Calcul du nouveau domaine possible
                    longueur_bas = Grille.longueur(self._grille.colonne(i,j+1)) + 1
                    domaine_bas = Grille.get_domaine(self._grille[i,j].valeur_bas, longueur_bas)

                    # Intersection des domaines
                    self._grille[i,j+1].domaine = set.intersection(self._grille[i,j+1].domaine, domaine_bas)
                    for el in self._grille.colonne(i, j+1):
                            el.domaine = set.intersection(el.domaine,domaine_bas)



    def has_solution(self):
        """ Méthode permettant de verifier si une grille à une solution calculable.
            Parcourt l'ensemble de la grille. Si une case vide à un domaine contenant un seul élément, elle affecte à la case cette valeur.
            Elle retire cette valeur des domaines de l'ensemble des cases de sa plage.

            Elle parcourt ensuite une seconde fois la grille et verifie qu'aucune case vide n'a un domaine vide, sans avoir de valeur_saisie.
        """

        for (i,j) in self._grille.keys():

            # Affichage
            self._fenetre.fill(COULEUR_FOND)
            self.afficher()
            pygame.display.flip()
            self.gestion_evenement()

            if type(self._grille[i,j]) is cases.CaseVide and len(self._grille[i,j].domaine) == 1:
                # On affecte les valeurs evidentes
                self._grille[i,j].valeur_saisie = list(self._grille[i,j].domaine)[0]
                valeur = self._grille[i,j].valeur_saisie

                # On retire cette valeur des valeurs possibles de chaque case de la plage
                for el in self._grille.ligne(i,j):
                    if valeur in el.domaine:
                        el.domaine.remove(valeur)
                for el in self._grille.colonne(i,j):
                    if valeur in el.domaine:
                        el.domaine.remove(valeur)

        # On teste si la grille a une solution
        for (i,j) in self._grille.keys():
            if type(self._grille[i,j]) is cases.CaseVide:
                if len(self._grille[i,j].domaine) == 0 and self._grille[i,j].valeur_saisie == -1:
                    raise NoSolutionException()


    def change_message(self):
        """ Cette méthode permet de changer le message affiché à l'écran.
            Le compteur_changement_message est incrémenté à chaque appel.
            Si ce compteur arrive à un multiple de VAL_CHANGEMENT_MESSAGE, le message affiché à l'écran est changé.
        """
        self.compteur_changement_message += 1
        if self.compteur_changement_message % VAL_CHANGEMENT_MESSAGE == 0:
            self.message = random.choice(TABLEAU_MESSAGE)
        

    def gestion_evenement(self):
        """ Méthode permettant de gérer les évenements.
            Cette méthode est utilisé dans chaque étape du solveur pour permettre à l'utilisateur de quitter le jeu ou le calcul de la grille.
            Cela permet aussi de simplement intéragir avec la fenêtre sans entrainer de problème avec le calcul de la solution
        """
        for event in pygame.event.get():

                if event.type == QUIT:
                    pygame.quit()

                if event.type == MOUSEBUTTONUP:
                    curseur = pygame.Rect(event.pos, (0,0))

                    if self.bouton_abandon.clicked(curseur):
                        raise AbandonException()

        


                    
                        
