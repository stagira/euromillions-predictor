# evaluation.py

def calculer_score(prediction_boules: list, reel_boules: list, prediction_etoiles: list, reel_etoiles: list) -> tuple[int, int]:
    """
    Calcule le nombre de boules et d'étoiles correctes.

    Returns:
        tuple[int, int]: Un tuple (score_boules, score_etoiles).
    """
    bons_numeros = set(prediction_boules) & set(reel_boules)
    bonnes_etoiles = set(prediction_etoiles) & set(reel_etoiles)
    return len(bons_numeros), len(bonnes_etoiles)