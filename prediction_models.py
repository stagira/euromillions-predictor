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
    Encapsule la logique du modèle de Machine Learning "RandomForest".
    """
    def __init__(self):
        # On initialise le modèle, mais il n'est pas encore entraîné
        self.modele = RandomForestClassifier(n_estimators=100, random_state=42)
        self.est_entraine = False

    def entrainer(self, historique_tirages: list[data_manager.Tirage]):
        """
        Entraîne le modèle sur l'historique des données.
        """
        print("\n🧠 Entraînement du modèle de Machine Learning...")

        # 1. On transforme notre liste d'objets Tirage en un format que Pandas comprend
        numeros_df = pd.DataFrame([t.numeros for t in historique_tirages], 
                                  columns=['boule_1', 'boule_2', 'boule_3', 'boule_4', 'boule_5'])

        # 2. On prépare les données X et y, comme dans Colab
        X = numeros_df[:-1]  # Toutes les boules, sauf pour le dernier tirage
        y = numeros_df['boule_1'][1:] # La première boule du tirage suivant

        # 3. On entraîne le modèle
        self.modele.fit(X, y)
        self.est_entraine = True
        print("✅ Modèle entraîné avec succès !")

    def predire(self, dernier_tirage: data_manager.Tirage):
        """
        Prédit le premier numéro du prochain tirage en se basant sur le dernier.
        """
        if not self.est_entraine:
            return "Erreur: Le modèle doit être entraîné avant de faire une prédiction."

        # On met les données du dernier tirage au bon format pour le modèle
        donnees_a_predire = pd.DataFrame([dernier_tirage.numeros], 
                                         columns=['boule_1', 'boule_2', 'boule_3', 'boule_4', 'boule_5'])

        # On fait la prédiction
        prediction = self.modele.predict(donnees_a_predire)
        probabilites = self.modele.predict_proba(donnees_a_predire)
        confiance = np.max(probabilites)

        return f"Le modèle prédit le numéro {prediction[0]} avec une confiance de {confiance*100:.2f}%"
