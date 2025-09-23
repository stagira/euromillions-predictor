# Dans backtest.py

import data_manager
import prediction_models
import evaluation
from tqdm import tqdm

def lancer_backtest(historique_complet: list[data_manager.Tirage], nombre_de_tests: int):
    """
    Lance une simulation de backtesting réaliste sur les N derniers tirages.
    """
    print(f"\n--- 🚀 Lancement du Backtesting (CORRIGÉ) sur les {nombre_de_tests} derniers tirages ---")
    scores_boules = []
    scores_etoiles = []

    # L'historique est classé du plus récent (index 0) au plus ancien
    for i in tqdm(range(nombre_de_tests), desc="Simulation temporelle correcte"):
        
        # 1. La VÉRITÉ : Le tirage que l'on veut deviner (le "futur")
        tirage_a_deviner = historique_complet[i]
        vrais_numeros = tirage_a_deviner.numeros
        vraies_etoiles = tirage_a_deviner.etoiles

        # 2. Les DONNÉES pour la prédiction : Le tirage juste avant
        tirage_precedent_pour_predire = historique_complet[i + 1]
        
        # 3. Les DONNÉES pour l'entraînement : TOUT ce qui est plus ancien
        donnees_entrainement = historique_complet[i + 2:]

        # On vérifie qu'on a assez de passé pour s'entraîner
        if len(donnees_entrainement) < 200:
            print("Arrêt anticipé : pas assez de données historiques pour continuer le test.")
            break

        # On crée, entraîne et prédit avec les bonnes données temporelles
        modele_ml = prediction_models.ComiteDeModelesML()
        modele_ml.entrainer(donnees_entrainement)
        pred_boules, pred_etoiles = modele_ml.predire(tirage_precedent_pour_predire)
        
        # On évalue le score
        score_b, score_e = evaluation.calculer_score(pred_boules, vrais_numeros, pred_etoiles, vraies_etoiles)
        scores_boules.append(score_b)
        scores_etoiles.append(score_e)

    if scores_boules:
        print(f"\n--- ✅ Résultats du Backtesting ({len(scores_boules)} tirages testés) ---")
        print(f"   - Score moyen (Boules) : {sum(scores_boules) / len(scores_boules):.2f} / 5")
        print(f"   - Score moyen (Étoiles) : {sum(scores_etoiles) / len(scores_etoiles):.2f} / 2")
        gros_scores = len([s for s in scores_boules if s >= 3])
        print(f"   - Occurrences de 3 bonnes boules ou plus : {gros_scores} fois.")
    else:
        print("❌ Le backtest n'a pas pu être effectué.")