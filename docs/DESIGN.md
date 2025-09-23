# Document de Conception Technique - Euromillions Predictor

Ce document décrit l'architecture logicielle, les composants clés et les flux de données de l'application `euromillions-predictor`. Il est destiné à servir de référence pour les développeurs et les contributeurs du projet.

## 1. Diagramme des Composants (Component Diagram)

Ce diagramme offre une vue d'ensemble de l'architecture. Il montre les principaux blocs logiques de l'application et comment ils interagissent.

```mermaid
graph TD
    subgraph "Interface Utilisateur"
        CLI[Terminal Utilisateur]
    end

    subgraph "Points d'Entrée (Scripts)"
        A[main.py] -.-> B(Optimisation & Entraînement Initial);
        C[predire_futur.py] -.-> D(Génération de Prédiction);
        E[update_model.py] -.-> F(Mise à Jour du Modèle);
    end

    subgraph "Coeur Logique (Modules)"
        G[prediction_models.py] -- Contient --> H(ComiteDeModelesML);
        I[data_manager.py] -- Fournit les données;
        L[feature_engineering.py] -- Calcule les features;
        M[backtest.py] -- Évalue la performance;
        N[evaluation.py] -- Calcule les scores;
    end

    subgraph "Sources de Données & Artefacts"
        J[API Externe];
        K[euromillions_results.csv];
        O[modèle_final_entrainé.joblib];
        P[meilleurs_parametres.json];
    end

    CLI -- Lance --> A;
    CLI -- Lance --> C;
    CLI -- Lance --> E;

    B -- Utilise --> M;
    B -- Crée --> O;
    B -- Crée --> P;

    D -- Charge --> O;
    D -- Utilise --> H;
    
    F -- Lit --> P;
    F -- Met à jour --> O;

    H -- Dépend de --> L;
    H -- Dépend de --> I;
    M -- Dépend de --> H;
    M -- Dépend de --> N;
    
    I -- Appelle --> J;
    I -- Fallback sur --> K;
```

---

## 2. Diagramme de Séquence (Sequence Diagram)

Ce diagramme illustre les interactions pas à pas pour le cas d'utilisation le plus courant : **lancer une prédiction**.

```mermaid
sequenceDiagram
    participant User as Utilisateur
    participant Predicteur as predire_futur.py
    participant Modele as modele_final_entraine.joblib
    participant Data as data_manager.py
    participant API as API Externe

    User->>+Predicteur: Lancement du script `python predire_futur.py`
    
    Predicteur->>+Modele: Chargement du modèle (joblib.load)
    Modele-->>-Predicteur: Instance de ComiteDeModelesML prête
    
    Predicteur->>+Data: Appelle charger_donnees()
    Data->>+API: Requête GET sur /draws
    API-->>-Data: Réponse JSON (historique complet)
    Data-->>-Predicteur: Retourne une liste d'objets Tirage
    
    Note over Predicteur: Prépare le dernier tirage et l'historique passé
    
    Predicteur->>Modele: Appelle predire(dernier_tirage, historique_passe)
    Note over Modele: Calcule les features, prédit avec chaque sous-modèle, et valide l'unicité des numéros.
    Modele-->>-Predicteur: Prédiction finale (boules, etoiles)
    
    Predicteur-->>-User: Affiche la prédiction dans le terminal
```

---

## 3. Graphe de Dépendances des Modules (Dependency Graph)

Ce diagramme montre les relations d'importation entre les différents fichiers Python du projet. Il est très utile pour visualiser le couplage entre les modules.

Ce diagramme est généré **automatiquement** pour garantir qu'il soit toujours à jour avec le code.

* **Outil Requis** : `pydeps`
* **Installation** : `pip install pydeps`
* **Commande de Génération** (à lancer depuis la racine du projet) :
    ```bash
    pydeps --cluster --rankdir LR -o dependency_graph.svg .
    ```
Cette commande générera un fichier image `dependency_graph.svg` représentant les dépendances actuelles.

---

## 4. Graphe d'Appels (Call Graph)

Ce diagramme montre le flux d'exécution réel du programme, en visualisant quelles fonctions en appellent d'autres lors d'un scénario spécifique.

Ce diagramme est également généré **automatiquement**.

* **Outil Requis** : `pycallgraph2` et `Graphviz`
* **Installation** :
    1.  Installez Graphviz (un logiciel tiers) en suivant les instructions pour votre système d'exploitation.
    2.  Installez la bibliothèque Python : `pip install pycallgraph2`
* **Commande de Génération** (pour le scénario de prédiction) :
    ```bash
    pycallgraph graphviz -- predire_futur.py
    ```
Cette commande exécutera le script et générera une image `pycallgraph.png` qui détaille la séquence complète des appels de fonctions.