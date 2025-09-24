# predire_futur.py
import joblib
import data_manager
import os
import logging
import config_manager

# --- Configuration de la Journalisation ---
log_level = config_manager.get_log_level()
logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')

prediction_log_file = config_manager.get_prediction_log_file()
prediction_logger = logging.getLogger('PredictionLogger')
prediction_logger.setLevel(logging.INFO)
prediction_logger.propagate = False
pred_handler = logging.FileHandler(prediction_log_file, mode='a')
pred_formatter = logging.Formatter('%(asctime)s - %(message)s')
pred_handler.setFormatter(pred_formatter)
prediction_logger.addHandler(pred_handler)

def lancer_prediction():
    """
    Charge le modèle entraîné et prédit le prochain tirage de l'Euromillions.
    """
    logging.info("--- 🔮 Lancement du Script de Prédiction ---")

    fichier_modele = 'modele_final_entraine.joblib'
    fichier_donnees = 'euromillions_results.csv'

    if not os.path.exists(fichier_modele):
        logging.error(f"Le fichier du modèle '{fichier_modele}' est introuvable.")
        logging.error("   -> Veuillez d'abord lancer 'main.py' pour entraîner et sauvegarder un modèle.")
        return

    if not os.path.exists(fichier_donnees):
        logging.error(f"Le fichier de données '{fichier_donnees}' est introuvable.")
        return

    logging.info(f"🧠 Chargement du modèle depuis '{fichier_modele}'...")
    try:
        modele = joblib.load(fichier_modele)
    except Exception as e:
        logging.error(f"Erreur lors du chargement du modèle : {e}")
        return
        
    logging.info("📊 Chargement de l'historique des tirages...")
    historique = data_manager.charger_donnees(fichier_donnees)
    
    if not historique:
        logging.error("L'historique des tirages est vide.")
        return

    dernier_tirage_connu = historique[0]
    historique_passe = historique[1:]
    
    logging.info(f"🗓️ Utilisation du dernier tirage du {dernier_tirage_connu.date} comme base de prédiction.")

    logging.info("\n⏳ Le comité de modèles réfléchit à la meilleure combinaison...")
    
    pred_boules, pred_etoiles = modele.predire(dernier_tirage_connu, historique_passe)

    logging.info("\n--- 🎉 Résultat de la Prédiction ---")
    logging.info(f"   - 🎱 Boules : {pred_boules}")
    logging.info(f"   - ⭐ Étoiles : {pred_etoiles}")
    logging.warning("\nN'oubliez pas que ce sont des prédictions statistiques et non une garantie de succès.")

    prediction_logger.info(f"Prédiction - Boules: {pred_boules}, Etoiles: {pred_etoiles}")

if __name__ == "__main__":
    lancer_prediction()
    logging.info("\n--- Script terminé ---")