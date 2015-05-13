#!/usr/bin/python3
# -*- encoding: utf-8 -*

""" Module contenant les constantes utilisées dans l'ensemble du produit.
   Les constantes nécéssaires au développement sont dans ce module.
   Le module est divisé en plusieurs parties correspondant aux différents modules et fonctionnalités du produit.
"""

import math


###################### GENERAL ##########################

""" La partie Général contient:
         - les informations sur la fenêtre principale
         - les informations sur la police du jeu
         - les informations sur les images fréquemment utilisé au cours du jeu
"""

# Fenêtre principale
TAILLE_FENETRE = (1200,600)
COULEUR_FOND = (244,250,252)
COULEUR_FOND_CASE = (255,255,255)
TITRE_JEU = "Kakurawwr"
CHEMIN_IMAGE_ICONE = "../images/icone.png"

# Information police
CHEMIN_FICHIER_POLICE = "./calvin-regular.ttf"
COULEUR_POLICE = (0,0,0)
COULEUR_ERREUR = (255, 0, 0)

# Image
CHEMIN_IMAGE_BOUTON = "../images/bouton.png"
CHEMIN_IMAGE_ICONE = "../images/icone.png"
DECALAGE_TITRE_BOUTON_LONG = (10, 30)
DECALAGE_TITRE_BOUTON_COURT = (35, 30)

TITRE_BOUTON_MENU = "Menu"
TITRE_BOUTON_RETOUR = "Retour"
POSITION_BOUTON_RETOUR = (15, 15)




######################## TESTS UNITAIRES ########################
""" La partie Tests unitaires contient les valeurs pouvant servir aux tests unitaires graphiques. """

TAILLE_FENETRE_TEST = (50,50)
POSITION_IMAGE_TEST = (25,25)




########################## MENU ##########################
""" La partie Menu contient:
     - les informations sur les images du menu
     - les informations sur les titres des boutons
     - les informations sur les positions des éléments.
"""

CHEMIN_IMAGE_KAKURAWWR = "../images/titre.png"
POSITION_IMG_KAKURAWWR = (250, 0)

# Titres boutons
TITRE_BOUTON_JOUER = "Jouer"
TITRE_BOUTON_CHARGER = "Charger"
TITRE_BOUTON_EDITEUR = "Editeur"

# Position
POSITION_BOUTON_JOUER = (500, 200)
POSITION_BOUTON_CHARGER = (500, 300)
POSITION_BOUTON_EDITEUR = (500, 400)




########################## GENERATION ##########################
""" La partie Generation contient:
     - les informations sur les titres des boutons
     - les informations sur les positions des éléments.
"""

# Titres boutons
TITRE_BOUTON_FACILE = "Facile"
TITRE_BOUTON_MOYEN = "Moyen"
TITRE_BOUTON_DIFFICILE = "Difficile"
TITRE_BOUTON_MDFT = "FLAN"

# Position
POSITION_BOUTON_FACILE = (500, 100)
POSITION_BOUTON_MOYEN = (500, 200)
POSITION_BOUTON_DIFFICILE= (500, 300)
POSITION_BOUTON_MDFT = (500, 400)





########################## BOUTONS #########################
""" La partie Bouton contient les informations nécéssaires à l'affiche centré des erreurs à l'écran. """

ERREUR_POSITION_Y = 550
ERREUR_POSITION_DEPART = 500
FACTEUR_DECALAGE_ERREUR = 3.8






########################## JEU ##########################

""" La partie Jeu contient:
     - les informations sur les images du jeu
     - les informations sur les grilles jouables
     - les informations sur les polices utilisées dans cet écran

"""
## Images ##

# Chemin
CHEMIN_IMAGE_INDICATRICE = "../images/indicatrice.png"
CHEMIN_IMAGE_CASEVIDE = "../images/case_vide.png"
CHEMIN_IMAGE_CASENOIRE = "../images/case_noire.png"
CHEMIN_IMAGE_BOUTON_JEU = "../images/bouton.png"
CHEMIN_IMAGE_BARRE_ERREUR = "../images/barre_erreur.png"

