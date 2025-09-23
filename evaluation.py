# evaluation.py

def calculer_score(prediction_boules: list, reel_boules: list, prediction_etoiles: list, reel_etoiles: list) -> tuple[int, int]:
    """Calcule le nombre de boules et d'étoiles correctement prédites.

    Args:
        prediction_boules (list): La liste des 5 boules prédites.
        reel_boules (list): La liste des 5 boules réelles du tirage.
        prediction_etoiles (list): La liste des 2 étoiles prédites.
        reel_etoiles (list): La liste des 2 étoiles réelles du tirage.

    Returns:
        tuple[int, int]: Un tuple contenant le nombre de boules correctes
        et le nombre d'étoiles correctes.
    """
    bons_numeros = set(prediction_boules) & set(reel_boules)
    bonnes_etoiles = set(prediction_etoiles) & set(reel_etoiles)
    return len(bons_numeros), len(bonnes_etoiles)