# Dans backtest.py

import data_manager
import prediction_models
import evaluation
from tqdm import tqdm

def lancer_backtest(
    modele_a_tester: prediction_models.ComiteDeModelesML,
    historique_complet: list[data_manager.Tirage],
    nombre_de_tests: int
) -> tuple[float, float]:
    """Lance une simulation de backtesting pour évaluer un modèle.

    Cette fonction simule des prédictions sur une période passée. Pour chaque
    pas de temps, elle entraîne le modèle sur un historique qui s'arrête avant
    le tirage à prédire, fait une prédiction, et la compare au résultat réel.

    Args:
        modele_a_tester (prediction_models.ComiteDeModelesML): L'instance du
            modèle à évaluer.
        historique_complet (list[data_manager.Tirage]): L'historique complet
            des tirages, du plus récent au plus ancien.
        nombre_de_tests (int): Le nombre de tirages récents à utiliser pour
            la simulation.

    Returns:
        tuple[float, float]: Un tuple contenant le score moyen pour les boules
        et le score moyen pour les étoiles sur l'ensemble de la simulation.
    """
    print(f"\n--- 🚀 Lancement du Backtesting sur les {nombre_de_tests} derniers tirages ---")
    scores_boules = []
    scores_etoiles = []

    for i in tqdm(range(nombre_de_tests), desc="Simulation temporelle", leave=False):
        tirage_a_deviner = historique_complet[i]
        tirage_precedent_pour_predire = historique_complet[i + 1]
        donnees_entrainement = historique_complet[i + 2:]

        if len(donnees_entrainement) < 200:
            break

        # On utilise le modèle fourni en argument, on ne le crée plus ici
        modele_a_tester.entrainer(donnees_entrainement) 
        pred_boules, pred_etoiles = modele_a_tester.predire(tirage_precedent_pour_predire, donnees_entrainement)
        
        score_b, score_e = evaluation.calculer_score(pred_boules, tirage_a_deviner.numeros, pred_etoiles, tirage_a_deviner.etoiles)
        scores_boules.append(score_b)
        scores_etoiles.append(score_e)

    score_moyen_boules = sum(scores_boules) / len(scores_boules) if scores_boules else 0
    score_moyen_etoiles = sum(scores_etoiles) / len(scores_etoiles) if scores_etoiles else 0
    
    # On retourne le résultat au lieu de juste l'imprimer
    return score_moyen_boules, score_moyen_etoiles