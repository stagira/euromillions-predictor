# data_manager.py
import pandas as pd

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
        # On utilise les nouveaux noms de colonnes ici
        date = row['date_de_tirage']
        numeros = [row['boule_1'], row['boule_2'], row['boule_3'], row['boule_4'], row['boule_5']]
        etoiles = [row['etoile_1'], row['etoile_2']]
        
        # On passe toujours les valeurs dans le même ordre à notre classe Tirage
        tirage = Tirage(date, numeros, etoiles)
        liste_tirages.append(tirage)
    
    return liste_tirages