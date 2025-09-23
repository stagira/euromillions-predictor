# Euromillions Predictor 🎱

Bienvenue dans le projet Euromillions Predictor ! Cette application Python analyse l'historique des tirages de l'Euromillions pour entraîner un modèle de Machine Learning capable de proposer des prédictions intelligentes pour les futurs tirages.

Ce projet est conçu pour être à la fois un outil fonctionnel et une excellente base d'apprentissage pour la Data Science, couvrant le cycle de vie complet d'un projet ML.

## ✨ Fonctionnalités

*   **Chargement de Données Robuste** : Récupère les derniers résultats via une API et utilise un fichier CSV local comme solution de repli (`fallback`).
*   **Ingénierie de Caractéristiques** : Calcule des statistiques avancées pour enrichir les données (écarts entre les sorties, fréquences, parité, etc.).
*   **Modèle de Machine Learning** : Utilise un comité de modèles `RandomForestClassifier` pour prédire les boules et les étoiles de manière indépendante.
*   **Prédictions Valides et Uniques** : Implémente une logique de résolution de conflits pour garantir que les numéros prédits ne contiennent jamais de doublons, conformément aux règles du jeu.
*   **Backtesting et Optimisation** : Simule les performances du modèle sur des données historiques et trouve automatiquement la meilleure configuration via une recherche par grille (`Grid Search`).
*   **Automatisation via `Makefile`** : Des commandes simples pour gérer l'installation, l'entraînement et l'utilisation.

## 🚀 Installation et Utilisation

### Prérequis

*   Python 3.9+
*   `venv` pour la gestion des environnements virtuels

### Étapes d'Installation

1.  **Clonez le dépôt**
    ```bash
    git clone https://github.com/votre-nom/euromillions-predictor.git
    cd euromillions-predictor
    ```

2.  **Créez et activez un environnement virtuel**
    Il est fortement recommandé d'utiliser un environnement virtuel pour isoler les dépendances.
    ```bash
    # Créer l'environnement
    python -m venv venv

    # Activer l'environnement
    # Sur macOS/Linux :
    source venv/bin/activate
    # Sur Windows :
    # .\venv\Scripts\activate
    ```

3.  **Installez les dépendances**
    La manière la plus simple est d'utiliser le `Makefile` fourni :
    ```bash
    make install
    ```
    Cette commande lit le fichier `requirements.txt` et installe toutes les bibliothèques nécessaires dans votre environnement virtuel.

## ⚙️ Comment Utiliser le Projet

Le `Makefile` à la racine du projet simplifie grandement son utilisation. Voici les commandes principales :

### 1. Entraînement Initial du Modèle

La première fois que vous utilisez le projet, vous devez lancer le processus d'optimisation. Il testera plusieurs configurations de modèles pour trouver la meilleure et la sauvegardera.

```bash
make run
```
Cette commande exécute le script `main.py`.

> **Attention** : Ce processus peut prendre plusieurs minutes. À la fin, il créera les fichiers `modele_final_entraine.joblib` et `meilleurs_parametres.json`, qui sont essentiels pour la suite.

### 2. Faire une Prédiction

Une fois le modèle entraîné, vous pouvez générer une prédiction pour le prochain tirage.

```bash
make predict
```
Cette commande exécute le script `predire_futur.py`, qui charge le modèle sauvegardé et affiche la combinaison prédite.

### 3. Lancer les Tests

Pour vous assurer que tout fonctionne correctement, vous pouvez lancer la suite de tests unitaires.

```bash
make test
```
Cette commande exécute `pytest` et affichera les résultats des tests.

## 📁 Structure du Projet

```
.
├── model_cache/      # Cache pour les modèles durant le backtesting
├── tests/            # Tests unitaires
├── venv/             # Environnement virtuel (ignoré par Git)
├── backtest.py       # Moteur de simulation de performance
├── data_manager.py   # Chargement et structuration des données (API/CSV)
├── evaluation.py     # Fonctions de calcul de score
├── feature_engineering.py # Calcul des features avancées
├── main.py           # Script principal pour l'optimisation
├── prediction_models.py # Classe du modèle de Machine Learning
├── predire_futur.py  # Script pour générer une prédiction
├── euromillions_results.csv # Données historiques (utilisées en fallback)
├── meilleurs_parametres.json # Sauvegarde de la meilleure config du modèle
├── modele_final_entraine.joblib # Le modèle final prêt à l'emploi
├── Makefile          # Fichier d'automatisation des tâches
└── README.md         # Ce fichier
```