# Dimension
COTE_IMAGE_CASE = 50

# Position
POSITION_GRILLE = (350, 15)
POSITION_BOUTON_SAUVEGARDE = (1035, 15)
POSITION_BOUTON_IMPRESSION = (1035, 110)
POSITION_BOUTON_RESET = (15, 510)
POSITION_BOUTON_SOLUTION = (1035, 510)



DECALAGE_INDICATRICE_VALDROITE = (25,5)
DECALAGE_INDICATRICE_VALBAS = (5,25)
DECALAGE_SAISIE_CASE_VIDE = (10, 10)

# Titre bouton
TITRE_BOUTON_SAUVEGARDE = "Sauvegarde"
TITRE_BOUTON_IMPRESSION = "Impression"
TITRE_BOUTON_RECOMMENCER = "Reset"
TITRE_BOUTON_SOLUTION = "Solution"


## Information annexe ##

# Niveau de difficulté
NB_INDICATRICE_FACILE = 40
NB_INDICATRICE_MOYEN = 30
NB_INDICATRICE_DIFFICILE = 20
NB_INDICATRICE_MDFT = 10


# Police
TAILLE_POLICE_INDICATRICE = 20
TAILLE_POLICE_CASEVIDE = 45
TAILLE_POLICE_BOUTON = 17
TAILLE_TITRE_COURT = 8
TAILLE_POLICE_CASEVIDE = 45

# Dimension grille
NB_LIGNE_GRILLE = 10
NB_COLONNE_GRILLE = 10








################ SOLUTIONS ####################
""" La partie Solution contient:
        - les informations sur les messages affichées à l'écran
        - les informations concernant les positions des éléments.

"""

# Message
MESSAGE_VICTOIRE = "Félicitations, vous avez gagné!"
MESSAGE_DEFAITE = "Voici la solution de votre grille!"
COULEUR_MESSAGE = (0,255, 0)

# Positions
POSITION_BOUTON_MENU = (1035, 510)






############# SAUVEGARDE & CHARGEMENT ########################
""" La partie sauvegarde & chargement contient:
        - les informations sur la position des boutons
        - les informations sur la zone de Saisie
        - les informations sur les fichiers
"""

# Boutons
TITRE_BOUTON_VALIDER = "Valider"
INDICATION_SAUVEGARDE = "Nommez votre grille"
INDICATION_CHARGEMENT = "Nom de la grille à charger"
POSITION_INDICATION_SAUVEGARDE = (375, 150)
POSITION_INDICATION_CHARGEMENT = (325,150)

# Saisie
CHEMIN_IMAGE_ZONE_SAISIE = "../images/zone_saisie.png"
POSITION_ZONE_SAISIE = (300, 300)
DIMENSION_SAISIE_SAUVEGARDE = (550, 35)
DECALAGE_ZONE_SAISIE = (25,10)
COULEUR_SAISIE = (0,0,255)

# Fichier
TAILLE_NOM_FICHIER_MAX = 14
TAILLE_POLICE_SAISIE = 35
EXTENSION_FICHIER_SAUVEGARDE = ".rawr"
CHEMIN_DOSSIER_SAUVEGARDE = "../Sauvegarde/"






################ EDITEUR ####################
""" La partie Editeur contient les informations sur:
        - la position des boutons
        - le titre des boutons
        - la saisie des indicatrices
        - les options d'éditeurs
        - l'elargissement des boutons d'options

"""

# Titre boutons
TITRE_BOUTON_RESET = "Reset"
TITRE_BOUTON_VERIF = "Vérification"

# Position boutons
POSITION_BOUTON_VERIF = (1035, 410)
POSITION_BOUTON_JOUER_EDITEUR = (1035, 510)
POSITION_MODE_VIDE = (220,110)
POSITION_MODE_INDIC = (220,240)
POSITION_MODE_NOIRE = (220,370)

# Saisie
DIMENSION_SAISIE_INDICATRICE = (19, 19)
COULEUR_SAISIE_INDICATRICE = (0,0,255)

SAISIE_BAS = "bas"
SAISIE_DROITE = "droite"

