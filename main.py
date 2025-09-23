# main.py
import data_manager
import backtest

print("--- Démarrage du Prédicteur Euromillions ---")
historique = data_manager.charger_donnees()
print(f"✅ {len(historique)} tirages ont été chargés.")

# On ne lance le backtest que si on a assez de données
if historique and len(historique) > 250:
    # Lance la simulation sur les 50 derniers tirages
    backtest.lancer_backtest(historique, 50)
else:
    print("Pas assez de données pour lancer une simulation de backtest.")

print("\n--- Application terminée ---")