#!/usr/bin/python3
# -*- encoding: utf-8 -*

""" Module définissant les exceptions pouvant être déclenchées lors du jeu ou de la saisie d'une grille.

    Ce module contient les classes:
        - DoublonException
        - SommeIncorrecteException

        - ExceptionMixte

        - ValeurIncorrecteException
        - BlockedException

        -NoSolutionException
        -AbandonException

    Ce module importe les modules suivant:
        - constantes: utilisé dans toutes les méthodes
"""

from constantes import *


class DoublonException(Exception):
    """ Classe d'exception utilisée lors d'un doublon sur une case lors du jeu d'une grille.
        Cette classe a un unique attribut message_erreur, initialisé lors du constructeur.
    """

    def __init__(self, message=MESSAGE_ERREUR_DOUBLON):
        """ Initialise l'attribut message_erreur avec le texte défini dans le fichier constantes"""
        self.message_erreur = message

    def __str__(self):
        """ Chaine retournée lors de la conversion de l'exception en chaine, ou lorsqu'elle est en paramètre de la fonction print(). """
        return self.message_erreur


class SommeIncorrecteException(Exception):
    """ Classe d'exception utilisée lorsque la somme d'un bloc est incorrecte lors du jeu d'une grille.
        Cette classe a un unique attribut message_erreur, initialisé lors du constructeur.
    """

    def __init__(self, message=MESSAGE_ERREUR_SOMME):
        """ Initialise l'attribut message_erreur avec le texte défini dans le fichier constantes"""
        self.message_erreur = message

    def __str__(self):
        return self.message_erreur


class ExceptionMixte(Exception):
    """classe d'exception utilisée quand les deux types d'erreur précédents sont avérés simultanément"""

    def __init__(self, message=MESSAGE_ERREUR_MIXTE):
        """ Initialise le constructeur avec le texte défini dans le fichier constantes"""
        self.message_erreur = message

    def __str__(self):
        """ Chaine retournée lors de la conversion de l'exception en chaine, ou lorsqu'elle est en paramètre de la fonction print(). """
        return self.message_erreur


class ValeurIncorrecteException(Exception):
    """ Classe d'exception utilisée lorsque la valeur d'une indicatrice est incorrecte ou incohérente en fonction de la plage qui lui est associée.
         Cette classe a un unique attribut message_erreur, initialisé lors du constructeur.
    """

    def __init__(self, message=MESSAGE_ERREUR_VALEUR):
        """ Initialise le message d'erreur avec le texte défini dans les constantes """
        self.message_erreur = message

    def __str__(self):
        """ Chaine retournée lors de la conversion de l'exception en chaine, ou lorsqu'elle est en paramètre de la fonction print(). """
        return self.message_erreur


class BlockedException(Exception):
    """ Classe d'exception utilisée lorsqu'une indicatrice est bloquée par d'autres indicatrices ou cases noires.
        Cette classe a un unique attribut message_erreur, initialisé dans le constructeur.
    """

    def __init__(self, message=MESSAGE_ERREUR_BLOCKED):
        """ Initialise le message d'erreur avec le texte défini dans les constantes """
        self.message_erreur = message

    def __str__(self):
        """ Chaine retournée lorsde la conversion de l'exception en chaine, ou lorsqu'elle est en paramètre de la fonction print(). """
        return self.message_erreur


class NoSolutionException(Exception):
    """ Classe d'exception utilisée lorsque le solveur ne trouve pas de solution a une grille saisie.
        Cette classe a un unique attribut message_erreur, initialisé lors du constructeur.
    """

    def __init__(self, message=MESSAGE_ERREUR_NOSOLUTION):
        """ Initialise le message d'erreur avec le message passé en paramètre.
            Par défaut ce message est celui défini dans les constantes.
        """
        self.message_erreur = message

    def __str__(self):
        """ Chaine retournée lors de la conversion de l'exception en chaine, ou lorsqu'elle est en paramètre de la fonction print(). """
        return self.message_erreur


class AbandonException(Exception):
    """ Classe d'exception utilisée lorsque le solveur est brutalement arrêté par l'utilisateur.
        Cette classe a un unique attribut message_erreur, initialisé dans le constructeur.
    """

    def __init__(self, message=MESSAGE_ERREUR_ABANDON):
        """ Initialise le message d'erreur avec le message passé en paramètre.
            Par défaut ce message est celui défini dans les constantes.
        """
        self.message_erreur = message

    def __str__(self):
        """ Chaine retournée lors de la conversion de l'exception en chaine, ou lorsqu'elle est en paramètre de la fonction print(). """
        return self.message_erreur
