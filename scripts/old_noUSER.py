import os
import re

def supprimer_mentions_user(txt_file_path):
    # 1. Gestion du nom du fichier de sortie
    base_name, ext = os.path.splitext(txt_file_path)
    output_base = f"{base_name}_noUSER"
    output_file_path = f"{output_base}{ext}"
    
    counter = 1
    while os.path.exists(output_file_path):
        output_file_path = f"{output_base}_{counter}{ext}"
        counter += 1

    print(f"Génération du fichier sans mentions USER_ : {output_file_path}")

    # 2. Nettoyage et écriture
    with open(txt_file_path, mode='r', encoding='utf-8') as f_in, \
         open(output_file_path, mode='w', encoding='utf-8') as f_out:
        
        for line in f_in:
            # Suppression de tous les "mots" commençant par USER_
            # \S+ signifie "tous les caractères qui suivent jusqu'au prochain espace"
            line = re.sub(r'USER_\S+', '', line)
            
            # Lissage des espaces potentiellement laissés vides par la suppression
            line = re.sub(r' +', ' ', line)
            
            # Nettoyage de l'espace potentiel en début de ligne (sans toucher aux balises étoilées)
            if line.startswith(" ") and not line.startswith(" ****"):
                line = line[1:]
                
            f_out.write(line)

    print("Suppression des mentions terminée avec succès !")

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
chemin_corpus = config.RAW_DATA_DIR / "descriptions" / "xDescStats_EMJIfr.txt"

# 3. Exécution de la fonction
# On utilise str() par sécurité au cas où certaines anciennes fonctions Python
# auraient encore besoin d'une chaîne de caractères classique
supprimer_mentions_user(str(chemin_corpus))