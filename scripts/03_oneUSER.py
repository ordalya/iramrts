import os
import re

def anonymiser_mentions_user(txt_file_path):
    # 1. Gestion du nom du fichier de sortie
    base_name, ext = os.path.splitext(txt_file_path)
    output_base = f"{base_name}_oneUSER"
    output_file_path = f"{output_base}{ext}"
    
    counter = 1
    while os.path.exists(output_file_path):
        output_file_path = f"{output_base}_{counter}{ext}"
        counter += 1

    print(f"Génération du fichier avec mentions anonymisées : {output_file_path}")

    # 2. Remplacement et écriture
    with open(txt_file_path, mode='r', encoding='utf-8') as f_in, \
         open(output_file_path, mode='w', encoding='utf-8') as f_out:
        
        for line in f_in:
            # Remplacement de tous les "mots" commençant par USER_ par "USER_utilisateurice"
            # \S+ capture tous les caractères de l'ancien pseudo jusqu'au prochain espace
            line = re.sub(r'USER_\S+', 'USER_utilisateurice', line)
            
            # Lissage des espaces (sécurité maintenue)
            line = re.sub(r' +', ' ', line)
            
            # Nettoyage de l'espace potentiel en début de ligne (sans toucher aux balises étoilées)
            if line.startswith(" ") and not line.startswith(" ****"):
                line = line[1:]
                
            f_out.write(line)

    print("Anonymisation des mentions USER_ terminée avec succès !")

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
chemin_corpus = config.RAW_DATA_DIR / "rts_x_langID_EMJIfr.txt"

# 3. Exécution de la fonction
anonymiser_mentions_user(str(chemin_corpus))