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
* **Objectif** : Garantir que les prédictions générées par le modèle respectent les règles fondamentales du jeu (ex: pas de boules ou d'étoiles dupliquées).
* **Actions Clés** :
    * Diagnostic : Compréhension que les modèles "spécialistes" pour chaque boule/étoile fonctionnent en isolation et peuvent donc prédire le même numéro.
    * Refonte de la méthode ``predire`` dans ``prediction_models.py``.
    * Implémentation d'une logique de correction post-prédiction qui utilise ``predict_proba()`` pour obtenir les probabilités de tous les numéros possibles.
    * Mise en place d'une boucle de validation qui détecte les doublons et les remplace par le "deuxième meilleur choix" du modèle concerné, jusqu'à ce que la combinaison soit unique.
* **Concepts Abordés** : Validation et post-traitement des sorties de modèle, Utilisation de ``predict_proba()`` vs ``predict()``.

---

Étape 13 : Révision des Bonnes Pratiques de Documentation
---------------------------------------------------------
* **Objectif** : Consolider les connaissances sur la documentation pour assurer la qualité et la maintenabilité du projet.
* **Actions Clés** :
    * Révision de la "Pyramide de la Documentation" :
        1.  **Niveau 1 (Fondation)** : Les docstrings au format Google directement dans le code.
        2.  **Niveau 2 (Porte d'Entrée)** : Un fichier ``README.md`` clair et complet.
        3.  **Niveau 3 (Finition)** : La génération automatique d'un site web de documentation avec Sphinx.
* **Concepts Abordés** : Qualité logicielle, Documentation as Code.

---

Étape 14 : Productivité de l'IDE
--------------------------------
* **Objectif** : Accélérer et standardiser l'écriture de la documentation dans le code.
* **Actions Clés** :
    * Installation et configuration de l'extension **"autoDocstring - Python Docstring Generator"** dans VS Code.
    * Paramétrage de l'extension pour utiliser le format ``google``.
* **Concepts Abordés** : Outillage de développement (Tooling), Automatisation des tâches répétitives.

---

Étape 15 & 20 : Génération Automatique de la Documentation
----------------------------------------------------------
* **Objectif** : Mettre en place un système pour générer un site web professionnel à partir des docstrings du projet.
* **Actions Clés** :
    * Installation de Sphinx et des extensions ``furo`` et ``sphinx-autodoc-typehints``.
    * Initialisation du projet de documentation avec ``sphinx-quickstart``.
    * Configuration du fichier ``docs/conf.py`` pour lier Sphinx au code source du projet et activer les extensions.
    * Création des fichiers ``.rst`` pour définir le contenu et la structure du site.
* **Défis Rencontrés** : Résolution du ``ModuleNotFoundError: No module named 'sklearn'`` en comprenant que Sphinx doit être exécuté avec l'environnement virtuel (``venv``) activé pour avoir accès aux dépendances du projet.

---

Étape 16 & 17 : Maîtrise de la Gestion des Dépendances
------------------------------------------------------
* **Objectif** : Comprendre et appliquer la bonne méthode pour installer des bibliothèques dans un projet Python isolé.
* **Actions Clés** :
    * Installation de ``scikit-learn`` avec ``pip``.
    * Mise à jour du fichier ``requirements.txt`` avec la commande ``pip freeze > requirements.txt``.
* **Défis Rencontrés** : Diagnostic du "mystère de l'installation invisible", en comprenant la différence entre l'environnement Python global et l'environnement virtuel du projet.
* **Concepts Abordés** : Isolation d'environnement, Reproductibilité des projets.

---

Étape 19 : Diagnostic et Correction du Chemin d'Accès
------------------------------------------------------
* **Objectif** : Résoudre les erreurs de terminal liées à des chemins de fichiers incorrects.
* **Actions Clés** :
    * Diagnostic de l'erreur ``Le chemin d’accès spécifié est introuvable``.
    * Utilisation des commandes ``cd`` et ``dir``/``ls`` pour naviguer et vérifier la position dans le système de fichiers avant de lancer des commandes relatives.

---

Étape 21 & 22 : Création d'un Plan de Développement Détaillé
-----------------------------------------------------------
* **Objectif** : Conserver une trace écrite de l'évolution du projet, des décisions prises et des concepts appris.
* **Actions Clés** :
    * Création du fichier ``docs/PLAN_DE_DEVELOPPEMENT.rst``.
    * Intégration de ce fichier dans la table des matières de la documentation Sphinx.
    * Enrichissement du plan avec des détails sur les objectifs, actions et défis de chaque étape.

---

Étape 23 : Création d'un Document de Conception Technique
----------------------------------------------------------
* **Objectif** : Décrire l'architecture logicielle de manière formelle et visuelle.
* **Actions Clés** :
    * Création du fichier ``DESIGN.md``.
    * Utilisation de "Diagrams as Code" avec la syntaxe **Mermaid** pour créer :
        * Un **Diagramme des Composants**.
        * Un **Diagramme de Séquence**.
    * Identification et documentation des outils pour la génération automatique de diagrammes :
        * ``pydeps`` pour le **Graphe de Dépendances**.
        * ``pycallgraph2`` pour le **Graphe d'Appels**.

---

Étape 24 : Automatisation des Tâches avec un `Makefile`
--------------------------------------------------------
* **Objectif** : Simplifier l'utilisation du projet en centralisant les commandes courantes.
* **Actions Clés** :
    * Création d'un ``Makefile`` à la racine du projet.
    * Définition de cibles (`targets`) pour les actions principales : ``install``, ``docs``, ``run``, ``predict``, ``update``, ``clean``.

---

Étape 25 & 26 : Intégration du Workflow de Développement avec Jules
-------------------------------------------------------------------
* **Objectif** : Tirer parti d'un assistant IA avancé (Jules) comme un pair-programmeur pour améliorer la qualité du code et accélérer le développement.
* **Actions Clés** :
    * Clarification que Jules a un accès en lecture au dépôt GitHub du projet.
    * Définition d'un flux de travail où Jules est utilisé pour des tâches complexes : analyse d'impact, revue d'architecture, génération de tests, refactoring multi-fichiers et débogage avancé.
* **Concepts Abordés** : Développement assisté par l'IA, Pair-programming avec une IA.