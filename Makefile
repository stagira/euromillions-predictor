# ==============================================================================
# Makefile pour le projet Euromillions Predictor
# ==============================================================================
#
# Ce fichier centralise les commandes les plus courantes pour ce projet.
# Assurez-vous d'avoir 'make' installé sur votre système.
# Sur Windows, 'make' est souvent disponible via Git Bash ou Chocolatey.

# Définit l'interpréteur Python à utiliser depuis l'environnement virtuel.
# Cela rend les commandes plus propres et indépendantes du système d'exploitation.
PYTHON = venv/Scripts/python

# .PHONY déclare que ces cibles ne sont pas des fichiers.
# C'est une bonne pratique pour éviter les conflits.
.PHONY: help install docs run predict update clean

# La cible par défaut, qui s'exécute si on tape juste 'make'.
default: help

help:
	@echo "=============================================================================="
	@echo "Bienvenue dans le tableau de bord du projet Euromillions Predictor !"
	@echo "=============================================================================="
	@echo "Commandes disponibles :"
	@echo "  make install   : Crée l'environnement virtuel et installe les dépendances."
	@echo "  make docs      : Génère toute la documentation (Sphinx, diagrammes)."
	@echo "  make run       : Lance l'optimisation complète du modèle (main.py)."
	@echo "  make predict   : Génère une nouvelle prédiction (predire_futur.py)."
	@echo "  make update    : Met à jour le modèle avec les dernières données (update_model.py)."
	@echo "  make clean     : Nettoie les fichiers et dossiers générés."
	@echo "=============================================================================="

# Cible pour l'installation et l'initialisation du projet.
install:
	@echo "-> Création de l'environnement virtuel 'venv' s'il n'existe pas..."
	@if not exist venv (python -m venv venv)
	@echo "-> Installation/Mise à jour des dépendances depuis requirements.txt..."
	@$(PYTHON) -m pip install --upgrade pip
	@$(PYTHON) -m pip install -r requirements.txt

# Cible pour générer toute la documentation.
docs: install
	@echo "-> Génération de la documentation Sphinx..."
	@$(PYTHON) -m sphinx.cmd.build -b html docs docs/_build/html
	@echo "-> Génération du graphe de dépendances avec pydeps..."
	@$(PYTHON) -m pydeps.pydeps --cluster --rankdir LR -o dependency_graph.svg .
	@echo "✅ Documentation générée dans 'docs/_build/html/' et 'dependency_graph.svg'"
	@echo "NOTE : Pour le graphe d'appels (pycallgraph), lancez manuellement :"
	@echo "       make predict-graph"

# Cible pour lancer le script principal d'optimisation.
run: install
	@echo "-> Lancement du 'tournoi' de modèles (main.py)..."
	@$(PYTHON) main.py

# Cible pour lancer une prédiction.
predict: install
	@echo "-> Lancement d'une prédiction (predire_futur.py)..."
	@$(PYTHON) predire_futur.py

# Cible pour générer le graphe d'appels lors d'une prédiction.
predict-graph: install
	@echo "-> Lancement d'une prédiction avec génération du graphe d'appels (pycallgraph)..."
	@$(PYTHON) -m pycallgraph2 graphviz -- predire_futur.py
	@echo "✅ Graphe d'appels généré dans 'pycallgraph.png'"

# Cible pour mettre à jour le modèle avec les dernières données.
update: install
	@echo "-> Mise à jour du modèle avec les dernières données (update_model.py)..."
	@$(PYTHON) update_model.py

# Cible pour nettoyer le projet.
clean:
	@echo "-> Nettoyage des fichiers générés..."
	@if exist docs/_build (rmdir /s /q docs/_build)
	@if exist .pytest_cache (rmdir /s /q .pytest_cache)
	@if exist model_cache (rmdir /s /q model_cache)
	@if exist dependency_graph.svg (del dependency_graph.svg)
	@if exist pycallgraph.png (del pycallgraph.png)
	@echo "Nettoyage des fichiers __pycache__..."
	@for /d /r . %d in (__pycache__) do @if exist "%d" rmdir /s /q "%d"