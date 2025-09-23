# prediction_models.py
from collections import Counter
import data_manager
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

def analyse_frequence(historique_tirages: list[data_manager.Tirage]):
    """
    Analyse la fréquence de sortie de chaque numéro dans l'historique.

    Args:
        historique_tirages (list): Une liste d'objets Tirage.

    Returns:
        list: Une liste de tuples (numero, occurrences) des 5 numéros les plus fréquents.
    """
    tous_les_numeros = []
    for tirage in historique_tirages:
        tous_les_numeros.extend(tirage.numeros)

    # Counter est un outil magique pour compter des éléments dans une liste
    frequence = Counter(tous_les_numeros)

    # .most_common(5) nous donne les 5 plus fréquents
    numeros_chauds = frequence.most_common(5)

    return numeros_chauds

class ModeleRandomForest:
    """
    Encapsule un comité de 5 modèles RandomForest pour prédire un tirage complet.
    """
    def __init__(self):
        # On crée un dictionnaire pour contenir nos 5 modèles, un par boule
        self.modeles = {f'boule_{i}': RandomForestClassifier(n_estimators=100, random_state=42) for i in range(1, 6)}
        self.est_entraine = False

    def entrainer(self, historique_tirages: list[data_manager.Tirage]):
        """
        Entraîne les 5 modèles, chacun sur sa boule respective.
        """
        print("\n🧠 Entraînement du comité de 5 modèles de Machine Learning...")

        numeros_df = pd.DataFrame([t.numeros for t in historique_tirages], 
                                  columns=['boule_1', 'boule_2', 'boule_3', 'boule_4', 'boule_5'])

        X = numeros_df[:-1]

        # On entraîne chaque modèle sur sa cible
        for i in range(1, 6):
            nom_boule = f'boule_{i}'
            print(f"   - Entraînement du spécialiste pour {nom_boule}...")
            y = numeros_df[nom_boule][1:]
            self.modeles[nom_boule].fit(X, y)
        
        self.est_entraine = True
        print("✅ Comité de modèles entraîné avec succès !")

    def predire(self, dernier_tirage: data_manager.Tirage):
        """
        Combine les prédictions des 5 modèles pour un tirage complet.
        """
        if not self.est_entraine:
            return "Erreur: Le modèle doit être entraîné."

        donnees_a_predire = pd.DataFrame([dernier_tirage.numeros], 
                                         columns=['boule_1', 'boule_2', 'boule_3', 'boule_4', 'boule_5'])
        
        prediction_finale = []
        # Chaque modèle spécialiste fait sa propre prédiction
        for i in range(1, 6):
            nom_boule = f'boule_{i}'
            prediction = self.modeles[nom_boule].predict(donnees_a_predire)
            prediction_finale.append(prediction[0])
            
        # On trie les numéros pour un affichage plus propre
        prediction_finale.sort()
        return f"Le comité de modèles prédit les 5 numéros suivants : {prediction_finale}"