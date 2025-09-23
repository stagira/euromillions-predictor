# tests/test_evaluation.py
import sys
import os
import pytest

# Ajoute le dossier parent au chemin
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import evaluation

@pytest.mark.parametrize("pred_boules, reel_boules, pred_etoiles, reel_etoiles, expected_score", [
    ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [6, 7], [6, 7], (5, 2)), # All correct
    ([1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [1, 2], [3, 4], (0, 0)), # None correct
    ([1, 2, 3, 4, 5], [1, 7, 8, 9, 10], [6, 7], [6, 8], (1, 1)), # Some correct
    ([], [], [], [], (0, 0)), # Empty lists
    ([1, 2, 3], [1, 2, 4], [5], [5, 6], (2, 1)), # Partial lists
])
def test_calculer_score(pred_boules, reel_boules, pred_etoiles, reel_etoiles, expected_score):
    """
    Vérifie que calculer_score retourne le bon nombre de correspondances.
    """
    # ACT
    score = evaluation.calculer_score(pred_boules, reel_boules, pred_etoiles, reel_etoiles)

    # ASSERT
    assert score == expected_score
