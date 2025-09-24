# data_manager.py
import pandas as pd
import requests 
from datetime import datetime 
import logging

# --- Constantes et Configuration ---
API_URL = "http://localhost:8000/euromillions-results"  # URL Fictive pour l'exemple

# --- Fonctions de Parsing ---

def _parser_date_api(date_str: str) -> str:
    """Convertit une chaîne de date du format API (AAAA-MM-JJ) au format interne (JJ/MM/AAAA)."""
    return datetime.strptime(date_str, "%Y-%m-%d").strftime("%d/%m/%Y")

def _parser_date_csv(date_str: str | int) -> str:
    """Convertit une chaîne de date du format CSV (AAAAMMJJ) au format interne (JJ/MM/AAAA)."""
    return datetime.strptime(str(date_str), "%Y%m%d").strftime("%d/%m/%Y")

# --- Classe de Données ---

class Tirage:
    """ Représente un seul tirage de l'Euromillions."""
    def __init__(self, date, numeros, etoiles):
        self.date = date
        self.numeros = sorted(numeros)
        self.etoiles = sorted(etoiles)

# --- Fonction Principale de Chargement ---

def charger_donnees(chemin_fichier_fallback: str = 'euromillions_results.csv') -> list[Tirage]:
    """
    Charge l'historique des tirages, en priorisant l'API puis un fichier CSV.
    """
    try:
        reponse = requests.get(API_URL, timeout=5)
        reponse.raise_for_status()
        donnees_api = reponse.json()
        liste_tirages = []
        for tirage_json in donnees_api.get("draws", []):
            date = _parser_date_api(tirage_json["date"])
            numeros = [int(n) for n in tirage_json["numbers"].split(',')]
            etoiles = [int(e) for e in tirage_json["stars"].split(',')]
            liste_tirages.append(Tirage(date, numeros, etoiles))
        logging.info("Données chargées avec succès depuis l'API.")
        return liste_tirages
    except (requests.RequestException, ValueError) as e:
        logging.warning(f"L'API a échoué ({e}), tentative de chargement depuis le fichier CSV local.")
        try:
            df = pd.read_csv(chemin_fichier_fallback, sep=';')
            liste_tirages = []
            for index, row in df.iterrows():
                try:
                    date = _parser_date_csv(row['date_de_tirage'])
                    numeros = [int(row[f'boule_{i}']) for i in range(1, 6)]
                    etoiles = [int(row[f'etoile_{i}']) for i in range(1, 3)]
                    liste_tirages.append(Tirage(date, numeros, etoiles))
                except (ValueError, TypeError) as ex:
                    logging.warning(f"Ligne ignorée (index {index}) dans le CSV : {ex}")
            logging.info("Données chargées avec succès depuis le fichier CSV.")
            return liste_tirages
        except FileNotFoundError:
            logging.error(f"Le fichier de fallback '{chemin_fichier_fallback}' est introuvable.")
            return []