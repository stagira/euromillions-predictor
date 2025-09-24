# config_manager.py
import configparser
from pathlib import Path

# Le chemin vers le fichier de configuration, relatif à ce fichier.
CONFIG_FILE = Path(__file__).parent / 'config.ini'

def get_config() -> configparser.ConfigParser:
    """Charge la configuration depuis le fichier config.ini.

    Returns:
        configparser.ConfigParser: Un objet ConfigParser contenant les
        données de configuration. Si le fichier n'existe pas, l'objet
        sera vide mais valide.
    """
    config = configparser.ConfigParser()
    # read() ne lève pas d'erreur si le fichier n'existe pas, il retourne juste un objet vide.
    config.read(CONFIG_FILE)
    return config

# On charge la configuration une seule fois au démarrage du module.
config = get_config()

def get_log_level() -> str:
    """Récupère le niveau de log depuis la configuration.

    Lit la clé 'level' de la section [Logging]. Si la clé ou la section
    est absente, retourne 'INFO' par défaut.

    Returns:
        str: Le niveau de log (ex: 'INFO', 'DEBUG').
    """
    return config.get('Logging', 'level', fallback='INFO').upper()

def get_prediction_log_file() -> str:
    """Récupère le chemin du fichier de log pour les prédictions.

    Lit la clé 'log_file' de la section [Predictions]. Si la clé ou la
    section est absente, retourne 'predictions.log' par défaut.

    Returns:
        str: Le nom du fichier de log pour les prédictions.
    """
    return config.get('Predictions', 'log_file', fallback='predictions.log')

def get_report_file() -> str:
    """Récupère le chemin du fichier de rapport pour les exécutions.

    Lit la clé 'report_file' de la section [Report]. Si la clé ou la
    section est absente, retourne 'run_report.log' par défaut.

    Returns:
        str: Le nom du fichier de log pour les rapports d'exécution.
    """
    return config.get('Report', 'report_file', fallback='run_report.log')
