# tests/test_feature_engineering.py
import sys
import os

# Ajoute le dossier parent au chemin
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import data_manager
import feature_engineering

def test_calculer_stats_tirage():
    """Vérifie le calcul des statistiques de base d'un tirage."""
    # ARRANGE
    tirage_test = data_manager.Tirage("date", [1, 2, 3, 4, 10], [1, 2])
    
    # ACT
    stats = feature_engineering.calculer_stats_tirage(tirage_test)
    
    # ASSERT
    assert stats['somme_numeros'] == 20
    assert stats['moyenne_numeros'] == 4.0
    assert stats['nb_pairs'] == 3 # (2, 4, 10)
    assert stats['nb_impairs'] == 2 # (1, 3)