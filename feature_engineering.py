# feature_engineering.py
import pandas as pd
import data_manager
from collections import Counter

def calculer_stats_tirage(tirage: data_manager.Tirage) -> dict:
    """Calcule des statistiques de base pour un seul tirage."""
    numeros = tirage.numeros
    return {
        'somme_numeros': sum(numeros),
        'moyenne_numeros': sum(numeros) / len(numeros),
        'nb_pairs': len([n for n in numeros if n % 2 == 0]),
        'nb_impairs': len([n for n in numeros if n % 2 != 0])
    }

def calculer_ecarts(historique_pertinent: list[data_manager.Tirage]) -> dict:
    """
    Calcule l'écart pour chaque numéro (depuis combien de tirages il n'est pas sorti).
    L'historique pertinent est la liste des tirages PASSÉS.
    """
    ecarts = {}
    # On initialise l'écart de tous les numéros à la taille de l'historique (au cas où ils ne soient jamais sortis)
    for num in range(1, 51):
        ecarts[f'ecart_{num}'] = len(historique_pertinent)

    # On parcourt l'historique du plus récent au plus ancien
    for i, tirage in enumerate(historique_pertinent):
        for num in tirage.numeros:
            # Si on n'a pas encore trouvé cet écart, on le note
            if f'ecart_{num}' not in ecarts or ecarts[f'ecart_{num}'] == len(historique_pertinent):
                 ecarts[f'ecart_{num}'] = i
    return ecarts

def calculer_frequence_chaude(historique_pertinent: list[data_manager.Tirage], periode: int = 50) -> dict:
    """
    Calcule la fréquence de sortie de chaque numéro sur une période donnée (les 50 derniers tirages par ex.).
    """
    tous_les_numeros = []
    # On ne prend que la période qui nous intéresse
    for tirage in historique_pertinent[:periode]:
        tous_les_numeros.extend(tirage.numeros)

    frequence = Counter(tous_les_numeros)
    
    frequences_chaudes = {}
    for num in range(1, 51):
        frequences_chaudes[f'freq_chaude_{num}'] = frequence.get(num, 0)
        
    return frequences_chaudes

def enrichir_donnees(historique: list[data_manager.Tirage]) -> pd.DataFrame:
    """
    Fonction principale qui génère toutes les nouvelles features pour l'ensemble de l'historique.
    Pour chaque tirage, les features sont calculées en se basant UNIQUEMENT sur les tirages précédents.
    """
    features_enrichies = []
    
    # On parcourt l'historique du plus récent au plus ancien
    for i in range(len(historique)):
        
        # Le tirage pour lequel on veut calculer les features
        tirage_actuel = historique[i]
        
        # L'historique pertinent pour ce tirage est tout ce qui est arrivé AVANT
        historique_passe = historique[i+1:]
        
        if not historique_passe:
            # Pour le tout premier tirage de l'histoire, on n'a pas de passé, on met des valeurs par défaut
            features_pour_un_tirage = {f'ecart_{n}': 0 for n in range(1, 51)}
            features_pour_un_tirage.update({f'freq_chaude_{n}': 0 for n in range(1, 51)})
            features_pour_un_tirage.update({'somme_numeros': 0, 'moyenne_numeros': 0, 'nb_pairs': 0, 'nb_impairs': 0})

        else:
            # On calcule les features en se basant sur le passé
            stats = calculer_stats_tirage(historique_passe[0]) # Stats du tirage N-1
            ecarts = calculer_ecarts(historique_passe)
            freq_chaude = calculer_frequence_chaude(historique_passe)
            
            # On fusionne tout
            features_pour_un_tirage = {**stats, **ecarts, **freq_chaude}
        
        features_enrichies.append(features_pour_un_tirage)
        
    return pd.DataFrame(features_enrichies)