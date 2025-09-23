# main.py
import argparse
import data_manager
import backtest
import prediction_models

def lancer_prediction():
    """
    Orchestre l'entraînement d'un modèle sur tout l'historique
    et la prédiction du prochain tirage.
    """
    print("--- Lancement du mode Prédiction ---")
    historique = data_manager.charger_donnees()
    if not historique:
        print("❌ Impossible de charger l'historique.")
        return

    # Le dernier tirage connu sert de base à la prédiction
    dernier_tirage = historique[0]
    # Tout l'historique sert à l'entraînement
    donnees_entrainement = historique

    print(f"🤖 Entraînement du modèle sur {len(donnees_entrainement)} tirages historiques...")
    modele = prediction_models.ComiteDeModelesML()
    modele.entrainer(donnees_entrainement)

    print("\n🔮 Prédiction pour le prochain tirage :")
    pred_boules, pred_etoiles = modele.predire(dernier_tirage)
    print(f"   - Boules  : {pred_boules}")
    print(f"   - Étoiles : {pred_etoiles}")

def lancer_le_backtest(nombre_de_tests: int):
    """
    Orchestre le lancement du backtest.
    """
    print("--- Lancement du mode Backtest ---")
    historique = data_manager.charger_donnees()
    if len(historique) < nombre_de_tests + 200:
        print(f"❌ Pas assez de données pour un backtest de {nombre_de_tests} tirages.")
        return
    backtest.lancer_backtest(historique, nombre_de_tests)

def main():
    """
    Fonction principale qui analyse les arguments de la ligne de commande.
    """
    parser = argparse.ArgumentParser(
        description="Prédicteur Euromillions et outil de backtesting.",
        epilog="Exemple d'utilisation : py main.py --predict"
    )
    parser.add_argument('--predict', action='store_true', help="Entraîne un modèle sur tout l'historique et prédit le prochain tirage.")
    parser.add_argument('--backtest', type=int, metavar='N', help="Lance un backtest sur les N derniers tirages.")

    args = parser.parse_args()

    if args.predict:
        lancer_prediction()
    elif args.backtest:
        lancer_le_backtest(args.backtest)
    else:
        # Action par défaut si aucun argument n'est donné
        print("Bienvenue ! Veuillez choisir une action : --predict ou --backtest N")
        parser.print_help()

if __name__ == "__main__":
    # Ce bloc ne s'exécute que si le fichier est lancé directement
    main()