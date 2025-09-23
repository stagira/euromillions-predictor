# tests/test_data_manager.py
import sys
import os
from unittest.mock import patch, Mock
import pytest

# Ajoute le dossier parent au chemin
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import data_manager

def test_creation_tirage():
    """Vérifie que les données sont correctement assignées lors de la création d'un objet Tirage."""
    date_test = "22/09/2025"
    numeros_test = [1, 2, 3, 4, 5]
    etoiles_test = [6, 7]

    mon_tirage = data_manager.Tirage(date=date_test, numeros=numeros_test, etoiles=etoiles_test)

    assert mon_tirage.date == date_test
    # On vérifie que les numéros sont bien triés
    assert mon_tirage.numeros == sorted(numeros_test)
    assert mon_tirage.etoiles == sorted(etoiles_test)

# --- NOUVEAUX TESTS AVEC MOCK ---

# On utilise @patch pour remplacer 'requests.get' par un objet magique (mock)
@patch('data_manager.requests.get')
def test_charger_donnees_succes_api(mock_get):
    """
    Vérifie que charger_donnees traite correctement une réponse réussie de l'API.
    """
    # ARRANGE : On configure notre faux 'requests.get'
    fausse_reponse_json = {
        "draws": [
            {
                "date": "2025-09-19",
                "numbers": "8,10,26,32,42",
                "stars": "9,12"
            },
            {
                "date": "2025-09-16",
                "numbers": "1,9,13,35,40",
                "stars": "5,6"
            }
        ]
    }
    # Notre mock retournera un objet avec un statut 200 et notre JSON
    mock_get.return_value = Mock(status_code=200)
    mock_get.return_value.json.return_value = fausse_reponse_json

    # ACT : On appelle la fonction à tester
    tirages = data_manager.charger_donnees()

    # ASSERT : On vérifie que les données ont été correctement parsées
    assert len(tirages) == 2
    # La fonction doit inverser l'ordre pour avoir le plus récent en premier
    assert tirages[0].date == "19/09/2025"
    assert tirages[0].numeros == [8, 10, 26, 32, 42]
    assert tirages[1].date == "16/09/2025"
    assert tirages[1].etoiles == [5, 6]
    # On vérifie que le VRAI appel a bien été fait une fois
    mock_get.assert_called_once()

@patch('data_manager.requests.get')
def test_charger_donnees_echec_api_fallback_csv(mock_get, tmp_path):
    """
    Vérifie que charger_donnees se rabat sur le CSV si l'API échoue.
    """
    # ARRANGE :
    # 1. On configure le mock pour simuler une erreur réseau
    mock_get.side_effect = requests.RequestException("Erreur réseau simulée")

    # 2. On crée un faux fichier CSV pour le test
    d = tmp_path / "data"
    d.mkdir()
    fichier_csv_test = d / "fallback.csv"
    contenu_csv = "date_de_tirage;boule_1;boule_2;boule_3;boule_4;boule_5;etoile_1;etoile_2\n"
    contenu_csv += "20250919;26;32;42;8;10;9;12"
    fichier_csv_test.write_text(contenu_csv)

    # ACT : On appelle la fonction
    tirages = data_manager.charger_donnees(chemin_fichier_fallback=str(fichier_csv_test))

    # ASSERT : On vérifie que les données du CSV ont bien été lues
    assert len(tirages) == 1
    assert tirages[0].date == "19/09/2025"
    assert tirages[0].numeros == [8, 10, 26, 32, 42]