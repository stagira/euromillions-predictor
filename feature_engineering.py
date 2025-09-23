# feature_engineering.py
import pandas as pd
import data_manager
from collections import Counter

def calculer_stats_tirage(tirage: data_manager.Tirage) -> dict:
    """Calcule des statistiques descriptives de base pour un seul tirage.

    Args:
        tirage (data_manager.Tirage): L'objet Tirage à analyser.

    Returns:
        dict: Un dictionnaire contenant la somme, la moyenne, le nombre de
              numéros pairs et le nombre de numéros impairs.
    """
    numeros = tirage.numeros
    return {
        'somme_numeros': sum(numeros),
        'moyenne_numeros': sum(numeros) / len(numeros) if numeros else 0,
        'nb_pairs': len([n for n in numeros if n % 2 == 0]),
        'nb_impairs': len([n for n in numeros if n % 2 != 0])
    }

def calculer_ecarts(historique_pertinent: list[data_manager.Tirage]) -> dict:
    """Calcule l'écart pour chaque numéro (depuis combien de tirages il n'est pas sorti).

    L'écart est le nombre de tirages écoulés depuis la dernière apparition
    d'un numéro. Un écart de 0 signifie que le numéro est sorti lors du
    dernier tirage de l'historique fourni.

    Args:
        historique_pertinent (list[data_manager.Tirage]): La liste des tirages
            passés sur laquelle calculer les écarts, du plus récent au plus ancien.

    Returns:
        dict: Un dictionnaire où les clés sont 'ecart_N' et les valeurs sont
              l'écart calculé pour le numéro N.
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
    """Calcule la fréquence de sortie de chaque numéro sur une période récente.

    Args:
        historique_pertinent (list[data_manager.Tirage]): La liste des tirages
            passés, du plus récent au plus ancien.
        periode (int, optional): Le nombre de tirages récents à considérer
            pour le calcul. Defaults to 50.

    Returns:
        dict: Un dictionnaire où les clés sont 'freq_chaude_N' et les valeurs
              sont le nombre d'apparitions du numéro N dans la période.
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
    """Génère un DataFrame de features enrichies pour un historique de tirages.

    Pour chaque tirage dans l'historique, cette fonction calcule un ensemble de
    caractéristiques (features) basées exclusivement sur les tirages qui l'ont
    précédé. Cela évite toute fuite de données du futur dans le passé.

    Args:
        historique (list[data_manager.Tirage]): L'historique complet des
            tirages, du plus récent au plus ancien.

    Returns:
        pd.DataFrame: Un DataFrame où chaque ligne correspond à un tirage de
                      l'historique et chaque colonne à une feature calculée.
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