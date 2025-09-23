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

def charger_donnees(chemin_fichier='euromillions_results.csv'):
    """
    Charge l'historique des tirages depuis un fichier CSV.
    
    Args:
        chemin_fichier (str): Le chemin vers le fichier CSV.

    Returns:
        list: Une liste d'objets Tirage.
    """
    df = pd.read_csv(chemin_fichier, sep=';')
    
    liste_tirages = []
    for index, row in df.iterrows():
        date = row['date_de_tirage']
        
        # --- CORRECTION ICI ---
        # On s'assure que toutes les boules et étoiles sont bien des nombres entiers
        try:
            numeros = [
                int(row['boule_1']), 
                int(row['boule_2']), 
                int(row['boule_3']), 
                int(row['boule_4']), 
                int(row['boule_5'])
            ]
            etoiles = [
                int(row['etoile_1']), 
                int(row['etoile_2'])
            ]
            
            tirage = Tirage(date, numeros, etoiles)
            liste_tirages.append(tirage)
        except (ValueError, TypeError) as e:
            print(f"⚠️ Avertissement : Ligne ignorée à l'index {index} car les données ne sont pas des nombres valides. Erreur: {e}")

    return liste_tirages