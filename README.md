# Euromillions Predictor 🎱

Ce projet est une application Python qui analyse l'historique des tirages de l'Euromillions pour entraîner un modèle de Machine Learning capable de proposer des prédictions pour les futurs tirages.

L'application est conçue pour être modulaire et évolutive, servant à la fois d'outil de prédiction et de projet d'apprentissage en Data Science.

## ✨ Fonctionnalités

* **Chargement Automatique des Données** : Récupère les derniers résultats de tirage via une API externe, avec un fichier CSV local comme solution de repli.
* **Ingénierie de Caractéristiques (Feature Engineering)** : Calcule des statistiques avancées pour enrichir les données (écarts, fréquences chaudes, somme, parité...).
* **Modèle de Machine Learning** : Utilise un comité de modèles `RandomForestClassifier` pour prédire les boules et les étoiles.
* **Backtesting Robuste** : Simule les performances du modèle sur des données historiques pour une évaluation fiable.
* **Optimisation d'Hyperparamètres** : Trouve automatiquement la meilleure configuration pour le modèle via un "tournoi" (Grid Search).
* **Prédictions Valides** : La logique de prédiction garantit que les numéros prédits sont uniques, conformément aux règles du jeu.
* **Cycle de Vie du Modèle** : Scripts séparés pour l'optimisation, la mise à jour et la prédiction.

## 🚀 Installation

Suivez ces étapes pour mettre en place l'environnement de développement.

1.  **Clonez le dépôt**
    ```bash
    # Remplacez par l'URL de votre dépôt
    git clone [https://github.com/votre-nom/euromillions-predictor.git](https://github.com/votre-nom/euromillions-predictor.git)
    cd euromillions-predictor
    ```

2.  **Créez un environnement virtuel**
    Il est fortement recommandé d'utiliser un environnement virtuel pour isoler les dépendances du projet.
    ```bash
    python -m venv venv
    ```

3.  **Activez l'environnement virtuel**
    * Sur Windows :
        ```bash
        .\venv\Scripts\activate
        ```
    * Sur macOS/Linux :
        ```bash
        source venv/bin/activate
        ```

4.  **Installez les dépendances**
    Toutes les bibliothèques nécessaires sont listées dans `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```

## ⚙️ Utilisation

Le projet est divisé en plusieurs scripts pour différentes tâches.

### 1. Optimisation Initiale du Modèle (`main.py`)

Ce script lance le processus le plus long : le "tournoi" de modèles pour trouver les meilleurs hyperparamètres, puis sauvegarde le modèle optimisé. **Lancez ce script en premier.**

```bash
python main.py
```
> **Note** : Ce processus peut prendre plusieurs minutes. Il créera les fichiers `modele_final_entraine.joblib` et `meilleurs_parametres.json`.

### 2. Mise à Jour du Modèle (`update_model.py`)

Après avoir ajouté de nouveaux tirages à vos données (si vous mettez à jour le CSV manuellement), ce script ré-entraîne rapidement le modèle avec les dernières informations, en utilisant les meilleurs paramètres déjà trouvés.

```bash
python update_model.py
```

### 3. Faire une Prédiction (`predire_futur.py`)

Pour obtenir une prédiction pour le prochain tirage en utilisant le modèle entraîné.

```bash
python predire_futur.py
```

## ✅ Tests

Pour vous assurer que tout fonctionne correctement, vous pouvez lancer la suite de tests unitaires avec `pytest`.

```bash
pytest -v
```

## 📁 Structure du Projet

```
.
├── model_cache/      # Cache pour les modèles durant le backtesting
├── tests/            # Tests unitaires
├── venv/             # Environnement virtuel
├── backtest.py       # Moteur de simulation de performance
├── data_manager.py   # Chargement et structuration des données (API/CSV)
├── evaluation.py     # Fonctions de calcul de score
├── feature_engineering.py # Calcul des features avancées
├── main.py           # Script principal pour l'optimisation
├── prediction_models.py # Classe du modèle de Machine Learning
├── predire_futur.py  # Script pour générer une prédiction
├── update_model.py   # Script pour mettre à jour le modèle
├── euromillions_results.csv # Données historiques (fallback)
├── meilleurs_parametres.json # Sauvegarde de la meilleure config du modèle
├── modele_final_entraine.joblib # Le modèle final prêt à l'emploi
└── README.md         # Ce fichier
```