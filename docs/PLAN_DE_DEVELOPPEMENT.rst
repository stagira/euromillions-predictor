======================================
Plan de Développement Détaillé
======================================

Ce document retrace les grandes étapes de la création et de l'amélioration de l'application Euromillions Predictor, en détaillant les objectifs, actions et concepts clés de chaque phase.

.. contents:: Journal de Bord du Projet
   :local:
   :depth: 2

---

Étape 1 : Initialisation et Structure de Base
---------------------------------------------
* **Objectif** : Mettre en place une architecture de projet saine, modulaire et évolutive.
* **Actions Clés** :
    * Création des modules Python distincts pour chaque responsabilité :
        * ``data_manager.py`` : Pour tout ce qui touche au chargement des données.
        * ``prediction_models.py`` : Pour la logique des modèles de prédiction.
        * ``backtest.py`` : Pour la simulation de performance historique.
        * ``evaluation.py`` : Pour le calcul des scores.
        * ``main.py`` : Comme point d'entrée de l'application.
    * Mise en place d'un premier modèle simple basé sur ``RandomForestClassifier``.
* **Concepts Abordés** : Modularité, Séparation des préoccupations (Separation of Concerns).

---

Étape 2 : Ingénierie de Caractéristiques (Feature Engineering)
-------------------------------------------------------------
* **Objectif** : Enrichir les données brutes pour fournir plus de contexte au modèle de Machine Learning, dans l'espoir d'améliorer ses performances.
* **Actions Clés** :
    * Création d'un nouveau module dédié : ``feature_engineering.py``.
    * Développement de fonctions pour calculer :
        * Les **écarts** : Depuis combien de tirages un numéro n'est pas sorti.
        * Les **fréquences chaudes** : La popularité d'un numéro sur une période récente.
        * Les **statistiques de tirage** : Somme, moyenne, parité des numéros.
* **Concepts Abordés** : L'importance du Feature Engineering en Data Science.

---

Étape 3 : Intégration des Nouvelles Features
--------------------------------------------
* **Objectif** : Utiliser les caractéristiques créées à l'étape 2 dans le pipeline d'entraînement et de prédiction du modèle.
* **Actions Clés** :
    * Modification de la méthode ``_preparer_donnees`` dans ``prediction_models.py`` pour fusionner les données brutes avec les nouvelles caractéristiques.
    * Modification de la méthode ``predire`` pour qu'elle puisse aussi calculer ces caractéristiques pour une nouvelle prédiction.
* **Défis Rencontrés** :
    * ``ValueError`` de Scikit-learn car les données de prédiction n'avaient pas la même forme que les données d'entraînement.
    * ``TypeError`` car la méthode ``predire`` modifiée nécessitait un argument supplémentaire (``historique_passe``) qui n'était pas fourni par les scripts l'appelant.

---

Étape 4 : Optimisation d'Hyperparamètres
----------------------------------------
* **Objectif** : Trouver la meilleure configuration possible pour notre ``RandomForestClassifier`` au lieu d'utiliser des paramètres par défaut.
* **Actions Clés** :
    * Modification de la classe ``ComiteDeModelesML`` pour qu'elle accepte des hyperparamètres (``n_estimators``, ``max_depth``) lors de son initialisation.
    * Transformation de ``backtest.py`` pour qu'il agisse comme un "juge" évaluant un modèle donné et retournant un score.
    * Mise en place d'une boucle de "Grid Search" (le "tournoi") dans ``main.py`` pour tester de multiples combinaisons et identifier la meilleure.
* **Concepts Abordés** : Hyperparameter Tuning, Grid Search.

---

Étape 5 : Persistance et Scripts de Production
----------------------------------------------
* **Objectif** : Sauvegarder le travail d'optimisation et rendre le modèle facilement utilisable pour de vraies prédictions.
* **Actions Clés** :
    * Utilisation de ``joblib`` et ``json`` dans ``main.py`` pour sauvegarder le meilleur modèle entraîné et ses paramètres.
    * Création de ``predire_futur.py`` pour charger le modèle et faire une prédiction simple.
    * Création de ``update_model.py`` pour ré-entraîner rapidement le modèle avec de nouvelles données, sans refaire tout le tournoi.
* **Concepts Abordés** : Sérialisation de modèles, Cycle de vie MLOps (entraînement, mise à jour, prédiction).

---

Étape 6 & 13 : Amélioration de la Documentation
-----------------------------------------------
* **Objectif** : Rendre le projet compréhensible, maintenable et professionnel.
* **Actions Clés** :
    * Adoption du format "Google Style" pour les docstrings.
    * Création d'un fichier ``requirements.txt`` pour gérer les dépendances.
    * Rédaction d'un fichier ``README.md`` complet.
* **Concepts Abordés** : Qualité logicielle, Documentation as Code.

---

Étape 7 & 10 : Automatisation et Fiabilisation des Données
----------------------------------------------------------
* **Objectif** : Rendre l'application autonome en la connectant à une source de données externe et en la rendant robuste aux pannes.
* **Actions Clés** :
    * Remplacement de la lecture du CSV par un appel à une API via la bibliothèque ``requests``.
    * Implémentation d'un mécanisme de "fallback" qui utilise le CSV local en cas d'échec de l'API.
* **Défis Rencontrés** : Débogage itératif de la structure de la réponse de l'API (``TypeError``, ``AttributeError``, ``ValueError`` sur les dates).

---

Étape 8, 9, 17-20 : Maîtrise de l'Environnement Virtuel
-------------------------------------------------------
* **Objectif** : Assurer une exécution stable, isolée et reproductible du projet.
* **Actions Clés** : Création, activation et utilisation systématique d'un environnement virtuel (``venv``).
* **Défis Rencontrés** : Résolution des erreurs de ``PATH`` et de ``ModuleNotFoundError`` en comprenant que toutes les commandes (``pip``, ``pytest``, ``sphinx``) doivent être lancées avec le ``venv`` activé.
* **Concepts Abordés** : Gestion des dépendances, Isolation d'environnement.

---

Étape 11 : Compréhension du Code
--------------------------------
* **Objectif** : Analyser les décisions de conception pour en comprendre l'impact.
* **Actions Clés** : Analyse de l'utilisation de ``sorted()`` dans le ``__init__`` de la classe ``Tirage``.
* **Concepts Abordés** : Programmation défensive, Normalisation des données, Représentation canonique.

---

Étape 12 : Validation des Prédictions
-------------------------------------
* **Objectif** : Garantir que les prédictions générées par le modèle respectent les règles du jeu (ex: pas de numéros dupliqués).
* **Actions Clés** : Refonte de la méthode ``predire`` pour utiliser ``predict_proba()`` et implémenter une boucle de correction pour assurer l'unicité des numéros.
* **Concepts Abordés** : Validation et post-traitement des sorties de modèle.

---

Étape 14 & 15 & 21 : Documentation Professionnelle et Productivité
-----------------------------------------------------------------
* **Objectif** : Mettre en place un outillage professionnel pour la documentation.
* **Actions Clés** :
    * Installation de l'extension "autoDocstring" dans VS Code.
    * Installation et configuration de Sphinx pour générer un site web HTML à partir des docstrings.
    * Création de ce plan de développement et intégration dans la documentation finale.
* **Concepts Abordés** : Tooling, Automatisation de la documentation.