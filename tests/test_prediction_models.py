# tests/test_prediction_models.py
import sys
import os
import pandas as pd
import prediction_models
import shutil
from unittest.mock import patch
import pytest

# Ajoute le dossier parent au chemin pour que Python trouve data_manager
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import data_manager
from prediction_models import analyse_frequence

def test_analyse_frequence():
    """
    Vérifie que la fonction d'analyse de fréquence compte et classe correctement les numéros.
    """
    # 1. Préparation : On crée une liste de faux tirages
    # Le numéro 7 devrait être le plus fréquent (3 fois)
    tirage1 = data_manager.Tirage("date1", [1, 2, 3, 4, 7], [1, 2])
    tirage2 = data_manager.Tirage("date2", [5, 6, 7, 8, 9], [3, 4])
    tirage3 = data_manager.Tirage("date3", [10, 11, 12, 13, 7], [5, 6])
    historique_test = [tirage1, tirage2, tirage3]
    # 2. Action : On appelle la fonction à tester
    resultat = analyse_frequence(historique_test)
    # 3. Vérification : On s'assure que le résultat est celui attendu
    assert len(resultat) > 0
    assert resultat[0][0] == 7
    assert resultat[0][1] == 3

def test_preparation_donnees_anti_fuite():
    """
    TEST DE SÉCURITÉ : Vérifie que les données d'entraînement (X) sont bien
    antérieures aux données cibles (y) pour éviter toute fuite du futur.
    """
    # ARRANGE
    t3 = data_manager.Tirage(date="d3", numeros=[3,3,3,3,3], etoiles=[3,3])
    t2 = data_manager.Tirage(date="d2", numeros=[2,2,2,2,2], etoiles=[2,2])
    t1 = data_manager.Tirage(date="d1", numeros=[1,1,1,1,1], etoiles=[1,1])
    historique_test = [t3, t2, t1]
    # ACT
    modele_test = prediction_models.ComiteDeModelesML()
    X, y_df = modele_test._preparer_donnees(historique_test)
    # ASSERT
    ligne_X_attendue = [3,3,3,3,3,3,3]
    ligne_y_attendue = [2,2,2,2,2,2,2]
    assert X.iloc[0].tolist()[:7] == ligne_X_attendue
    assert y_df.iloc[0].tolist()[:7] == ligne_y_attendue

def test_comite_creation_cache_dir():
    """Vérifie que le dossier de cache est créé s'il n'existe pas."""
    # ARRANGE
    cache_dir = 'model_cache'
    if os.path.exists(cache_dir):
        shutil.rmtree(cache_dir)
    # ACT
    prediction_models.ComiteDeModelesML()
    # ASSERT
    assert os.path.exists(cache_dir)
    shutil.rmtree(cache_dir)

def test_comite_entrainer_sans_cache():
    """Vérifie que l'entraînement fonctionne correctement sans utiliser le cache."""
    # ARRANGE
    cache_dir = 'model_cache'
    if os.path.exists(cache_dir):
        shutil.rmtree(cache_dir)
    historique_test = [
        data_manager.Tirage("d1", [1,2,3,4,5], [1,2]),
        data_manager.Tirage("d2", [6,7,8,9,10], [3,4]),
        data_manager.Tirage("d3", [11,12,13,14,15], [5,6]),
    ]
    modele = prediction_models.ComiteDeModelesML()
    # ACT
    modele.entrainer(historique_test)
    # ASSERT
    assert modele.est_entraine
    assert len(os.listdir(cache_dir)) > 0
    shutil.rmtree(cache_dir)

def test_comite_entrainer_avec_cache():
    """Vérifie que l'entraînement charge les modèles depuis le cache s'il existe."""
    # ARRANGE
    cache_dir = 'model_cache'
    if os.path.exists(cache_dir):
        shutil.rmtree(cache_dir)
    historique_test = [
        data_manager.Tirage("d1", [1,2,3,4,5], [1,2]),
        data_manager.Tirage("d2", [6,7,8,9,10], [3,4]),
        data_manager.Tirage("d3", [11,12,13,14,15], [5,6]),
    ]
    modele1 = prediction_models.ComiteDeModelesML()
    modele1.entrainer(historique_test)

    # ACT
    modele2 = prediction_models.ComiteDeModelesML()
    with patch('joblib.load') as mock_load:
        modele2.entrainer(historique_test)
        # ASSERT
        mock_load.assert_called_once()
    shutil.rmtree(cache_dir)

def test_comite_predire():
    """Vérifie que la prédiction retourne des résultats dans le bon format."""
    # ARRANGE
    cache_dir = 'model_cache'
    if os.path.exists(cache_dir):
        shutil.rmtree(cache_dir)
    historique_test = [
        data_manager.Tirage("d1", [1,2,3,4,5], [1,2]),
        data_manager.Tirage("d2", [6,7,8,9,10], [3,4]),
        data_manager.Tirage("d3", [11,12,13,14,15], [5,6]),
        data_manager.Tirage("d4", [16,17,18,19,20], [7,8]),
    ]
    dernier_tirage = historique_test[0]
    historique_passe = historique_test[1:]
    modele = prediction_models.ComiteDeModelesML()
    modele.entrainer(historique_test)
    # ACT
    pred_boules, pred_etoiles = modele.predire(dernier_tirage, historique_passe)
    # ASSERT
    assert isinstance(pred_boules, list)
    assert len(pred_boules) == 5
    assert all(isinstance(n, int) for n in pred_boules)
    assert isinstance(pred_etoiles, list)
    assert len(pred_etoiles) == 2
    assert all(isinstance(e, int) for e in pred_etoiles)
    shutil.rmtree(cache_dir)

def test_comite_predire_sans_entrainement():
    """Vérifie qu'une exception est levée si on prédit sans entraînement."""
    # ARRANGE
    cache_dir = 'model_cache'
    if os.path.exists(cache_dir):
        shutil.rmtree(cache_dir)
    modele = prediction_models.ComiteDeModelesML()
    dernier_tirage = data_manager.Tirage("d1", [1,2,3,4,5], [1,2])
    historique_passe = []
    # ACT & ASSERT
    with pytest.raises(Exception, match="Le modèle doit être entraîné"):
        modele.predire(dernier_tirage, historique_passe)
    shutil.rmtree(cache_dir)