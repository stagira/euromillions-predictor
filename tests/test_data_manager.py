# tests/test_data_manager.py
import sys
import os
import prediction_models 

# Ajoute le dossier parent au chemin pour que Python trouve data_manager
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import data_manager
from prediction_models import analyse_frequence


def test_creation_tirage():
    """Vérifie que les données sont correctement assignées lors de la création d'un objet Tirage."""
    # 1. Préparation des données de test
    date_test = "22/09/2025"
    numeros_test = [1, 2, 3, 4, 5]
    etoiles_test = [6, 7]

    # 2. Action : création de l'objet
    mon_tirage = data_manager.Tirage(date=date_test, numeros=numeros_test, etoiles=etoiles_test)

    # 3. Vérification : on affirme que les valeurs sont correctes
    assert mon_tirage.date == date_test
    assert mon_tirage.numeros == numeros_test
    assert mon_tirage.etoiles == etoiles_test