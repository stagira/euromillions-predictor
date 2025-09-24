# main.py
import data_manager
import backtest
import prediction_models
import itertools
import json
import joblib
import logging
import time
import config_manager

# --- Configuration de la Journalisation ---
log_level = config_manager.get_log_level()
logging.basicConfig(
    level=log_level,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

report_file = config_manager.get_report_file()
report_logger = logging.getLogger('RunReport')
report_logger.setLevel(logging.INFO)
report_logger.propagate = False
file_handler = logging.FileHandler(report_file, mode='w')
file_formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
file_handler.setFormatter(file_formatter)
report_logger.addHandler(file_handler)

# --- Démarrage de l'application ---
start_time = time.time()
logging.info("--- Démarrage du Prédicteur Euromillions ---")
report_logger.info(f"Rapport d'exécution du {time.strftime('%Y-%m-%d %H:%M:%S')}")
report_logger.info("="*40)

historique = data_manager.charger_donnees()
logging.info(f"✅ {len(historique)} tirages ont été chargés.")

if not historique or len(historique) < 250:
    logging.error("Pas assez de données pour lancer une simulation.")
else:
    msg = "\n--- 🏆 Lancement de l'optimisation des hyperparamètres ---"
    logging.info(msg)
    report_logger.info(msg)

    parametres_a_tester = {
        'n_estimators': [50, 100],
        'max_depth': [10, 20, None]
    }

    meilleurs_parametres = None
    meilleur_score = -1

    keys, values = zip(*parametres_a_tester.items())
    combinaisons = [dict(zip(keys, v)) for v in itertools.product(*values)]

    msg = f"{len(combinaisons)} combinaisons de paramètres à tester..."
    logging.info(msg)
    report_logger.info(msg)

    for i, params in enumerate(combinaisons, 1):
        msg = f"\nTest de la combinaison {i}/{len(combinaisons)} : {params}"
        logging.info(msg)
        report_logger.info(msg)
        
        modele_candidat = prediction_models.ComiteDeModelesML(**params)
        score_boules, score_etoiles = backtest.lancer_backtest(modele_candidat, historique, 50)
        
        msg = f"   - Résultat : Score moyen Boules = {score_boules:.2f} / 5"
        logging.info(msg)
        report_logger.info(msg)

        if score_boules > meilleur_score:
            meilleur_score = score_boules
            meilleurs_parametres = params
            logging.info("   -> ✨ Nouvelle meilleure combinaison trouvée !")
            report_logger.info("   -> ✨ Nouvelle meilleure combinaison trouvée !")

    msg = "\n--- ✅ Optimisation terminée ---"
    logging.info(msg)
    report_logger.info(msg)

    msg = f"La meilleure combinaison de paramètres est : {meilleurs_parametres}"
    logging.info(msg)
    report_logger.info(msg)

    msg = f"Avec un score moyen de : {meilleur_score:.2f} / 5"
    logging.info(msg)
    report_logger.info(msg)
    
    if meilleurs_parametres:
        msg = "\n--- 💾 Sauvegarde du meilleur modèle et des paramètres ---"
        logging.info(msg)
        report_logger.info(msg)

        with open('meilleurs_parametres.json', 'w') as f:
            json.dump(meilleurs_parametres, f, indent=4)
        logging.info("   - Meilleurs paramètres sauvegardés dans 'meilleurs_parametres.json'")

        logging.info("   - Entraînement du modèle final sur tout l'historique disponible...")
        modele_final = prediction_models.ComiteDeModelesML(**meilleurs_parametres)
        modele_final.entrainer(historique[1:])

        joblib.dump(modele_final, 'modele_final_entraine.joblib')
        logging.info("   - Modèle final entraîné et sauvegardé dans 'modele_final_entraine.joblib'")

end_time = time.time()
duration = end_time - start_time
logging.info("\n--- Application terminée ---")
report_logger.info("="*40)
report_logger.info(f"Processus terminé en {duration:.2f} secondes.")