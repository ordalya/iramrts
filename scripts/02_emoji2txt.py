import os
import re
import emoji

def convert_emojis_iramuteq_fr(txt_file_path):
    # 1. Gestion du nom du fichier de sortie
    base_name, ext = os.path.splitext(txt_file_path)
    output_base = f"{base_name}_EMJIfr"
    output_file_path = f"{output_base}{ext}"
    
    counter = 1
    while os.path.exists(output_file_path):
        output_file_path = f"{output_base}_{counter}{ext}"
        counter += 1

    print(f"Le fichier de sortie sera généré sous le nom : {output_file_path}")

    # 2. Lecture, conversion et écriture
    with open(txt_file_path, mode='r', encoding='utf-8') as f_in, \
         open(output_file_path, mode='w', encoding='utf-8') as f_out:
        
        for line in f_in:
            # On cherche tous les emojis uniques présents dans la ligne
            unique_emojis = emoji.distinct_emoji_list(line)
            
            for emj in unique_emojis:
                # Traduction de l'emoji en français (format par défaut : :nom_de_lemoji:)
                demojized = emoji.demojize(emj, language='fr')
                
                # Remplacement du premier ":" par EMJI_ et suppression du second
                balise_finale = demojized.replace(":", "EMJI_", 1).replace(":", "")
                
                # Remplacement des espaces par des "_" pour la syntaxe IRaMuTeQ (sécurité supplémentaire)
                balise_finale = balise_finale.replace(" ", "_")
                
                # On encadre la balise d'espaces (avant ET après) pour l'isoler
                balise_isolee = f" {balise_finale} "
                
                # Remplacement de l'emoji par la balise isolée dans la ligne
                line = line.replace(emj, balise_isolee)
            
            # Lissage des espaces : transforme les suites de 1 à N espaces en un seul
            line = re.sub(r' +', ' ', line)
            
            # Nettoyage des bordures pour respecter la syntaxe Iramuteq
            # Retire l'espace potentiel juste avant le saut de ligne
            line = line.replace(" \n", "\n") 

            # Retire l'espace potentiel au tout début de la ligne (si elle commençait par un emoji)
            # sans toucher aux étoiles des variables Iramuteq
            if line.startswith(" ") and not line.startswith(" ****"):
                line = line[1:]
                
            f_out.write(line)

    print("Conversion des emojis en français terminée avec succès !")

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
chemin_du_fichier_txt = config.RAW_DATA_DIR / "descriptions" / "xDescStats_langID.txt"

# 3. Exécution de la fonction
# On utilise str() par sécurité au cas où certaines anciennes fonctions Python
# auraient encore besoin d'une chaîne de caractères classique
convert_emojis_iramuteq_fr(str(chemin_du_fichier_txt))