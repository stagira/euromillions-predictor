# main.py
import data_manager
import backtest
import prediction_models
import itertools # On importe un outil pour nous aider à créer les combinaisons
import json     # <--- AJOUTER pour la sauvegarde des paramètres
import joblib   # <--- AJOUTER pour la sauvegarde du modèle

print("--- Démarrage du Prédicteur Euromillions ---")
historique = data_manager.charger_donnees()
print(f"✅ {len(historique)} tirages ont été chargés.")

if not historique or len(historique) < 250:
    print("Pas assez de données pour lancer une simulation.")
else:
    # --- Début de la boucle d'optimisation (le "Tournoi") ---
    print("\n--- 🏆 Lancement de l'optimisation des hyperparamètres ---")

    # 1. Définir la grille des paramètres à tester
    parametres_a_tester = {
        'n_estimators': [50, 100],      # Nombre d'arbres
        'max_depth': [10, 20, None]       # Profondeur max des arbres (None = illimité)
    }

    # Préparation pour stocker les résultats
    meilleurs_parametres = None
    meilleur_score = -1

    # Créer toutes les combinaisons possibles de paramètres
    keys, values = zip(*parametres_a_tester.items())
    combinaisons = [dict(zip(keys, v)) for v in itertools.product(*values)]

    print(f"{len(combinaisons)} combinaisons de paramètres à tester...")

    # 2. Boucle sur chaque combinaison
    for params in combinaisons:
        print(f"\nTest de la combinaison : {params}")
        
        # Crée un "champion" avec ces paramètres spécifiques
        modele_candidat = prediction_models.ComiteDeModelesML(**params)
        
        # Lance le backtest pour ce champion
        score_boules, score_etoiles = backtest.lancer_backtest(modele_candidat, historique, 50)
        
        print(f"   - Résultat : Score moyen Boules = {score_boules:.2f} / 5")

        # 3. On garde en mémoire le meilleur
        if score_boules > meilleur_score:
            meilleur_score = score_boules
            meilleurs_parametres = params
            print(f"   -> ✨ Nouvelle meilleure combinaison trouvée !")

    # --- Fin de l'optimisation ---
    print("\n--- ✅ Optimisation terminée ---")
    print(f"La meilleure combinaison de paramètres est : {meilleurs_parametres}")
    print(f"Avec un score moyen de : {meilleur_score:.2f} / 5")
    
    # --- Sauvegarde des résultats ---
    if meilleurs_parametres:
        print("\n--- 💾 Sauvegarde du meilleur modèle et des paramètres ---")

        # 1. Sauvegarder les meilleurs paramètres dans un fichier JSON
        with open('meilleurs_parametres.json', 'w') as f:
            json.dump(meilleurs_parametres, f, indent=4)
        print("   - Meilleurs paramètres sauvegardés dans 'meilleurs_parametres.json'")

        # 2. Créer le modèle final avec ces paramètres et l'entraîner sur TOUTES les données disponibles
        print("   - Entraînement du modèle final sur tout l'historique disponible...")
        modele_final = prediction_models.ComiteDeModelesML(**meilleurs_parametres)
        
        # On l'entraîne avec toutes les données qu'on peut, sauf le tout dernier tirage qui servira de point de départ à la prédiction
        modele_final.entrainer(historique[1:])

        # 3. Sauvegarder l'objet modèle entraîné
        joblib.dump(modele_final, 'modele_final_entraine.joblib')
        print("   - Modèle final entraîné et sauvegardé dans 'modele_final_entraine.joblib'")



print("\n--- Application terminée ---")