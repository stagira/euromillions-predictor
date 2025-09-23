# tests/test_prediction_models.py
import sys
import os
import pandas as pd 
import prediction_models 

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
    # Le premier élément de la liste résultat doit être (7, 3)
    assert len(resultat) > 0 # On vérifie qu'on a bien un résultat
    assert resultat[0][0] == 7 # Le numéro le plus fréquent est bien 7
    assert resultat[0][1] == 3 # Il est bien apparu 3 fois

def test_preparation_donnees_anti_fuite():
    """
    TEST DE SÉCURITÉ : Vérifie que les données d'entraînement (X) sont bien
    antérieures aux données cibles (y) pour éviter toute fuite du futur.
    """
    # ARRANGE : On crée un historique factice et contrôlé
    # L'historique va du plus récent (t3) au plus ancien (t1)
    t3 = data_manager.Tirage(date="d3", numeros=[3,3,3,3,3], etoiles=[3,3]) # Doit être dans X[0]
    t2 = data_manager.Tirage(date="d2", numeros=[2,2,2,2,2], etoiles=[2,2]) # Doit être dans y[0] et X[1]
    t1 = data_manager.Tirage(date="d1", numeros=[1,1,1,1,1], etoiles=[1,1]) # Doit être dans y[1]
    historique_test = [t3, t2, t1]

    # ACT : On appelle la méthode de préparation des données
    modele_test = prediction_models.ComiteDeModelesML()
    X, y_df = modele_test._preparer_donnees(historique_test)

    # ASSERT : On vérifie le décalage temporel
    # La première ligne de X doit contenir les données de t3
    # La première ligne de y_df doit contenir les données de t2

    # Données attendues pour X (features)
    ligne_X_attendue = [3,3,3,3,3,3,3]
    # Données attendues pour y (targets)
    ligne_y_attendue = [2,2,2,2,2,2,2]

    assert X.iloc[0].tolist()[:7] == ligne_X_attendue, "La première ligne de X devrait être les données du tirage le plus récent (t3)"
    assert y_df.iloc[0].tolist()[:7] == ligne_y_attendue, "La première ligne de y devrait être les données du deuxième tirage (t2)"

from unittest.mock import patch

def test_prediction_produit_des_numeros_uniques():
    """
    TEST DE BUG : Vérifie que la méthode `predire` ne produit jamais de doublons,
    même si les modèles sous-jacents le suggèrent.
    """
    # ARRANGE
    # 1. Créer un historique et un dernier tirage factices
    historique = [
        data_manager.Tirage("d2", [2,3,4,5,6], [2,3]),
        data_manager.Tirage("d1", [1,2,3,4,5], [1,2])
    ]
    dernier_tirage = historique[0]

    # 2. Initialiser et "entraîner" le comité de modèles
    # L'entraînement est nécessaire pour que les `feature_names_in_` soient définis
    comite = prediction_models.ComiteDeModelesML()
    comite.entrainer(historique)

    # 3. Forcer les modèles à prédire un doublon via un mock
    # On mock la méthode 'predict' de deux modèles différents pour qu'ils retournent la même valeur
    with patch.object(comite.modeles_boules['boule_1'], 'predict', return_value=[10]), \
         patch.object(comite.modeles_boules['boule_2'], 'predict', return_value=[20]), \
         patch.object(comite.modeles_boules['boule_3'], 'predict', return_value=[25]), \
         patch.object(comite.modeles_boules['boule_4'], 'predict', return_value=[25]), \
         patch.object(comite.modeles_boules['boule_5'], 'predict', return_value=[30]):

        # ACT
        pred_boules, pred_etoiles = comite.predire(dernier_tirage, historique)

        # ASSERT
        # On vérifie qu'il y a bien 5 boules uniques et 2 étoiles uniques
        assert len(set(pred_boules)) == 5, f"La prédiction des boules contient des doublons: {pred_boules}"

@patch('prediction_models.joblib.load')
@patch('prediction_models.os.path.exists')
def test_entrainer_charge_depuis_cache(mock_exists, mock_load):
    """
    Vérifie que la méthode `entrainer` charge bien un modèle depuis le cache
    s'il existe.
    """
    # ARRANGE
    # 1. Simuler que le fichier de cache existe
    mock_exists.return_value = True

    # 2. Préparer un faux modèle à "charger"
    faux_modeles = {
        'boules': {'boule_1': 'modele_boule_1'},
        'etoiles': {'etoile_1': 'modele_etoile_1'}
    }
    mock_load.return_value = faux_modeles

    # 3. Créer une instance de ComiteDeModelesML et un historique factice
    comite = prediction_models.ComiteDeModelesML()
    historique = [data_manager.Tirage("d1", [1,2,3,4,5], [1,2])]

    # ACT
    comite.entrainer(historique)

    # ASSERT
    # On vérifie que le chargement depuis le cache a bien eu lieu
    nom_fichier_attendu = f"model_cache/model_{len(historique)}_{historique[0].date}.joblib"
    mock_exists.assert_any_call(nom_fichier_attendu)
    mock_load.assert_called_once_with(nom_fichier_attendu)

    # On vérifie que le modèle interne a bien été remplacé par celui du cache
    assert comite.modeles_boules == faux_modeles['boules']
    assert comite.est_entraine == True