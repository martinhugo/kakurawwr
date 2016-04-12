#!/usr/bin/python3
# -*- encoding:utf-8 -*

""" Module contenant la classe grille permettant de generer, saisir, afficher et jouer une grille.

    Contient la classe suivante:
       - Grille

     Modules importés:
        - random: utilisé pour la génération de grille
        - pickle: utilisé pour la sauvegarde et le chargement d'une grille
        - pygame: utilisé pour l'affichage et le jeu d'une grille
        - cases: utilisé pour creer la grille (génération/édition)
        - constantes: utilisé dans toutes les méthodes
        - exceptions: utilisé lors de la validation d'une grille (jeu/édition)

    Les constantes de pygame et du produit, ainsi que les exceptions, sont importés dans l'espace de nommage du jeu, pour une utilisation simplifiée.
"""

import random
import pickle
import pygame
from pygame.locals import *
import pygame.freetype
import cases
from constantes import *
from exceptions import *

class Grille:
    """ Classe modélisant la grille du Kakuro.
        Elle possède un attribut de type dict, une largeur et une hauteur.
    """

    def __init__(self, **kwargs):
        """ Initialise la grille avec un dictionnaire vide.
            Les attributs nb_ligne et nb_colonne sont initialisés selon les constantes NB_LIGNE_GRILLE, NB_COLONNE_GRILLE
        """
        self._grid = {}

        if "grid" in kwargs:
            grid = kwargs["grid"]

            for (i,j) in grid.keys():
                
                caseType = type(grid[i,j])
                case = grid[i,j]

                if caseType is cases.CaseVide:
                    self[i,j] = cases.CaseVide(case)
                
                elif caseType is cases.CaseNoire:
                    self[i,j] = cases.CaseNoire()

                else:
                    self[i,j] = cases.Indicatrice(case)


        self.nb_ligne = NB_LIGNE_GRILLE
        self.nb_colonne = NB_COLONNE_GRILLE
        self.solved = False



    ####################################################################### Méthodes spéciales ################################################################################
    
    def __getitem__(self, indice):
        """Action effectuée lors d'un acces du type self[indice]""" 
        return self._grid[indice]


    def __setitem__(self, indice, value):
        """Action effectuée lors d'un acces du type self[indice] = value""" 
        self._grid[indice] = value


    def __str__(self):
        """Action effectuée lors d'un print ou d'une conversion en str"""
        i,j = 0,0
        ligne = ""
        grille = ""

        while i < self.nb_ligne:
            while j < self.nb_colonne:
                ligne += str(self[j,i])+"\t"
                j += 1
            j = 0
            i += 1
            grille += ligne + "\n"
            ligne = ""

        return grille

    def __eq__(self, other):
        """Action effectuée lors d'un test d'égalité du type a==b"""
        if isinstance(other, self.__class__) and len(self.items())==len(other.items()):
            for (i,j) in self.keys():
                if self[i,j] != other[i,j]:
                    return False
            return True
        else:
            return False

    def __ne__(self, other):
        """Action effectuée lors d'un test d'ingalité du type a!=b"""
        return not self.__eq__(other)


    ############################################################################ Générateurs ############################################################################

    def keys(self):
        """Retourne un générateur sur les clés du dictionnaire"""
        return self._grid.keys()

    def items(self):
        """Retourne un générateur sur (clés, values) du dictionnaire """    
        return self._grid.items()

    def values(self):
        """Retourne un générateur sur les valeurs du dictionnaire """   
        return self._grid.values()



    def colonneIndices(self, x,y):
        #Explore le bas de la colonne
        i = 1
        continuer = True
        while continuer:
            if y+i >= self.nb_ligne:
                continuer = False
                
            elif (x, y+i) not in self.keys():
                continuer = False
                
            elif type(self[x,y+i]) in (cases.Indicatrice, cases.CaseNoire): 
                continuer = False
                
            else:
                yield x, y+i
                i += 1
        # Explore le haut de la colonne     
        i = 1
        continuer = True
        while continuer:
            if y-i <0:
                continuer = False
                
            elif (x, y-i) not in self.keys():
                continuer = False
                
            elif type(self[x,y-i]) in (cases.Indicatrice, cases.CaseNoire): 
                continuer = False
                
            else:
                yield x, y-i
                i += 1
     


    def colonne(self, x, y):
        """Retourne un générateur sur l'ensemble des CasesVides de la plage colonne à laquelle la case appartient"""
        #Explore le bas de la colonne
        for indices in self.colonneIndices(x,y):
            yield self[indices]

    def ligneIndices(self, x, y):
        """Retourne un générateur sur l'ensemble des valeurs de la plage ligne à laquelle la case appartient"""
        #Explore la gauche de la ligne
        i = 1 
        continuer = True
        while continuer:
            if x+i >= self.nb_colonne:
                continuer = False
                
            elif (x+i, y) not in self.keys():
                continuer = False
                
            elif type(self[x+i,y]) in (cases.Indicatrice, cases.CaseNoire): 
                continuer = False
            else:
                yield x+i, y
                i += 1
        # Explore la droite de la ligne    
        i = 1
        continuer = True
        while continuer:
            if x-i < 0:
                continuer = False
                
            elif (x-i, y) not in self.keys():
                continuer = False
                
            elif type(self[x-i,y]) in (cases.Indicatrice, cases.CaseNoire): 
                continuer = False
                
            else:
                yield x-i, y
                i += 1
    
    
    def ligne(self, x, y):
        """Retourne un générateur sur l'ensemble des valeurs de la plage ligne à laquelle la case appartient"""
        for indices in self.ligneIndices(x,y):
            yield self[indices]
        

    @staticmethod
    def cases_to_valeur_saisie(generateur):
        """convertit un generateur de cases en generateur de valeur_saisie"""
        for elem in generateur:
            yield elem.valeur_saisie

    
    @staticmethod
    def cases_to_solution(generateur):
        """ Convertit un générateur de cases vides en générateur de _solution_case """
        for elem in generateur:
            yield elem._solution_case



    ######################################################### Génération de grille ################################################################



    # Méthode principale
    def generer_grille(self, difficulte):
        """ Fonction générale permettant de creer aléatoirement une grille selon un niveau de difficulté passé en paramètre """
        
        #ce qui varie d'une difficulté à l'autre est le nombre d'indicatrices
        if difficulte == "facile":
            nb_indicatrice = NB_INDICATRICE_FACILE
        elif difficulte == "moyen":
            nb_indicatrice = NB_INDICATRICE_MOYEN
        elif difficulte == "difficile" :
            nb_indicatrice = NB_INDICATRICE_DIFFICILE
        else:
            nb_indicatrice = NB_INDICATRICE_MDFT
            
        self._creer_structure(nb_indicatrice)
        self._placer_indicatrices(nb_indicatrice)
        self._placer_valeurs()
        self.noircir()
        self.somme_indicatrices()
        self.solved = True

        
    # Création de la structure
    
    def _creer_structure(self, nb_indicatrice):
        """ Cette méthode a pour but de creer la structure de la grille.
            Elle parcourt la première ligne et la première colonne du tableau et définit une indicatrice et un décalage (entre 0 et 2).
            Elle assigne une indicatrice a cette case (en fonction du décalage) et remplit le trou entre le bord et l'indicatrice par des cases noires.
        """
        
      # on remplit la ligne du haut d'indicatrices a un random près (certaines ne seront pas tout a fait sur la ligne du haut)
        i = 0 
        while i < self.nb_colonne:
            offset = random.choice(range(0,2))
            self[i,offset] = cases.Indicatrice()
           
            j=0
            while j<offset:
                self[i,j] = cases.CaseNoire()
                j += 1

            nb_indicatrice -= 1
            i += 1
      # on remplit la colonne de gauche d'indicatrices a un random près (certaines ne seront pas tout a fait sur la colonne de gauche)
        i=0
        while i < self.nb_ligne:
            offset = random.choice(range(0,2))
            self[offset,i] = cases.Indicatrice()

            j=0
            while j<offset:
                self[j,i] = cases.CaseNoire()
                j += 1

            nb_indicatrice -= 1
            i += 1
            


    def _placer_indicatrices(self, nb_indicatrice):
        """ Cette méthode complète la structure en ajoutant un nombre d'indicatrice a des positions aléatoires du tableau.
            Une fois que l'ensemble des indicatrices ont été placées, la méthode remplace toutes les indicatrices bloquées par un case noire.
        """
         
        # placage des indicatrices supplémentaires
        i=0
        while i<nb_indicatrice:
            # Choisit une case au hasard
            x,y = random.choice(range(1,self.nb_colonne)),random.choice(range(1,self.nb_ligne))
            self[x,y] = cases.Indicatrice()
            i+=1

        # on remplace les indicatrices bloquees par des cases noires
        for (i,j) in self.keys():
            if self.blocked(i,j):
                self[i,j] = cases.CaseNoire()



            
    def blocked(self, i, j):
        """ Determine si une case indicatrice est bloquée par d'autres cases noires ou indicatrices """
        # Seule une indicatrice peut être bloquée
        if type(self[i,j]) is cases.Indicatrice:
            
            blocked_bas, blocked_droite = False, False
            
            # Verifie si la case est bloquée à droite
            if (i <= self.nb_colonne-2 and (i+1,j) in self.keys()  and type(self[i+1,j]) is not cases.CaseVide) or i == self.nb_colonne-1:
                blocked_droite = True
                
            # Verifie si la case est bloquée en-dessous
            if (j <= self.nb_ligne-2 and (i,j+1) in self.keys() and type(self[i,j+1]) is not cases.CaseVide) or j == self.nb_ligne-1:
                blocked_bas = True

            return (blocked_bas and blocked_droite)

        return False
                   



    # Placement des valeurs
    def _placer_valeurs(self):
        """ Affecte toutes les valeurs solution aux cases blanches, en fonction des valeurs déja affectées aux autres cases du bloc.
            Cette méthoe appelle choix_valeur, qui permet de selectionner une valeur n'étant ni dans la ligne, ni dans la colonne.
        """
        i,j=0,0
        while i<self.nb_colonne:
            while j<self.nb_ligne:
                if (i,j) not in self.keys():
                    self.choix_valeur(i,j)
                j+=1
            j=0
            i+=1



    def choix_valeur(self, x, y):
        """ Affecte une valeur a une case, cette valeur est unique, comprise entre 1 et 9 et ne se retrouve dans aucune
            plage a laquelle la case appartient

            Si la case peut prendre une valeur, lui affecte et retourne cette valeur.
            Sinon la case devient une indicatrice et la methode retourne -1.
            Le fait qu'elle devienne une indicatrice implique que de nouvelles indicatrices peuvent être bloquées.
        """
        
        domaine = list(range(1,10))
        
        valeur_possible = []
        for val in domaine:
            dispo = True
            for  el in self.ligne(x,y):
                if el._solution_case == val:
                    dispo = False
            for el in self.colonne(x,y):
                if el._solution_case == val:
                    dispo = False
            if dispo:
                valeur_possible.append(val)
                

        # Si il n'y a aucun choix possible, créée une indicatrice, l'initialise, retourne -1
        if len(valeur_possible) == 0:
            self[x,y] = cases.Indicatrice()
            return -1
        
        # Sinon, choisit une valeur, l'affecte a la case et retourne cette valeur            
        else:
            valeur = random.choice(valeur_possible)
            self[x,y] = cases.CaseVide(valeur)
            return valeur            



    def somme_indicatrices(self):
        """ Initialise les valeurs de chaque indicatrice en fonction des valeurs de ses plages.
            Pour chaque indicatrice elle sommes les valeurs de sa plage droite et l'affecte a son attribut valeur_droite.
            Elle effectue le même comportement pour sa plage bas.
        """
        somme_droite = 0
        somme_bas = 0

        for(i,j) in self.keys():
            if type(self[i,j]) is cases.Indicatrice:
                
                # Si l'indicatrice a une plage droite
                if (i+1, j) in self.keys() and type(self[i+1,j]) is cases.CaseVide:
                    somme_droite += self[i+1, j]._solution_case # ligne() ne prend pas l'élément sur lequel il est appelé
                    for el in self.ligne(i+1,j):
                        somme_droite += el._solution_case
                        
                # Si l'indicatrice a une plage gauche
                if (i,j+1) in self.keys() and type(self[i,j+1]) is cases.CaseVide:
                    somme_bas += self[i, j+1]._solution_case  # colonne() ne prend pas l'élément sur lequel il est appelé
                    for el in self.colonne(i,j+1):
                        somme_bas += el._solution_case
                    
                self[i,j].valeur_droite = somme_droite
                self[i,j].valeur_bas = somme_bas
                somme_droite = 0
                somme_bas = 0
  
                
    # Finition 
    def noircir(self):
        """ Une fois que la grille a été créée, des indicatrices bloquées ont pu réapparaitre, lors du choix des valeurs.
            Cette méthode verifie qu'aucune indicatrice bloquée est apparue. Si c'est le cas elle la transforme en case noire
        """
        for (i,j) in self.keys():
            if self.blocked(i,j):
                self[i,j] = cases.CaseNoire()
             



    ################################################################ Jeu d'une grille ##############################################################################


    ## Affichage de la grille ## 

    def afficher_grille(self, fenetre):
        """ Permet d'afficher la grille sur la fenêtre.
            Son seul paramètre est la fenêtre d'affichage.
            Il demarre l'affichage suivant la constantes POSITION_GRILLE.
            Il parcourt l'ensemble de la grille. 
            Pour les cases vides et indicatrices, il lance leur méthode afficher_valeur, permettant d'afficher la case et les valeurs correspondantes.
            Il décale chaque case suivant la constante COTE_CASE.
        """
        pygame.freetype.init()
       
        # Chargement des images des cases
        img_indicatrice = pygame.image.load(CHEMIN_IMAGE_INDICATRICE).convert()
        img_case_noire = pygame.image.load(CHEMIN_IMAGE_CASENOIRE).convert()
        img_case_vide = pygame.image.load(CHEMIN_IMAGE_CASEVIDE).convert()

        # Générateur de texte
        font_indicatrice = pygame.freetype.Font(CHEMIN_FICHIER_POLICE, TAILLE_POLICE_INDICATRICE)
        font_casevide = pygame.freetype.Font(CHEMIN_FICHIER_POLICE, TAILLE_POLICE_CASEVIDE)
        
        i, j = 0,0
        # Positionnement de la grille
        pos_x, pos_y = POSITION_GRILLE

        while i < self.nb_colonne:
            while j < self.nb_ligne :

                if type(self[i,j]) == cases.Indicatrice:
                    self[i,j].affichage(fenetre, font_indicatrice, (pos_x,pos_y), img_indicatrice)
                                        
                elif type(self[i,j]) == cases.CaseVide:
                    self[i,j].affichage(fenetre, font_casevide, (pos_x, pos_y), img_case_vide)
                                           
                else:
                    fenetre.blit(img_case_noire, (pos_x, pos_y))
                    self[i,j].rect = pygame.Rect(pos_x,pos_y, COTE_IMAGE_CASE, COTE_IMAGE_CASE)
                    
                j += 1
                pos_y += COTE_IMAGE_CASE
            j = 0
            pos_y = POSITION_GRILLE[1]
            i += 1
            pos_x += COTE_IMAGE_CASE


    def validate(self, solving=False):
        """ Cette méthode Verifie si la grille a une erreur.

            Elle verifie que la grille n'a pas de doublon ou de somme incorrecte. 
            Si la grille a un doublon, une DoublonException est levée.
            Si la grille a une somme incorrecte, une SommeIncorrecteException est levée.
            Si la grille a un doublon et une somme incorrecte, une ExceptionMixte est levée.

            Si aucune exception n'est levée, la méthode victoire est lancée, verifiant si le jeu est fini.
        """

        doublon, somme_fausse = False, False
        
        for (i,j) in self.keys():
            # on a le droit parce que case_courante est une reference
            case_courante = self[i,j]
            
            if type(case_courante)==cases.CaseVide:
                case_courante.erreur = False
                if self.has_doublon(i,j):
                    case_courante.erreur=True
                    doublon = True

            elif type(case_courante)==cases.Indicatrice:
                case_courante.erreur_bas, case_courante.erreur_droite = False, False
                erreur = self.has_fausse_somme(i,j)

                if solving:
                    unfinished_error = self.has_inconsistent_sum(i,j)
                    erreur = erreur or unfinished_error

                somme_fausse = somme_fausse or erreur

        if(doublon and somme_fausse):
            raise ExceptionMixte()
        elif doublon:
            raise DoublonException()
        elif somme_fausse:
            raise SommeIncorrecteException()
            
        return True


    def has_fausse_somme(self, i, j):
        """ Cette méthode verifie la valeur droite et basse des indicatrices en fonction des sommes des valeurs de ses plages.
            Si cette somme et la valeur de l'indicatrice ne correspondent pas, la fonction retourne True.
            Si c'est le cas pour la plage basse, l'attribut erreur_bas de l'indicatrice devient True.
            Si c'est le cas pour la plage droite, l'attribut erreur_droite de l'indicatrice devient True.
        """
        
        somme_fausse = False
        # Si elle a une plage droite
        if i < self.nb_colonne-1  and type(self[i+1, j]) is cases.CaseVide:
            # Si cette plage n'a pas de case(s) vide(s)
            if -1 not in self.cases_to_valeur_saisie(self.ligne(i+1,j)) and self[i+1,j].valeur_saisie != -1:

                # On verifie la valeur de l'indicatrice
                somme = self[i+1,j].valeur_saisie
                for el in self.ligne(i+1,j):
                    somme += el.valeur_saisie

                if somme != self[i,j].valeur_droite:
                    somme_fausse = True
                    self[i,j].erreur_droite = True
        
        # Si elle a une plage bas
        if j < self.nb_ligne-1  and type(self[i,j+1]) is cases.CaseVide:
            # Si cette plage n'a pas de case(s) vide(s)
            if -1 not in self.cases_to_valeur_saisie(self.colonne(i,j+1)) and self[i, j+1].valeur_saisie != -1:
                # On verifie la valeur de l'indicatrice

                somme = self[i, j+1].valeur_saisie
                for el in self.colonne(i,j+1):
                    somme += el.valeur_saisie
                    
                if somme != self[i,j].valeur_bas:
                    somme_fausse = True
                    self[i,j].erreur_bas = True

        return somme_fausse



    def has_inconsistent_sum(self, i, j):
        """ Retourne vrai si la les valeurs remplies de la plage de l'indicatrice ne permettent pas de remplir de manière cohérente la somme.
            params:
                i -> coordonnée i de la case indicatrice
                j -> coordonnée j de la case indicatrice
            return:
                Vrai si la somme des valeurs remplis n'est pas cohérente avec la valeur de l'indicatrice
                Faux sinon.
        """
        somme_fausse = False

        # Si elle a une plage droite
        if i < self.nb_colonne-1  and type(self[i+1, j]) is cases.CaseVide:
            # Si cette plage n'a pas de case(s) vide(s)
            if -1 in self.cases_to_valeur_saisie(self.ligne(i+1,j)) or self[i+1,j].valeur_saisie == -1:

                cpt = 0
                assigned = set()
                valeur = self[i+1,j].valeur_saisie

                ## On garde en mémoire les valeurs rencontrées et le nombre de case non remplies

                if valeur == -1:
                    cpt+=1
                    valeur = 0
                else:
                    assigned.add(valeur)
                somme = valeur

                for el in self.ligne(i+1,j):
                    valeur = el.valeur_saisie

                    if valeur == -1:
                        cpt+=1
                        valeur = 0
                    else: 
                        assigned.add(valeur)

                    somme += valeur

                # Si la somme est plus grande que ce que la solution
                if somme >= self[i,j].valeur_droite:
                    somme_fausse = True
                    self[i,j].erreur_droite = True

                # Si la somme est plus petite
                #else:
                    #maxValue = Grille.getMaxValue(cpt, assigned)
                    # Si la somme et la valeur maximale qu'on peut affecter ne suffit pas, il y a une erreur
                    #if somme + maxValue < self[i,j].valeur_droite:
                        #somme_fausse = True
                        #self[i,j].erreur_droite = True



        # Si elle a une plage bas
        if j < self.nb_ligne-1  and type(self[i,j+1]) is cases.CaseVide:
            # Si cette plage n'a pas de case(s) vide(s)
            if -1 in self.cases_to_valeur_saisie(self.colonne(i,j+1)) or self[i, j+1].valeur_saisie == -1:

                cpt = 0
                assigned = set()
                

                ## On garde en mémoire les valeurs rencontrées et le nombre de case non remplies
                valeur = self[i,j+1].valeur_saisie
                if valeur == -1:
                    cpt+=1
                    valeur = 0
                else:
                    assigned.add(valeur)
                somme = valeur

                for el in self.colonne(i,j+1):
                    valeur = el.valeur_saisie

                    if valeur == -1:
                        cpt+=1
                        valeur = 0
                    else: 
                        assigned.add(valeur)

                    somme += valeur

                # Si la somme est plus grande que ce que la solution
                if somme >= self[i,j].valeur_bas:
                    somme_fausse = True
                    self[i,j].erreur_bas = True

                # Si la somme est plus petite
                #else:
                   
                    #maxValue = Grille.getMaxValue(cpt, assigned)
                    # Si la somme et la valeur maximale qu'on peut affecter ne suffit pas, il y a une erreur
                    #if somme + maxValue < self[i,j].valeur_bas:
                        #somme_fausse = True
                        #self[i,j].erreur_bas = True


        return somme_fausse

    @staticmethod
    def getMaxValue(cpt, assigned):
        """ Returns the max value possible in cpt sum without the already assigned value possible """
        i = 0
        maxValue = 0
        # On prend la valeur max possible
        while cpt != 0:
            valeur = 9-i
            if valeur not in assigned:
                maxValue += valeur
                cpt-=1
            i+=1

        return maxValue

    def has_doublon(self, i, j):
        """ Cette méthode verifie que la valeur saisie dans la case n'existe pas déja dans cette plage """
        # Si la valeur saisie dans la case courante est deja dans la ligne ou la colonne et qu'elle ne vaut pas -1
        doublon = self[i,j].valeur_saisie in self.cases_to_valeur_saisie(self.ligne(i,j))
        doublon = doublon or self[i,j].valeur_saisie in self.cases_to_valeur_saisie(self.colonne(i,j))
        doublon = doublon and (self[i,j].valeur_saisie != -1)
        return doublon



    def reinitialiser(self):
        """ Cette méthode reinitialise la grille.
            Toutes les valeurs_saisies des cases vides sont remises à -1.
        """
        for (i,j) in self.keys():
            if type(self[i,j]) is cases.CaseVide:
                self[i,j].valeur_saisie = (-1)
                self[i,j].domaine = set(range(1,10))


    def victoire(self):
        """ Cette méthode verifie si la grille est finie.
            Elle verifie si la grille est intégralement remplie. 
            Cette fonction est lancée si validate ne releve pas d'erreur.
        """

        remplie = True
        for (i,j) in self.keys():
            if type(self[i,j]) is cases.CaseVide:
                if (self[i,j].valeur_saisie == -1):
                    remplie = False
        return remplie


    def solve(self):
        """ Cette methode donne la solution de la grille. 
            Chaque case vide se voit affecter à sa valeur_saisie la solution_case définie lors de la création de la grille.
        """
        for (i,j) in self.keys():
            if type(self[i,j]) is cases.CaseVide:
                self[i,j].valeur_saisie = self[i,j]._solution_case
                self[i,j].erreur = False
            elif type(self[i,j]) is cases.Indicatrice:
                self[i,j].erreur_bas = False
                self[i,j].erreur_droite=  False


