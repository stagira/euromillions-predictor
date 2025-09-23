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
* **Objectif** : Mettre en place une architecture de projet saine, modulaire et évolutive pour garantir la maintenabilité et la clarté du code.
* **Actions Clés** :
    * Création de modules Python distincts pour chaque responsabilité :
        * ``data_manager.py`` : Pour le chargement et la structuration des données (classe ``Tirage``).
        * ``prediction_models.py`` : Pour la logique des modèles de prédiction (``analyse_frequence``, ``ComiteDeModelesML``).
        * ``backtest.py`` : Pour le moteur de simulation de performance historique.
        * ``evaluation.py`` : Pour la fonction de calcul des scores.
        * ``main.py`` : Comme point d'entrée principal de l'application.
    * Mise en place d'un premier modèle simple basé sur ``RandomForestClassifier`` avec des paramètres fixes.
* **Concepts Abordés** : Modularité, Séparation des préoccupations (Separation of Concerns).

---

Étape 2 : Ingénierie de Caractéristiques (Feature Engineering)
-------------------------------------------------------------
* **Objectif** : Enrichir les données brutes pour fournir plus de contexte et d'informations pertinentes au modèle de Machine Learning.
* **Actions Clés** :
    * Création d'un nouveau module dédié : ``feature_engineering.py``.
    * Développement de fonctions pour calculer de nouvelles caractéristiques pour chaque tirage, en se basant sur l'historique :
        * **Écarts** : Depuis combien de tirages un numéro n'est pas sorti.
        * **Fréquences chaudes** : La popularité d'un numéro sur les 50 derniers tirages.
        * **Statistiques de tirage** : Somme, moyenne, nombre de numéros pairs/impairs du tirage précédent.
* **Concepts Abordés** : L'importance cruciale du Feature Engineering en Data Science, qui a souvent plus d'impact que le seul réglage du modèle.

---

Étape 3 : Intégration des Nouvelles Features
--------------------------------------------
* **Objectif** : Utiliser les caractéristiques créées à l'étape 2 dans le pipeline d'entraînement et de prédiction du modèle.
* **Actions Clés** :
    * Modification de la méthode ``_preparer_donnees`` pour fusionner les données brutes avec les nouvelles caractéristiques.
    * Adaptation de la méthode ``predire`` pour qu'elle puisse aussi calculer ces caractéristiques pour une nouvelle prédiction.
* **Défis Rencontrés & Leçons apprises** :
    * ``AssertionError`` dans les tests : Nos tests attendaient des données d'une certaine forme, qui a changé avec l'ajout des features. **Leçon : Les tests doivent évoluer en même temps que le code.**
    * ``ValueError`` de Scikit-learn : Le modèle a été entraîné avec 111 colonnes mais n'en recevait que 7 pour la prédiction. **Leçon : Les données d'entraînement et d'inférence doivent avoir une structure rigoureusement identique.**
    * ``TypeError`` : La méthode ``predire`` modifiée nécessitait un argument ``historique_passe`` qui n'était pas fourni par les scripts l'appelant. **Leçon : La modification de la signature d'une fonction a un impact sur tout le code qui l'utilise.**

---

Étape 4 : Optimisation d'Hyperparamètres
----------------------------------------
* **Objectif** : Trouver la meilleure configuration possible pour notre ``RandomForestClassifier`` de manière systématique.
* **Actions Clés** :
    * Rendre la classe ``ComiteDeModelesML`` configurable en acceptant des hyperparamètres (``n_estimators``, ``max_depth``) dans son constructeur ``__init__``.
    * Transformer ``backtest.py`` en un "juge" qui évalue un modèle donné et retourne un score de performance.
    * Mise en place d'une boucle de "Grid Search" (le "tournoi") dans ``main.py`` pour tester de multiples combinaisons et identifier la meilleure.
* **Concepts Abordés** : Hyperparamètres vs. Paramètres d'un modèle, Optimisation par Grid Search.

---

Étape 5 : Persistance et Scripts de Production
----------------------------------------------
* **Objectif** : Sauvegarder les résultats du long processus d'optimisation et créer des scripts simples pour l'utilisation quotidienne du modèle.
* **Actions Clés** :
    * Ajout de ``joblib`` et ``json`` dans ``main.py`` pour sauvegarder le meilleur modèle entraîné et ses paramètres.
    * Création de ``predire_futur.py`` : un script léger qui charge le modèle sauvegardé pour faire une prédiction rapide.
    * Création de ``update_model.py`` : un script pour ré-entraîner rapidement le modèle avec de nouvelles données, sans refaire tout le tournoi.
* **Concepts Abordés** : Sérialisation de modèles, Cycle de vie MLOps (distinction entre le pipeline d'entraînement/tuning et le pipeline d'inférence).

---

