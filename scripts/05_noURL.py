import os
import re

def supprimer_urls(txt_file_path):
    # 1. Gestion du nom du fichier de sortie
    base_name, ext = os.path.splitext(txt_file_path)
    output_base = f"{base_name}_noURL"
    output_file_path = f"{output_base}{ext}"
    
    counter = 1
    while os.path.exists(output_file_path):
        output_file_path = f"{output_base}_{counter}{ext}"
        counter += 1

    print(f"Génération du fichier sans URL : {output_file_path}")

    # Regex pour capturer les URL commençant par http:// ou https://
    # "https?" cherche "http" suivi optionnellement d'un "s"
    # "\S+" capture tous les caractères qui suivent jusqu'au prochain espace (ce qui correspond à l'URL complète)
    regex_url = re.compile(r'https?://\S+')

    # 2. Lecture, nettoyage et écriture
    with open(txt_file_path, mode='r', encoding='utf-8') as f_in, \
         open(output_file_path, mode='w', encoding='utf-8') as f_out:
        
        for line in f_in:
            # Remplacement de l'URL par une chaîne vide
            line = regex_url.sub('', line)
            
            # Lissage des espaces (si la suppression de l'URL crée un double espace)
            line = re.sub(r' +', ' ', line)
            
            # Nettoyage de l'espace potentiel en début de ligne
            # (Attention à ne pas toucher aux lignes étoilées d'IRaMuTeQ)
            if line.startswith(" ") and not line.startswith(" ****"):
                line = line[1:]
                
            f_out.write(line)

    print("Suppression des URL terminée avec succès !")

# ==========================================
# ESPACE POUR RENSEIGNER L'ADRESSE DU FICHIER
# ==========================================
import sys
from pathlib import Path

# 1. Ajout du dossier racine pour importer config.py
chemin_racine = str(Path(__file__).resolve().parent.parent)
if chemin_racine not in sys.path:
    sys.path.append(chemin_racine)

import config

# 2. Construction du chemin dynamique vers le fichier TXT
chemin_corpus = config.RAW_DATA_DIR / "descriptions" / "xDescStats_langID_EMJIfr_oneUSER_noDash.txt"

# 3. Exécution de la fonction
# On utilise str() par sécurité au cas où certaines anciennes fonctions Python
# auraient encore besoin d'une chaîne de caractères classique
supprimer_urls(str(chemin_corpus))