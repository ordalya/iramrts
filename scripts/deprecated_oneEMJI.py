import os
import re

def dedupliquer_emojis(txt_file_path):
    # 1. Gestion du nom du fichier de sortie
    base_name, ext = os.path.splitext(txt_file_path)
    output_base = f"{base_name}_oneEMJI"
    output_file_path = f"{output_base}{ext}"
    
    counter = 1
    while os.path.exists(output_file_path):
        output_file_path = f"{output_base}_{counter}{ext}"
        counter += 1

    print(f"Génération du fichier avec emojis dédupliqués : {output_file_path}")

    # 2. Déduplication et écriture
    with open(txt_file_path, mode='r', encoding='utf-8') as f_in, \
         open(output_file_path, mode='w', encoding='utf-8') as f_out:
        
        for line in f_in:
            # L'expression régulière cherche une balise EMJI_ (capturée dans le groupe 1)
            # suivie d'espaces et de cette même balise répétée une ou plusieurs fois.
            # Elle remplace toute cette suite par une seule occurrence de la balise (r'\1').
            # La boucle 'while' permet de traiter les cas où plusieurs types d'emojis 
            # différents sont répétés à la suite dans la même phrase.
            
            old_line = ""
            while old_line != line:
                old_line = line
                line = re.sub(r'(EMJI_\S+)(?:\s+\1)+', r'\1', line)
                
            f_out.write(line)

    print("Déduplication des emojis terminée avec succès !")

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

# 2. Construction du chemin dynamique vers le fichier CSV
chemin_corpus = config.RAW_DATA_DIR / "descriptions" / "aDescStats.csv"

# 3. Exécution de la fonction
# On utilise str() par sécurité au cas où certaines anciennes fonctions Python
# auraient encore besoin d'une chaîne de caractères classique
dedupliquer_emojis(str(chemin_corpus))