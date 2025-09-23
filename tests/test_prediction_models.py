# tests/test_prediction_models.py
import sys
import os

# Permet de trouver nos modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_manager import Tirage
from prediction_models import analyse_frequence

def test_analyse_frequence():
    """
    Vérifie que la fonction d'analyse de fréquence compte et classe correctement les numéros.
    """
    # 1. Préparation : On crée une liste de faux tirages
    # Le numéro 7 devrait être le plus fréquent (3 fois)
    tirage1 = Tirage("date1", [1, 2, 3, 4, 7], [1, 2])
    tirage2 = Tirage("date2", [5, 6, 7, 8, 9], [3, 4])
    tirage3 = Tirage("date3", [10, 11, 12, 13, 7], [5, 6])

    historique_test = [tirage1, tirage2, tirage3]

    # 2. Action : On appelle la fonction à tester
    resultat = analyse_frequence(historique_test)

    # 3. Vérification : On s'assure que le résultat est celui attendu
    # Le premier élément de la liste résultat doit être (7, 3)
    assert len(resultat) > 0 # On vérifie qu'on a bien un résultat
    assert resultat[0][0] == 7 # Le numéro le plus fréquent est bien 7
    assert resultat[0][1] == 3 # Il est bien apparu 3 fois