# data_manager.py

class Tirage:
    """Représente un seul tirage de l'Euromillions."""
    def __init__(self, date, numeros, etoiles):
        """
        Initialise un objet Tirage.

        Args:
            date (str): La date du tirage au format JJ/MM/AAAA.
            numeros (list): Une liste de 5 entiers pour les numéros.
            etoiles (list): Une liste de 2 entiers pour les étoiles.
        """
        self.date = date
        self.numeros = numeros
        self.etoiles = etoiles

def charger_donnees():
    """Charge l'historique complet des tirages."""
    print("Module data_manager : chargement des données...")
    return []