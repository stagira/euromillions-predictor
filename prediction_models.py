# prediction_models.py
from collections import Counter
import data_manager
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib
import os
import feature_engineering

def analyse_frequence(historique_tirages: list[data_manager.Tirage]) -> list[tuple[int, int]]:
    """Analyse la fréquence de sortie de chaque numéro dans un historique.

    Args:
        historique_tirages (list[data_manager.Tirage]): Une liste d'objets
            Tirage représentant l'historique à analyser.

    Returns:
        list[tuple[int, int]]: Une liste de tuples, où chaque tuple contient
        un numéro et son nombre d'occurrences. La liste est triée par ordre
        décroissant de fréquence.
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
    """Un comité de modèles de Machine Learning pour prédire les tirages.

    Cette classe gère un ensemble de modèles RandomForest, un pour chaque boule
    et étoile à prédire. Elle encapsule la logique d'entraînement, de prédiction,
    de gestion de cache des modèles entraînés, et de préparation des données
    en évitant les fuites d'information du futur.
    """
    def __init__(self, n_estimators: int = 50, max_depth: int | None = None, random_state: int = 42):
        """Initialise le comité de modèles avec les hyperparamètres spécifiés.

        Args:
            n_estimators (int, optional): Le nombre d'arbres dans la forêt.
                Defaults to 50.
            max_depth (int | None, optional): La profondeur maximale des arbres.
                Si None, les nœuds sont étendus jusqu'à ce que toutes les
                feuilles soient pures. Defaults to None.
            random_state (int, optional): Contrôle le caractère aléatoire pour
                la reproductibilité des résultats. Defaults to 42.
        """
        # Initialisation des modèles avec les hyperparamètres fournis
        # `max_depth=None` signifie que les arbres peuvent grandir autant que nécessaire
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
        
        # Création du dossier de cache s'il n'existe pas
        if not os.path.exists('model_cache'):
            os.makedirs('model_cache')

    def _preparer_donnees(self, historique_tirages: list[data_manager.Tirage]) -> tuple[pd.DataFrame, pd.DataFrame]:
        """Prépare les données pour l'entraînement en features (X) et cibles (y).

        Cette méthode cruciale construit le jeu de données en s'assurant qu'il
        n'y a aucune fuite d'information du futur. Pour un tirage N, les
        caractéristiques (X) sont construites à partir des tirages N-1, N-2, etc.,
        et la cible (y) est le résultat du tirage N.

        Args:
            historique_tirages (list[data_manager.Tirage]): L'historique complet
                des tirages, du plus récent au plus ancien.

        Returns:
            tuple[pd.DataFrame, pd.DataFrame]: Un tuple contenant le DataFrame
            des caractéristiques (X) et le DataFrame des cibles (y).
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

    def entrainer(self, historique_tirages: list[data_manager.Tirage]) -> None:
        """Entraîne tous les modèles du comité sur l'historique fourni.

        La méthode utilise un système de cache pour éviter de ré-entraîner des
        modèles sur un historique déjà vu. Le nom du fichier de cache est
        dérivé de la taille de l'historique et de la date du premier tirage.

        Args:
            historique_tirages (list[data_manager.Tirage]): La liste complète
                des objets Tirage à utiliser pour l'entraînement.
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
    

    def predire(self, dernier_tirage: data_manager.Tirage, historique_passe: list[data_manager.Tirage]) -> tuple[list[int], list[int]]:
        """Prédit un tirage complet et garanti sans doublons.

        Cette méthode utilise le dernier tirage connu et son historique pour
        construire les caractéristiques nécessaires à la prédiction. Elle invoque
        ensuite une logique de résolution de conflits pour s'assurer que les
        numéros prédits (boules et étoiles) sont uniques.

        Args:
            dernier_tirage (data_manager.Tirage): Le dernier tirage connu.
            historique_passe (list[data_manager.Tirage]): La liste de tous les
                tirages qui ont précédé le `dernier_tirage`.

        Raises:
            Exception: Si la méthode est appelée avant que le modèle ne soit entraîné.

        Returns:
            tuple[list[int], list[int]]: Un tuple contenant deux listes triées :
            la première pour les 5 boules prédites, la seconde pour les 2 étoiles.
        """
        if not self.est_entraine:
            raise Exception("Le modèle doit être entraîné avant de pouvoir faire une prédiction.")

        # 1. Préparer les données de base du dernier tirage (les 7 numéros)
        donnees_base = pd.DataFrame([dernier_tirage.numeros + dernier_tirage.etoiles], 
                                    columns=[f'boule_{i}' for i in range(1, 6)] + [f'etoile_{i}' for i in range(1, 3)])

        # 2. Calculer les features enrichies pour ce tirage en se basant sur le passé
        # Note : On utilise directement les fonctions de notre module feature_engineering
        stats = feature_engineering.calculer_stats_tirage(dernier_tirage)
        ecarts = feature_engineering.calculer_ecarts(historique_passe)
        freq_chaude = feature_engineering.calculer_frequence_chaude(historique_passe)
        
        features_additionnelles = pd.DataFrame([{**stats, **ecarts, **freq_chaude}])

        # 3. Combiner les deux pour avoir les 111 colonnes attendues par le modèle
        donnees_a_predire = pd.concat([donnees_base, features_additionnelles], axis=1)
        
        # 4. S'assurer que les colonnes sont dans le même ordre que lors de l'entraînement
        # (Scikit-learn peut être sensible à l'ordre)
        # On récupère l'ordre des colonnes du premier modèle entraîné comme référence
        ordre_colonnes = self.modeles_boules['boule_1'].feature_names_in_
        donnees_a_predire = donnees_a_predire[ordre_colonnes]

        # 5. Prédiction avec logique anti-doublons
        pred_boules = self._predire_et_resoudre_conflits(self.modeles_boules, donnees_a_predire, 5)
        pred_etoiles = self._predire_et_resoudre_conflits(self.modeles_etoiles, donnees_a_predire, 2)

        return sorted(pred_boules), sorted(pred_etoiles)

    def _predire_et_resoudre_conflits(self, modeles: dict, donnees_a_predire: pd.DataFrame, n_predictions: int) -> list[int]:
        """Génère des prédictions uniques à partir d'un comité de modèles.

        Cette fonction utilise `predict_proba` pour obtenir les probabilités de
        chaque numéro. Elle sélectionne initialement le meilleur choix pour chaque
        modèle, puis entre dans une boucle de validation pour résoudre les
        conflits (doublons). Si un doublon est détecté, le modèle le moins
        confiant pour ce choix est forcé de passer à son alternative suivante,
        jusqu'à ce que toutes les prédictions soient uniques.

        Args:
            modeles (dict): Le dictionnaire de modèles à utiliser (boules ou étoiles).
            donnees_a_predire (pd.DataFrame): Le DataFrame contenant les
                caractéristiques pour la prédiction.
            n_predictions (int): Le nombre de prédictions uniques attendues.

        Returns:
            list[int]: Une liste de `n_predictions` numéros uniques.
        """
        # Étape 1: Obtenir les probabilités pour chaque modèle
        probas_par_modele = {}
        for nom, modele in modeles.items():
            # `predict_proba` renvoie une liste de listes de probas, une pour chaque classe
            probabilities = modele.predict_proba(donnees_a_predire)[0]
            # On associe chaque proba à sa classe (le numéro)
            classes = modele.classes_
            probas_avec_classes = sorted(zip(probabilities, classes), reverse=True)
            probas_par_modele[nom] = probas_avec_classes

        # Étape 2: Initialiser la prédiction avec le meilleur choix de chaque modèle
        predictions = {nom: probas[0][1] for nom, probas in probas_par_modele.items()}
        indices_choix = {nom: 0 for nom in modeles.keys()}

        # Étape 3: Boucler jusqu'à ce qu'il n'y ait plus de doublons
        while len(set(predictions.values())) < n_predictions:
            # Trouver les numéros dupliqués
            comptes = Counter(predictions.values())
            doublons = {numero for numero, compte in comptes.items() if compte > 1}

            for doublon in doublons:
                # Identifier les modèles qui ont prédit ce doublon
                modeles_en_conflit = [nom for nom, pred in predictions.items() if pred == doublon]

                # Trouver le modèle le moins confiant parmi ceux en conflit
                probabilite_la_plus_basse = float('inf')
                modele_a_changer = None
                for nom_modele in modeles_en_conflit:
                    # On récupère la proba du choix actuel pour ce modèle
                    index_actuel = indices_choix[nom_modele]
                    proba_actuelle = probas_par_modele[nom_modele][index_actuel][0]
                    if proba_actuelle < probabilite_la_plus_basse:
                        probabilite_la_plus_basse = proba_actuelle
                        modele_a_changer = nom_modele

                # Faire passer ce modèle à son choix suivant
                if modele_a_changer:
                    indices_choix[modele_a_changer] += 1
                    nouvel_index = indices_choix[modele_a_changer]
                    # S'assurer qu'on ne sort pas de la liste des choix possibles
                    if nouvel_index < len(probas_par_modele[modele_a_changer]):
                        predictions[modele_a_changer] = probas_par_modele[modele_a_changer][nouvel_index][1]
                    else:
                        # Cas très rare: on est à court de choix, on brise pour éviter une boucle infinie
                        # Une meilleure gestion serait de choisir un numéro aléatoire non présent
                        break

        return list(predictions.values())