############################################################ EDITEUR ###############################################################################


    def generer_grille_vide(self):
        """fonction permettant de creer une grille vide (pour l'editeur)"""
        for x in range(0,NB_COLONNE_GRILLE):
            for y in range(0,NB_LIGNE_GRILLE):
                self[x,y] = cases.CaseVide(-1)

    def validate_saisie(self):
        """ Cette méthode Verifie si la grille saisie a une erreur.

            Elle verifie qu'aucune indicatrice n'est bloquée ou n'a de valeurs incorrectes.
            Si une indicatrice est bloquée, une BlockedException est levée.
            Si une indicatrice a une valeur incorrecte, une ValeurIncorrecteException est levée.
            Si les deux cas sont avérés, une ExceptionMixte est levée.
        """
        blocked, valeur_fausse = False, False
        
        for (i,j) in self.keys():
            # on a le droit parce que case_courante est une reference
            case_courante = self[i,j]

            if type(case_courante)==cases.Indicatrice:
                case_courante.erreur_droite = case_courante.erreur_bas = False
                erreur = self.has_fausse_valeur(i,j)
                valeur_fausse = valeur_fausse or erreur
                if self.blocked(i,j):
                    blocked = True
                    self[i,j].erreur_droite = self[i,j].erreur_bas = True
                

        if(blocked and valeur_fausse):
            raise ExceptionMixte(MESSAGE_ERREUR_MIXTE_SAISIE)
        elif blocked:
            raise BlockedException()
        elif valeur_fausse:
            raise ValeurIncorrecteException()



    def has_fausse_valeur(self, i, j):
        """ Cette méthode verifie la valeur droite et basse des indicatrices. 
            Si l'une des deux valeurs est inférieures a sa valeur minimale théorique ou supérieure à sa valeur maximale théorique, la méthode renvoie true.
        """
        # Plage droite
        if i < self.nb_colonne-1 and type(self[i+1,j]) is cases.CaseVide:
            min = self.valeur_min(self.longueur(self.ligne(i+1,j)) +1)
            max = self.valeur_max(self.longueur(self.ligne(i+1,j)) +1)
            if self[i,j].valeur_droite < min or self[i,j].valeur_droite > max:
                self[i,j].erreur_droite = True
        else:
            if self[i,j].valeur_droite:
                self[i,j].erreur_droite = True

        # Plage droite
        if j <self.nb_ligne-1 and type(self[i, j+1]) is cases.CaseVide:
            min = self.valeur_min(self.longueur(self.colonne(i,j+1)) +1)
            max = self.valeur_max(self.longueur(self.colonne(i,j+1)) +1)
            if self[i,j].valeur_bas < min or self[i,j].valeur_bas > max:
                self[i,j].erreur_bas = True
        else:
            if self[i,j].valeur_bas:
                self[i,j].erreur_bas = True

        erreur = self[i,j].erreur_droite or self[i,j].erreur_bas

        return erreur

    @staticmethod
    def longueur(generateur):
        """ Méthode retournant la longueur d'un générateur """
        i = 0
        for el in generateur:
            i += 1
        return i

    @staticmethod
    def valeur_max(longueur):
        """ Méthode retournant la valeur maximale d'une somme sur une longueur sans doublon """
        somme = 0
        i = VALEUR_MAX
        while i>VALEUR_MAX-longueur:
            somme += i
            i -= 1
        return somme

    @staticmethod
    def valeur_min(longueur):
        """ Méthode retournant la valeur minimale d'une somme sur un nombre d'élément ne comportant pas de doublons """
        somme = 0
        i = VALEUR_MIN
        while i <= longueur:
            somme += i
            i += 1
        return somme



    ############################################################# SAUVEGARDE ####################################################################################################

    def sauvegarde(self, chemin_fichier):
        """ Permet de sauvegarder la grille dans un fichier binaire, dont le chemin est chemin_fichier """
        with open(chemin_fichier, "wb") as fichier:
            pickler = pickle.Pickler(fichier)
            pickler.dump(self._grid)

    def chargement(self, chemin_fichier):
        """ Permet de charger une grille depuis un fichier binaire dont le chemin est cemin_fichier """
        with open(chemin_fichier, "rb") as fichier:
            depickler = pickle.Unpickler(fichier)
            self._grid = depickler.load()

    def is_solved(self):
        """ Méthode permettant de verifier si une grille a une solution calculée. 
            Elle parcourt la grille. Si une case vide a un attribut _solution_case a -1, la grille n'a pas de solution.
        """
        for (i,j) in self.keys():
            if type(self[i,j]) is cases.CaseVide and self[i,j]._solution_case == -1:
                return False
        return True

    ############################################################# SOLVEUR ############################################################################################




    @staticmethod
    def get_domaine(valeur, longueur):
        """ Méthode permettant d'avoir toutes les combinaisons de chiffres possibles sur la longueur dont la somme donne la valeur passée en argument. 
            Cette méthode retourne un set, contenant l'ensemble des valeurs possibles.

            On initialise un tableau contenant la division entiere de la valeur par longueur pour les premieres cases sauf la derniere, qui elle contient le reste en plus.
            La somme de chaque case du tableau retourne donc la valeur.

            Le domaine est retourné à la fin de l'itération.
        """

        tab = list(range(1, longueur+1))
        valeurs_possibles = list()
        continuer = True


        i = longueur - 1
        # Calcul des valeurs possibles
        while continuer:
            while tab[i] < 10:
                somme = 0
                stop = False
                # Calcul la somme des éléments
                for el in tab:
                    somme += el

                # Si la somme est égale à la valeur et qu'il n'y a pas de doublons
                if somme == valeur and len(tab) == len(set(tab)):
                    ## On peut faire un truc style
                    result = list(tab)
                    result.sort()
                    if result not in valeurs_possibles:
                        valeurs_possibles.append(result)
                    # on a alors la combinaison des sommes
                    ## On peut utiliser cette information après pour réduire les domaines
                    
                    # Si une somme passe on peut arreter et incrémenter la valeur suivante
                    tab[i] = 9
                tab[i] += 1

            # Tant que la cases courante est a 10
            while tab[i] == 10 and i >= 0:
                # On lui redonne sa valeur initiale
                tab[i] = i + 1
                # On passe a la case précédente
                i -= 1
                # On l'incrémente
                tab[i] += 1
                # On a testé toutes les valeurs
                if (i == 0 and tab[i] == 10) or i<0:
                    continuer = False
            i = longueur - 1


        return valeurs_possibles


    def confirmer_solution(self):
        """ Une fois qu'une solution a été calculée et est correcte elle est confirmée.
            L'ensemble des valeurs saisies est transféré vers les solutions pour permettre le jeu de la grille.
        """
        for (i,j) in self.keys():
            if type(self[i,j]) is cases.CaseVide:
                self[i,j]._solution_case = self[i,j].valeur_saisie
                self[i,j].valeur_saisie = -1
    

    def get_indicatrices(self, i, j):
        """ Méthode permettant de verifier qu'une case vide appartient bien à une plage et dépend bien d'une indicatrice.
            Le haut et la gauche de la plage à laquelle elle appartient sont parcourus.
            Si une indicatrice est trouvée, dans l'une de ces directions, la méthode retourne True. 
        """

        indicatrice_bas = None
        indicatrice_droite = None

        # Parcours de la plage droite
        indice_ligne = j
        while indice_ligne > 0 and type(self[i, indice_ligne]) is cases.CaseVide:
            indice_ligne -= 1
            if type(self[i, indice_ligne]) is cases.Indicatrice:
                indicatrice_bas = self[i, indice_ligne]
            

        # Parcours de la plage bas
        indice_colonne = i
        while indice_colonne > 0 and type(self[indice_colonne, j]) is cases.CaseVide:
            indice_colonne -= 1
            if type(self[indice_colonne, j]) is cases.Indicatrice:
                indicatrice_droite = self[indice_colonne, j]

        return indicatrice_bas, indicatrice_droite


    def initDegre(self):
        """ Initialise le degré de toutes les cases vides """
        for (i,j) in self.keys():
            if type(self[i,j]) is cases.CaseVide:
                self[i,j].degre = self.longueur(self.ligne(i,j)) + self.longueur(self.colonne(i,j))


    def getEmptySquares(self):
        """ Retourne la liste des cases vides.
            return:
                la liste des cases vides
        """
        result = []
        for (i,j) in self.keys():
            if type(self[i,j]) is cases.CaseVide and self[i,j].valeur_saisie == -1:
                result.append(((i,j),self[i,j]))
        return result


    def getNextSquareUsingHeuristics(self):
        """ Retourne la prochaine case vide de la grille ayant le moins de valeur possibles et le degré de contraintes le plus élevé. """
        result = self.getEmptySquares()
        result.sort(key= lambda case: case[1].degre, reverse=True)
        result.sort(key= lambda case: len(case[1].domaine))
        return result[0]

    def forwardChecking(self, i, j):
        """ Implémentation de la recherche en avant. 
            Retire la valeur saisie actuelle des domaines de toutes les cases de la ligne et de la colonne de la case considérée.
            Retire ensuite l'ensemble des combinaisons de sommes des indicatrices correspondantes ne contenant pas la valeur choisie.
        """
        valeur = self[i,j].valeur_saisie

        # On retire cette valeur des valeurs possibles de chaque case de la plage
        for square in self.ligne(i,j):
            if valeur in square.domaine:
                square.domaine.remove(valeur)

        for square in self.colonne(i,j):
            if valeur in square.domaine:
                square.domaine.remove(valeur)

        indicatrice_bas, indicatrice_droite = self.get_indicatrices(i,j)

        if indicatrice_bas != None:
            indicatrice_bas.domaine_bas = [comb for comb in indicatrice_bas.domaine_bas if valeur in comb]
        if indicatrice_droite != None:
            indicatrice_droite.domaine_droite = [comb for comb in indicatrice_droite.domaine_droite if valeur in comb]


    def checkDomain(self, i, j):
        square = self[i,j]                
        indic_bas, indic_droite = sellf._grille.get_indicatrices(i,j)
        domaine = list(square.domaine)

        i = 0
        for valeur in domaine:
            values = [nb for comb in indic_bas.domaine for nb in comb]
            values += [nb for comb in indic_droit.domaine for nb in comb]
            values = set(values)

            if valeur not in value:
                square.domaine.remove(valeur)

               





        
if __name__ == "__main__":
    """ En executant ce fichier, une grille générée est affichée, permettant de verifier la viabilité de la génération de grille."""
    continuer = True
    while continuer:
        
        test = Grille()
        difficulte = input("Choisissez votre niveau de difficulté (facile/moyen/difficile/mdft) : ").lower()
        test.generer_grille(difficulte)  

        print("Grille générée:")
        print(test)
        
        continuer = input("Voulez-vous continuez (y/n)? ").lower()
        if continuer == "n":
            continuer = False