MODE_SAISIE = "normal"
MODE_CASEVIDE = "casevide"
MODE_INDICATRICE = "indicatrice"
MODE_CASENOIRE = "casenoire"

# Options
CHEMIN_IMAGE_MODE_CASEVIDE = "../images/mode_case_vide.png"
CHEMIN_IMAGE_MODE_INDICATRICE = "../images/mode_indicatrice.png"
CHEMIN_IMAGE_MODE_CASENOIRE = "../images/mode_case_noire.png"

# Elargissement
FACTEUR_ZOOM=1.1
COTE_IMAGE_CASE_ENLARGED = math.sqrt(COTE_IMAGE_CASE*COTE_IMAGE_CASE*FACTEUR_ZOOM)
DIMENSIONS_IMAGE_CASE_ENLARGED = (COTE_IMAGE_CASE_ENLARGED, COTE_IMAGE_CASE_ENLARGED)

VALEUR_MIN = 1
VALEUR_MAX = 9


################# SOLVEUR ###########################
""" La partie solveur contient les informations sur:
        - Les messages affichées à l'écran
        - Le titre des boutons
        - La valeur du compteur de changement de message
"""

TABLEAU_MESSAGE = [ "Honnêtement, allez vous chercher un café.",
                    "Ca va sinon?",
                    "Oh non, pas encore!",
                    "Ah? AH? AH! Ah ben non.",
                    "Je ne suis pas un abruti!",
                    "Il fait beau dehors.",
                    "Je ne finirai JAMAIS!!",
                    "Ca suffat comme ci!",
                    "On est pas déjà passé par là?",
                    "C est la bonne valeur, j en suis sûr à 100%",
                    "TIENS, MANGE TOI CA DANS LES D- ah non.",
                    "Ah oui je vois, pas bête, pas bête du tout.. Ah, en fait si, très très bête.",
                    "Non, revenez, j y suis presque!",
                    "Vous avez du temps devant vous? Moi oui."]

MESSAGE_CALCUL = "Début du calcul de la grille"
MESSAGE_SOLVABILITE = "Verification de la solvabilité de la grille"
MESSAGE_ENSEMBLES_POSSIBLES = "Calcul des ensembles de valeurs possibles"
MESSAGE_CORRECTION_GRILLE = "Verification de la forme de la grille."
MESSAGE_GRILLE_RESOLUE = "La grille a été résolue"

TITRE_BOUTON_ABANDON = "Abandon"

VAL_CHANGEMENT_MESSAGE = 750



################# EXCEPTIONS ###################
""" La partie exception contient les informations sur l'ensemble des messages d'erreurs pouvant être affiché à l'écran """

# Erreur de jeu
MESSAGE_ERREUR_DOUBLON = "Attention, vous avez un doublon!"
MESSAGE_ERREUR_SOMME = "Attention, la valeur de la plage est incorrecte!"
MESSAGE_ERREUR_MIXTE = "Attention, vous avez un doublon et la valeur de la plage est incorrecte!"

# Erreur de saisie
MESSAGE_ERREUR_VALEUR = "Une indicatrice a une valeur incorrecte!"
MESSAGE_ERREUR_BLOCKED = "Une indicatrice est bloquée!"
MESSAGE_ERREUR_MIXTE_SAISIE = "Vous avez des valeurs incorrectes et des indicatrices bloquées!"

# Erreur de fichier
MESSAGE_ERREUR_NOM_INCORRECT = "Le nom saisi est incorrect"

# Erreur de solveur
MESSAGE_ERREUR_NOSOLUTION = "la grille ne peut être résolue!"
MESSAGE_ERREUR_ABANDON = "Vous avez abandonné la resolution!"


################## IMPRESSION #######################
CHEMIN_DOSSIER_IMPRESSION = "../Impression/"
EXTENSION_FICHIER_IMPRESSION = ".pdf"
HAUTEUR = 17
LARGEUR = 17
DECALAGE_X_DROIT = 10
DECALAGE_Y_DROIT = 6
DECALAGE_X_BAS = 4
DECALAGE_Y_BAS = 15
