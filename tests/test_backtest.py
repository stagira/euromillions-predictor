# tests/test_backtest.py
import sys
import os

# Ajoute le dossier parent au chemin
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import data_manager
import backtest
import prediction_models

def test_lancer_backtest_retourne_un_score():
    """
    Vérifie que lancer_backtest fonctionne avec un modèle fourni
    et retourne bien des scores numériques.
    """
    # ARRANGE
    # 1. On crée un petit historique de faux tirages
    historique_test = [
        data_manager.Tirage("d5", [5,5,5,5,5], [5,5]), # Futur à deviner
        data_manager.Tirage("d4", [4,4,4,4,4], [4,4]), # Donnée pour prédire
        data_manager.Tirage("d3", [3,3,3,3,3], [3,3]), # Donnée d'entraînement
        data_manager.Tirage("d2", [2,2,2,2,2], [2,2]), # Donnée d'entraînement
        data_manager.Tirage("d1", [1,1,1,1,1], [1,1]), # Donnée d'entraînement
    ]

    # 2. On crée un modèle "simple" pour que le test soit rapide
    # n_estimators=1 pour aller très vite
    modele_test = prediction_models.ComiteDeModelesML(n_estimators=1, max_depth=1)

    # ACT
    # On lance un backtest sur 1 seul tirage pour la vitesse
    score_b, score_e = backtest.lancer_backtest(modele_test, historique_test, nombre_de_tests=1)

    # ASSERT
    # On ne cherche pas la performance, on vérifie juste que le mécanisme fonctionne
    # et retourne bien des nombres (float ou int).
    assert isinstance(score_b, (int, float))
    assert isinstance(score_e, (int, float))
    assert score_b >= 0
    assert score_e >= 0