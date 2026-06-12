# config.py
from pathlib import Path

# 1. Définir la racine du projet
# Path(__file__).resolve() donne le chemin absolu de config.py
# .parent donne le dossier qui le contient (donc la racine du projet)
ROOT_DIR = Path(__file__).resolve().parent

# 2. Définir les dossiers de données
# L'opérateur "/" est magique avec pathlib : il adapte les slashs selon l'OS (Windows ou Linux)
DATA_DIR = ROOT_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
IRAMUTEQ_DATA_DIR = DATA_DIR / "iramuteq"

# Création automatique des dossiers de sortie s'ils n'existent pas encore lors du clonage GitHub
IRAMUTEQ_DATA_DIR.mkdir(parents=True, exist_ok=True)