# prediction_models.py
from collections import Counter
import data_manager
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib
import os
import feature_engineering
import logging

def analyse_frequence(historique_tirages: list[data_manager.Tirage]) -> list[tuple[int, int]]:
    """Analyse la fréquence de sortie de chaque numéro dans un historique."""
    tous_les_numeros = []
    for tirage in historique_tirages:
        tous_les_numeros.extend(tirage.numeros)
    frequence = Counter(tous_les_numeros)
    return frequence.most_common(5)

class ComiteDeModelesML:
    """Un comité de modèles de Machine Learning pour prédire les tirages."""
    def __init__(self, n_estimators: int = 50, max_depth: int | None = None, random_state: int = 42):
        """Initialise le comité de modèles avec les hyperparamètres spécifiés."""
        self.modeles_boules = {
            f'boule_{i}': RandomForestClassifier(
                n_estimators=n_estimators, 
                max_depth=max_depth,
                random_state=random_state
            ) for i in range(1, 6)
        }
        self.modeles_etoiles = {
            f'etoile_{i}': RandomForestClassifier(
                n_estimators=n_estimators,
                max_depth=max_depth,
                random_state=random_state
            ) for i in range(1, 3)
        }
        self.est_entraine = False
        if not os.path.exists('model_cache'):
            os.makedirs('model_cache')

    def _preparer_donnees(self, historique_tirages: list[data_manager.Tirage]) -> tuple[pd.DataFrame, pd.DataFrame]:
        """Prépare les données pour l'entraînement en features (X) et cibles (y)."""
        boules_df = pd.DataFrame([t.numeros for t in historique_tirages], columns=[f'boule_{i}' for i in range(1, 6)])
        etoiles_df = pd.DataFrame([t.etoiles for t in historique_tirages], columns=[f'etoile_{i}' for i in range(1, 3)])
        X_base = pd.concat([boules_df, etoiles_df], axis=1)
        features_additionnelles = feature_engineering.enrichir_donnees(historique_tirages)
        X_complet = pd.concat([X_base, features_additionnelles], axis=1)
        X = X_complet.iloc[:-1]
        y_df = pd.concat([boules_df, etoiles_df], axis=1).iloc[1:]
        y_df = y_df.reset_index(drop=True)
        return X, y_df

    def entrainer(self, historique_tirages: list[data_manager.Tirage]) -> None:
        """Entraîne tous les modèles du comité sur l'historique fourni."""
        nom_fichier_modele = f"model_cache/model_{len(historique_tirages)}_{str(historique_tirages[0].date)}.joblib"
        if os.path.exists(nom_fichier_modele):
            logging.info(f"Chargement du comité de modèles depuis le cache : {nom_fichier_modele}")
            modeles_charges = joblib.load(nom_fichier_modele)
            self.modeles_boules = modeles_charges['boules']
            self.modeles_etoiles = modeles_charges['etoiles']
            self.est_entraine = True
            return

        logging.debug("Préparation des données pour l'entraînement...")
        X, y_df = self._preparer_donnees(historique_tirages)
        logging.info("Entraînement du comité de modèles...")
        for i in range(1, 6):
            self.modeles_boules[f'boule_{i}'].fit(X, y_df[f'boule_{i}'])
        for i in range(1, 3):
            self.modeles_etoiles[f'etoile_{i}'].fit(X, y_df[f'etoile_{i}'])
        self.est_entraine = True
        logging.info(f"Sauvegarde du modèle dans le cache : {nom_fichier_modele}")
        joblib.dump({'boules': self.modeles_boules, 'etoiles': self.modeles_etoiles}, nom_fichier_modele)

    def predire(self, dernier_tirage: data_manager.Tirage, historique_passe: list[data_manager.Tirage]) -> tuple[list[int], list[int]]:
        """Prédit un tirage complet et garanti sans doublons."""
        if not self.est_entraine:
            raise Exception("Le modèle doit être entraîné avant de pouvoir faire une prédiction.")

        stats = feature_engineering.calculer_stats_tirage(dernier_tirage)
        ecarts = feature_engineering.calculer_ecarts(historique_passe)
        freq_chaude = feature_engineering.calculer_frequence_chaude(historique_passe)
        donnees_base = pd.DataFrame([dernier_tirage.numeros + dernier_tirage.etoiles], columns=[f'boule_{i}' for i in range(1, 6)] + [f'etoile_{i}' for i in range(1, 3)])
        features_additionnelles = pd.DataFrame([{**stats, **ecarts, **freq_chaude}])
        donnees_a_predire = pd.concat([donnees_base, features_additionnelles], axis=1)
        ordre_colonnes = self.modeles_boules['boule_1'].feature_names_in_
        donnees_a_predire = donnees_a_predire[ordre_colonnes]

        pred_boules = self._predire_et_resoudre_conflits(self.modeles_boules, donnees_a_predire, 5)
        pred_etoiles = self._predire_et_resoudre_conflits(self.modeles_etoiles, donnees_a_predire, 2)
        return sorted(pred_boules), sorted(pred_etoiles)

    def _predire_et_resoudre_conflits(self, modeles: dict, donnees_a_predire: pd.DataFrame, n_predictions: int) -> list[int]:
        """Génère des prédictions uniques à partir d'un comité de modèles."""
        probas_par_modele = {}
        for nom, modele in modeles.items():
            probabilities = modele.predict_proba(donnees_a_predire)[0]
            classes = modele.classes_
            probas_par_modele[nom] = sorted(zip(probabilities, classes), reverse=True)

        predictions = {nom: probas[0][1] for nom, probas in probas_par_modele.items()}
        indices_choix = {nom: 0 for nom in modeles.keys()}

        while len(set(predictions.values())) < n_predictions:
            comptes = Counter(predictions.values())
            doublons = {numero for numero, compte in comptes.items() if compte > 1}
            for doublon in doublons:
                modeles_en_conflit = [nom for nom, pred in predictions.items() if pred == doublon]
                probabilite_la_plus_basse = float('inf')
                modele_a_changer = None
                for nom_modele in modeles_en_conflit:
                    index_actuel = indices_choix[nom_modele]
                    proba_actuelle = probas_par_modele[nom_modele][index_actuel][0]
                    if proba_actuelle < probabilite_la_plus_basse:
                        probabilite_la_plus_basse = proba_actuelle
                        modele_a_changer = nom_modele
                if modele_a_changer:
                    indices_choix[modele_a_changer] += 1
                    nouvel_index = indices_choix[modele_a_changer]
                    if nouvel_index < len(probas_par_modele[modele_a_changer]):
                        predictions[modele_a_changer] = probas_par_modele[modele_a_changer][nouvel_index][1]
                    else:
                        break
        return list(predictions.values())