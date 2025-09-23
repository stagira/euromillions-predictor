# prediction_models.py
from collections import Counter
import data_manager
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib
import os
import feature_engineering

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

# Dans prediction_models.py

class ComiteDeModelesML:
    """
    Encapsule deux comités de modèles (un pour les boules, un pour les étoiles),
    incluant une logique de cache et une préparation de données anti-fuite.
    """
    def __init__(self):
        # Initialisation des modèles
        self.modeles_boules = {f'boule_{i}': RandomForestClassifier(n_estimators=50, random_state=42) for i in range(1, 6)}
        self.modeles_etoiles = {f'etoile_{i}': RandomForestClassifier(n_estimators=50, random_state=42) for i in range(1, 3)}
        self.est_entraine = False
        
        # Création du dossier de cache s'il n'existe pas
        if not os.path.exists('model_cache'):
            os.makedirs('model_cache')

    def _preparer_donnees(self, historique_tirages: list[data_manager.Tirage]):
        """
        Extrait et décale les données X (features) et y (targets) pour l'entraînement,
        en s'assurant qu'il n'y a pas de fuite de données du futur.
        Cette version est ENRICHIE avec de nouvelles features.
        """
        # 1. Création des données de base (comme avant)
        boules_df = pd.DataFrame([t.numeros for t in historique_tirages], columns=[f'boule_{i}' for i in range(1, 6)])
        etoiles_df = pd.DataFrame([t.etoiles for t in historique_tirages], columns=[f'etoile_{i}' for i in range(1, 3)])

        # Données de base des tirages N-1, N-2, etc.
        X_base = pd.concat([boules_df, etoiles_df], axis=1)

        # 2. Enrichissement des données avec notre nouveau module
        features_additionnelles = feature_engineering.enrichir_donnees(historique_tirages)

        # 3. Combinaison des features
        # On combine les données de base avec les nouvelles features
        X_complet = pd.concat([X_base, features_additionnelles], axis=1)

        # 4. Décalage temporel pour éviter la fuite de données (comme avant)
        # X: Les données du passé (tous les tirages sauf le dernier)
        X = X_complet.iloc[:-1]

        # y_df: Les solutions du futur (tous les tirages sauf le premier)
        # La cible reste la même : les boules et étoiles du tirage suivant.
        y_df = pd.concat([boules_df, etoiles_df], axis=1).iloc[1:]

        # Les colonnes de y_df doivent être renommées pour correspondre à leur usage
        y_df = y_df.reset_index(drop=True)

        return X, y_df

    def entrainer(self, historique_tirages: list[data_manager.Tirage]):
        """
        Entraîne les modèles, en utilisant un cache pour éviter les recalculs.
        """
        # Création d'un nom de fichier unique pour le cache
        nom_fichier_modele = f"model_cache/model_{len(historique_tirages)}_{str(historique_tirages[0].date)}.joblib"

        # 1. Vérification du cache
        if os.path.exists(nom_fichier_modele):
            print(f"🧠 Chargement du comité de modèles depuis le cache : {nom_fichier_modele}")
            modeles_charges = joblib.load(nom_fichier_modele)
            self.modeles_boules = modeles_charges['boules']
            self.modeles_etoiles = modeles_charges['etoiles']
            self.est_entraine = True
            return

        # 2. Préparation des données (si pas dans le cache)
        X, y_df = self._preparer_donnees(historique_tirages)

        # 3. Entraînement des modèles
        for i in range(1, 6):
            nom_boule = f'boule_{i}'
            self.modeles_boules[nom_boule].fit(X, y_df[nom_boule])

        for i in range(1, 3):
            nom_etoile = f'etoile_{i}'
            self.modeles_etoiles[nom_etoile].fit(X, y_df[nom_etoile])
        
        self.est_entraine = True

        # 4. Sauvegarde dans le cache
        print(f"💾 Sauvegarde du modèle dans le cache : {nom_fichier_modele}")
        modeles_a_sauver = {'boules': self.modeles_boules, 'etoiles': self.modeles_etoiles}
        joblib.dump(modeles_a_sauver, nom_fichier_modele)
    
    def predire(self, dernier_tirage: data_manager.Tirage):
        """
        Prédit un tirage complet (5 boules + 2 étoiles) en se basant sur le dernier tirage connu.
        """
        if not self.est_entraine:
            raise Exception("Le modèle doit être entraîné avant de pouvoir faire une prédiction.")

        # Préparation des données du dernier tirage pour la prédiction
        donnees_a_predire = pd.DataFrame([dernier_tirage.numeros + dernier_tirage.etoiles], 
                                         columns=[f'boule_{i}' for i in range(1, 6)] + [f'etoile_{i}' for i in range(1, 3)])
        
        # Prédiction des boules
        pred_boules = [self.modeles_boules[f'boule_{i}'].predict(donnees_a_predire)[0] for i in range(1, 6)]
        pred_boules.sort()

        # Prédiction des étoiles
        pred_etoiles = [self.modeles_etoiles[f'etoile_{i}'].predict(donnees_a_predire)[0] for i in range(1, 3)]
        pred_etoiles.sort()

        return pred_boules, pred_etoiles