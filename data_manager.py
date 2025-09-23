# data_manager.py
import pandas as pd
import requests 
from datetime import datetime 

class Tirage:
    """ Représente un seul tirage de l'Euromillions."""
    def __init__(self, date, numeros, etoiles):
        """
        Initialise un objet Tirage.
        Args:
            date (str): La date du tirage au format JJ/MM/AAAA.
            numeros (list): Une liste de 5 entiers pour les numéros.
            etoiles (list): Une liste de 2 entiers pour les étoiles.
        """
        self.date = date
        self.numeros = sorted(numeros) # On trie pour être cohérent
        self.etoiles = sorted(etoiles) # On trie pour être cohérent

# Dans data_manager.py

API_URL = "http://localhost:8000/euromillions-results" # URL Fictive pour l'exemple

def _parser_date_api(date_str):
    """Convertit une chaîne de date du format API (AAAA-MM-JJ) au format interne (JJ/MM/AAAA).

    Args:
        date_str (str): La date au format "AAAA-MM-JJ".

    Returns:
        str: La date convertie au format "JJ/MM/AAAA".
    """
    return datetime.strptime(date_str, "%Y-%m-%d").strftime("%d/%m/%Y")

def _parser_date_csv(date_str):
    """Convertit une chaîne de date du format CSV (AAAAMMJJ) au format interne (JJ/MM/AAAA).

    Args:
        date_str (str or int): La date au format "AAAAMMJJ".

    Returns:
        str: La date convertie au format "JJ/MM/AAAA".
    """
    return datetime.strptime(str(date_str), "%Y%m%d").strftime("%d/%m/%Y")


def charger_donnees(chemin_fichier_fallback='euromillions_results.csv'):
    """Charge l'historique des tirages, en priorisant l'API puis un fichier CSV.

    Tente de récupérer les données depuis une API distante. En cas d'échec de la
    connexion ou de la validation des données, la fonction se rabat sur la lecture
    d'un fichier CSV local en guise de secours.

    Args:
        chemin_fichier_fallback (str): Le chemin vers le fichier CSV à utiliser
            si l'appel à l'API échoue. La valeur par défaut est
            'euromillions_results.csv'.

    Returns:
        list[Tirage]: Une liste d'objets `Tirage`, triée du plus récent au plus
        ancien. Retourne une liste vide si l'API et le fichier de secours
        sont tous deux inaccessibles.
    """
    try:
        # On tente de récupérer les données de l'API
        reponse = requests.get(API_URL, timeout=5)
        reponse.raise_for_status()  # Lève une exception pour les codes d'erreur HTTP

        # Si succès, on traite la réponse JSON
        donnees_api = reponse.json()
        liste_tirages = []
        for tirage_json in donnees_api.get("draws", []):
            date = _parser_date_api(tirage_json["date"])
            numeros = [int(n) for n in tirage_json["numbers"].split(',')]
            etoiles = [int(e) for e in tirage_json["stars"].split(',')]
            liste_tirages.append(Tirage(date, numeros, etoiles))
        
        # L'API est supposée retourner les tirages dans l'ordre attendu (plus récent en premier).
        print("✅ Données chargées avec succès depuis l'API.")
        return liste_tirages

    except (requests.RequestException, ValueError) as e:
        # En cas d'erreur réseau ou de JSON invalide, on se rabat sur le CSV
        print(f"⚠️ L'API a échoué ({e}), tentative de chargement depuis le fichier CSV local.")
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
                    print(f"⚠️ Ligne ignorée (index {index}) dans le CSV : {ex}")
            
            print("✅ Données chargées avec succès depuis le fichier CSV.")
            return liste_tirages
        except FileNotFoundError:
            print(f"❌ ERREUR : Le fichier de fallback '{chemin_fichier_fallback}' est introuvable.")
            return []