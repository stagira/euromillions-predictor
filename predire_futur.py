# predire_futur.py
import joblib
import data_manager
import os

def lancer_prediction():
    """
    Charge le modèle entraîné et prédit le prochain tirage de l'Euromillions.
    """
    print("--- 🔮 Lancement du Script de Prédiction ---")

    # --- 1. Vérification des fichiers requis ---
    fichier_modele = 'modele_final_entraine.joblib'
    fichier_donnees = 'euromillions_results.csv'

    if not os.path.exists(fichier_modele):
        print(f"❌ Erreur : Le fichier du modèle '{fichier_modele}' est introuvable.")
        print("   -> Veuillez d'abord lancer 'main.py' pour entraîner et sauvegarder un modèle.")
        return # Arrête le script si le modèle n'existe pas

    if not os.path.exists(fichier_donnees):
        print(f"❌ Erreur : Le fichier de données '{fichier_donnees}' est introuvable.")
        return

    # --- 2. Chargement du modèle et des données ---
    print(f"🧠 Chargement du modèle depuis '{fichier_modele}'...")
    try:
        modele = joblib.load(fichier_modele)
    except Exception as e:
        print(f"❌ Erreur lors du chargement du modèle : {e}")
        return
        
    print("📊 Chargement de l'historique des tirages...")
    historique = data_manager.charger_donnees(fichier_donnees)
    
    if not historique:
        print("❌ Erreur : L'historique des tirages est vide.")
        return

    # --- 3. Préparation des données pour la prédiction ---
    # Le modèle a besoin du tout dernier tirage connu pour prédire le suivant.
    dernier_tirage_connu = historique[0]
    
    # L'historique passé est TOUT l'historique SAUF le dernier tirage.
    historique_passe = historique[1:]
    
    print(f"🗓️ Utilisation du dernier tirage du {dernier_tirage_connu.date} comme base de prédiction.")

    # --- 4. Exécution de la prédiction ---
    print("\n⏳ Le comité de modèles réfléchit à la meilleure combinaison...")
    
    # On ajoute le deuxième argument manquant : historique_passe
    pred_boules, pred_etoiles = modele.predire(dernier_tirage_connu, historique_passe)
# ...

    # --- 5. Affichage du résultat ---
    print("\n--- 🎉 Résultat de la Prédiction ---")
    print(f"   - 🎱 Boules : {pred_boules}")
    print(f"   - ⭐ Étoiles : {pred_etoiles}")
    print("\nN'oubliez pas que ce sont des prédictions statistiques et non une garantie de succès.")

# Ce bloc permet d'exécuter la fonction seulement si on lance le script directement
if __name__ == "__main__":
    lancer_prediction()
    print("\n--- Script terminé ---")