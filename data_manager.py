# data_manager.py

class Tirage:
    def __init__(self, date, numeros, etoiles):
        self.date = date
        self.numeros = numeros
        self.etoiles = etoiles

def charger_donnees():
    """Cette fonction sera responsable de charger l'historique des tirages."""
    print("Module data_manager : chargement des données...")
    # Pour l'instant, on retourne une liste vide.
    return []