# tests/test_data_manager.py
import sys
import os
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

def test_charger_donnees_csv(tmp_path):
    """
    Vérifie que charger_donnees charge correctement les données depuis un fichier CSV.
    """
    # ARRANGE : On crée un faux fichier CSV pour le test
    fichier_csv_test = tmp_path / "test.csv"
    contenu_csv = "date_de_tirage;boule_1;boule_2;boule_3;boule_4;boule_5;etoile_1;etoile_2\n"
    contenu_csv += "20250919;8;10;26;32;42;9;12\n"
    contenu_csv += "20250916;1;9;13;35;40;5;6"
    fichier_csv_test.write_text(contenu_csv, encoding='utf-8')

    # ACT : On appelle la fonction à tester
    tirages = data_manager.charger_donnees(chemin_fichier=str(fichier_csv_test))

    # ASSERT : On vérifie que les données ont été correctement parsées
    assert len(tirages) == 2
    assert tirages[0].date == "20250919"
    assert tirages[0].numeros == [8, 10, 26, 32, 42]
    assert tirages[0].etoiles == [9, 12]
    assert tirages[1].date == "20250916"
    assert tirages[1].numeros == [1, 9, 13, 35, 40]
    assert tirages[1].etoiles == [5, 6]