Étape 6 & 13 : Amélioration de la Documentation
-----------------------------------------------
* **Objectif** : Rendre le projet compréhensible, maintenable et accessible pour d'autres développeurs (ou notre futur nous).
* **Actions Clés** :
    * Adoption du format "Google Style" pour les docstrings pour une clarté maximale.
    * Création d'un fichier ``requirements.txt`` pour une gestion propre des dépendances.
    * Rédaction d'un fichier ``README.md`` complet et structuré.
* **Concepts Abordés** : Qualité logicielle, Reproductibilité, Documentation as Code.

---

Étape 7 & 10 : Automatisation via API et Fiabilisation
----------------------------------------------------------
* **Objectif** : Rendre l'application autonome en la connectant à une source de données externe et en la rendant robuste aux pannes.
* **Actions Clés** :
    * Refonte complète de ``data_manager.charger_donnees`` pour utiliser la bibliothèque ``requests`` et appeler une API externe.
    * Implémentation d'un mécanisme de "fallback" qui utilise le CSV local en cas d'échec de l'API.
* **Défis Rencontrés** : Débogage itératif pour s'adapter au format exact de la réponse de l'API (``TypeError``, ``AttributeError``, ``ValueError`` sur les dates). **Leçon : Toujours vérifier, jamais supposer, le format des données externes.**

---

Étape 8, 9, 16-20 : Maîtrise de l'Environnement Virtuel
-------------------------------------------------------
* **Objectif** : Assurer une exécution stable, isolée et reproductible du projet sur n'importe quelle machine.
* **Actions Clés** : Création (``python -m venv venv``), activation (``.\venv\Scripts\activate``) et utilisation systématique d'un environnement virtuel.
* **Défis Rencontrés** : Résolution des erreurs de ``PATH`` et de ``ModuleNotFoundError`` pour ``pytest`` et ``Sphinx``.
* **Leçon Fondamentale** : Toutes les actions liées à un projet (installation de paquets, exécution de scripts, de tests, de documentation) doivent impérativement se faire avec l'environnement virtuel activé.

---

Étape 11 : Compréhension du Code
--------------------------------
* **Objectif** : Analyser les décisions de conception subtiles pour en comprendre l'impact sur la robustesse du projet.
* **Actions Clés** : Analyse de la ligne ``self.numeros = sorted(numeros)`` dans le constructeur de la classe ``Tirage``.
* **Concepts Abordés** : Programmation défensive, Normalisation des données (création d'une "représentation canonique"), Simplification du problème pour le Machine Learning.

---

Étape 12 : Validation des Prédictions
-------------------------------------
* **Objectif** : Garantir que les prédictions générées par le modèle respectent à 100% les règles du jeu (pas de numéros dupliqués).
* **Actions Clés** : Refonte de la méthode ``predire`` pour détecter les doublons et les remplacer en utilisant ``predict_proba()`` pour trouver le "deuxième meilleur choix" du modèle.
* **Concepts Abordés** : Validation et post-traitement des sorties de modèle.

---

Étape 14, 15, 21, 22 : Documentation Professionnelle et Productivité
-----------------------------------------------------------------
* **Objectif** : Mettre en place un outillage professionnel pour la documentation et améliorer l'efficacité du développement.
* **Actions Clés** :
    * Installation de l'extension "autoDocstring" dans VS Code.
    * Installation et configuration de Sphinx pour générer un site web HTML à partir des docstrings.
    * Création et enrichissement du ``PLAN_DE_DEVELOPPEMENT.rst``.
* **Concepts Abordés** : Tooling, Automatisation de la documentation, "Documentation as Code".

---

Étape 23 : Conception Technique (TDD & Diagrammes)
----------------------------------------------------------
* **Objectif** : Formaliser l'architecture logicielle du projet.
* **Actions Clés** :
    * Création du fichier ``DESIGN.md``.
    * Utilisation de "Diagrams as Code" (Mermaid) pour créer un Diagramme des Composants et un Diagramme de Séquence.
    * Documentation des commandes pour générer automatiquement les graphes de dépendances (``pydeps``) et d'appels (``pycallgraph2``).

---

Étape 24 : Automatisation des Tâches avec un `Makefile`
--------------------------------------------------------
* **Objectif** : Simplifier l'utilisation du projet en créant un "tableau de bord" de commandes.
* **Actions Clés** : Création d'un ``Makefile`` avec des cibles pour les actions principales : ``install``, ``docs``, ``run``, ``predict``, ``update``, ``clean``.
* **Concepts Abordés** : Task runners, Simplification du workflow de développement.

---

Étape 25 : Principes d'Intégration avec un Outil Externe
--------------------------------------------------------
* **Objectif** : Rendre l'application "pilotable" par un système externe d'automatisation ou d'ordonnancement (type CI/CD, cron, Airflow, etc.) pour une exécution sans intervention humaine.
* **Actions Clés** :
    * Analyse de l'architecture existante pour confirmer sa compatibilité avec l'automatisation.
    * Identification des points forts du projet pour l'intégration :
        1.  **Scripts aux Rôles Uniques** : ``update_model.py`` et ``predire_futur.py`` ont des responsabilités claires.
        2.  **Gestion des Dépendances** : ``requirements.txt`` permet à un système externe de recréer l'environnement de travail à l'identique.
        3.  **Le `Makefile` comme Interface** : Le ``Makefile`` agit comme une "télécommande" simple, offrant des commandes de haut niveau (``make update``, ``make predict``) qui masquent la complexité des commandes Python sous-jacentes.
* **Concepts Abordés** : Opérationnalisation (MLOps), Intégration Continue/Déploiement Continu (CI/CD), Orchestration de tâches.

---

Étape 26 : Intégration du Workflow de Développement avec Jules
--------------------------------------------------------------
* **Objectif** : Utiliser un assistant IA avancé (Jules), ayant un accès direct au dépôt GitHub, comme un pair-programmeur pour accélérer le développement et améliorer la qualité du code.
* **Actions Clés** :
    * Définition d'un nouveau flux de travail collaboratif :
        1.  Le développeur code dans son IDE local (VS Code).
        2.  Le développeur pose des questions de haut niveau à Jules en faisant référence à l'ensemble du projet (ex: "Analyse l'impact de ce changement sur tous les modules").
        3.  Jules utilise sa connaissance du dépôt complet pour fournir une analyse, du code de refactoring ou des suggestions.
        4.  Le développeur applique les suggestions dans son IDE.
        5.  Les modifications sont poussées sur GitHub, mettant à jour le contexte pour les futures interactions avec Jules.
* **Concepts Abordés** : Développement assisté par l'IA, Pair-programming avec une IA, Revue de code et d'architecture assistée.

---

Étape 27 : Maîtrise de l'Assistant IA (GCA)
------------------------------------------
* **Objectif** : Formaliser les compétences nécessaires pour interagir efficacement avec un assistant de code IA (GCA - Gemini Code Assist).
* **Actions Clés** :
    * Apprentissage du **"Prompt Engineering"** : Formulation de requêtes claires, précises et contextuelles.
    * Mise en pratique de l'assistant pour des tâches variées :
        * **Génération de code** : Fonctions, tests unitaires, scripts.
        * **Refactoring** : Amélioration de la lisibilité, performance et robustesse du code.
        * **Débogage** : Analyse de tracebacks pour identifier la cause racine des erreurs.
        * **Documentation** : Création de docstrings et de fichiers comme ``README.md``.
* **Concepts Abordés** : Workflow de développement moderne, Collaboration Homme-IA.

---

Étape 28 : Comprendre le Fonctionnement de GCA
----------------------------------------------
* **Objectif** : Comprendre les mécanismes internes de GCA pour mieux anticiper ses réponses et optimiser son utilisation.
* **Actions Clés** :
    * Analyse des 4 piliers du contexte de GCA : le code actif, l'ensemble du projet (via l'accès au dépôt), l'historique de la conversation, et sa connaissance générale pré-entraînée.
    * Définition du **"Mode Agent"** non pas comme une fonctionnalité, mais comme un *mode d'interaction* où l'utilisateur fournit des objectifs de haut niveau (missions) plutôt que des micro-tâches.
