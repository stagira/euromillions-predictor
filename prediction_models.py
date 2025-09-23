# prediction_models.py
from collections import Counter
import data_manager # On importe pour que le code connaisse la classe Tirage

def analyse_frequence(historique_tirages: list[data_manager.Tirage]):
    """
    Analyse la fréquence de sortie de chaque numéro dans l'historique.

    Args:
        historique_tirages (list): Une liste d'objets Tirage.

    Returns:
        list: Une liste de tuples (numero, occurrences) des 5 numéros les plus fréquents.
    """
    tous_les_numeros = []
    for tirage in historique_tirages:
        tous_les_numeros.extend(tirage.numeros)

    # Counter est un outil magique pour compter des éléments dans une liste
    frequence = Counter(tous_les_numeros)

    # .most_common(5) nous donne les 5 plus fréquents
    numeros_chauds = frequence.most_common(5)

    return numeros_chauds