# main.py

import data_manager

# On crée un "objet" en utilisant le plan data_manager.Tirage
premier_tirage = data_manager.Tirage(
    date="20/10/2023", 
    numeros=[5, 12, 22, 35, 48], 
    etoiles=[3, 9]
)

# On accède aux données de façon super lisible !
print(f"Date du tirage : {premier_tirage.date}")
print(f"Numéros : {premier_tirage.numeros}")
print(f"Étoiles : {premier_tirage.etoiles}")