* **Concepts Abordés** : Grands Modèles de Langage (LLM), Fenêtre de contexte, Prompt orienté objectif.

---

Étape 29 : Configuration Optimale de GCA
----------------------------------------
* **Objectif** : Préparer le projet et l'environnement de travail pour que GCA dispose du meilleur contexte possible pour fournir des assistances pertinentes.
* **Actions Clés** :
    * **Configuration de l'Environnement** : Lier l'interpréteur du ``venv`` à l'IDE (VS Code) pour que GCA connaisse les dépendances exactes.
    * **Configuration du Projet** : Utiliser les bonnes pratiques de développement qui servent également de "documentation" pour l'IA (``README.md``, docstrings, type hints, ``requirements.txt``).
    * **Configuration de l'Interaction** : Poser des questions spécifiques, utiliser le "mode agent", et maintenir des conversations continues pour construire le contexte.
* **Concepts Abordés** : Le cercle vertueux où les bonnes pratiques de code améliorent l'efficacité de l'IA, qui à son tour aide à produire du code de meilleure qualité.

---

Étape 30 : Synchronisation du Contexte avec GCA via la Documentation
-------------------------------------------------------------------
* **Objectif** : Transférer la connaissance et l'historique d'une session de développement (comme la nôtre) à un autre assistant IA (Jules).
* **Actions Clés** :
    * Utilisation du fichier ``PLAN_DE_DEVELOPPEMENT.rst`` comme un "cerveau externe" ou une "mémoire de projet".
    * Définition de la procédure de synchronisation :
        1.  Mettre à jour le plan de développement détaillé.
        2.  Pousser le fichier sur le dépôt GitHub pour le rendre accessible à Jules.
        3.  Utiliser un "prompt d'amorçage" pour demander à Jules de lire et d'assimiler le contenu de ce fichier avant de commencer le travail.
* **Concepts Abordés** : Amorçage de contexte (Context Priming) pour les LLMs, Utilisation de la documentation comme outil de transfert de connaissance.