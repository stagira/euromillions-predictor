# main.py
import data_manager
import prediction_models # 👈 On importe notre nouveau module

print("--- Démarrage du Prédicteur Euromillions ---")

historique = data_manager.charger_donnees()

print(f"✅ {len(historique)} tirages ont été chargés depuis le fichier.")

# On affiche les données du tirage le plus récent
if historique:
    dernier_tirage = historique[0]
    print("\n🔎 Dernier tirage enregistré :")
    print(f"   - Date : {dernier_tirage.date}")
    print(f"   - Numéros : {dernier_tirage.numeros}")
    print(f"   - Étoiles : {dernier_tirage.etoiles}")

    # 👇 On ajoute notre nouvelle analyse ici
    print("\n🔥 Analyse des numéros les plus fréquents (Numéros Chauds) :")
    numeros_chauds = prediction_models.analyse_frequence(historique)
    print(f"   - Les 5 numéros les plus sortis sont : {numeros_chauds}")


print("\n--- Application terminée ---")