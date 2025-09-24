# backtest.py
import data_manager
import prediction_models
import evaluation
import logging

def lancer_backtest(modele_a_tester, historique_complet: list[data_manager.Tirage], nombre_de_tests: int):
    """
    Lance une simulation de backtesting pour un MODÈLE DONNÉ.
    Retourne les scores moyens pour les boules et les étoiles.
    """
    logging.info(f"--- 🚀 Lancement du Backtesting sur les {nombre_de_tests} derniers tirages ---")
    scores_boules = []
    scores_etoiles = []

    for i in range(nombre_de_tests):
        tirage_a_deviner = historique_complet[i]
        tirage_precedent_pour_predire = historique_complet[i + 1]
        donnees_entrainement = historique_complet[i + 2:]

        if len(donnees_entrainement) < 200:
            logging.warning(f"Arrêt du backtest à l'itération {i} car la taille de l'historique d'entraînement est insuffisante.")
            break

        logging.debug(f"Backtest itération {i+1}/{nombre_de_tests}: entraînement sur {len(donnees_entrainement)} tirages.")

        modele_a_tester.entrainer(donnees_entrainement) 
        pred_boules, pred_etoiles = modele_a_tester.predire(tirage_precedent_pour_predire, donnees_entrainement)
        
        score_b, score_e = evaluation.calculer_score(pred_boules, tirage_a_deviner.numeros, pred_etoiles, tirage_a_deviner.etoiles)
        scores_boules.append(score_b)
        scores_etoiles.append(score_e)

    score_moyen_boules = sum(scores_boules) / len(scores_boules) if scores_boules else 0
    score_moyen_etoiles = sum(scores_etoiles) / len(scores_etoiles) if scores_etoiles else 0
    
    logging.info("--- ✅ Backtesting terminé ---")
    return score_moyen_boules, score_moyen_etoiles