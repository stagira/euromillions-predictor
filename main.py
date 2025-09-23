# main.py
import data_manager
import prediction_models

print("--- Démarrage du Prédicteur Euromillions ---")
historique = data_manager.charger_donnees()
print(f"✅ {len(historique)} tirages ont été chargés depuis le fichier.")

if historique:
    dernier_tirage = historique[0]
    print("\n🔎 Dernier tirage enregistré :")
    print(f"   - Date : {dernier_tirage.date}")
    print(f"   - Numéros : {dernier_tirage.numeros}")
    print(f"   - Étoiles : {dernier_tirage.etoiles}")

    # --- Modèle Statistique ---
    print("\n🔥 Analyse des numéros les plus fréquents (Modèle Historien) :")
    numeros_chauds = prediction_models.analyse_frequence(historique)
    print(f"   - Les 5 numéros les plus sortis sont : {numeros_chauds}")

    # --- Modèle de Machine Learning ---
    # 1. On crée une instance de notre modèle
    modele_ml = prediction_models.ModeleRandomForest()
    
    # 2. On l'entraîne avec tout l'historique
    modele_ml.entrainer(historique)
    
    # 3. On lui demande une prédiction basée sur le dernier tirage connu
    prediction_ml = modele_ml.predire(dernier_tirage)
    print("\n🤖 Prédiction du Machine Learning (Modèle Détective) :")
    print(f"   - {prediction_ml}")

print("\n--- Application terminée ---")