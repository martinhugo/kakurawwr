#!/usr/bin/python3
# -*- encoding: utf-8 -*

""" Module principal du jeu Kakurawwr. 
    Le lancement du module provoque le lancement du produit dans son état actuel.
    Actuellement le jeu est entièrement fonctionnel.
"""

import pygame
from pygame.locals import *
import menu
from constantes import *

pygame.init()

# Création de la fenêtre
fenetre = pygame.display.set_mode(TAILLE_FENETRE)
pygame.display.set_caption(TITRE_JEU)
pygame.display.set_icon(pygame.image.load(CHEMIN_IMAGE_ICONE))
fenetre.fill(COULEUR_FOND)

# curseur est un rect de 0 par 0 (un point) qui suit le curseur
curseur = pygame.Rect(pygame.mouse.get_pos(), (0, 0))

# Lancement du jeu
ecran_menu = menu.Menu(fenetre)
ecran_menu.wait_evenement()




