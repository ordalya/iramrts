import os
import re

def remplacer_tirets_apostrophes_emojis(txt_file_path):
    # 1. Gestion du nom du fichier de sortie
    base_name, ext = os.path.splitext(txt_file_path)
    output_base = f"{base_name}_noDash"
    output_file_path = f"{output_base}{ext}"
    
    counter = 1
    while os.path.exists(output_file_path):
        output_file_path = f"{output_base}_{counter}{ext}"
        counter += 1

    print(f"Génération du fichier corrigé : {output_file_path}")

    # Fonction de remplacement ciblée
    def nettoyer_balise(match):
        # Récupère le mot trouvé par la regex
        mot = match.group(0)
        
        # On remplace les tirets et les apostrophes en modifiant la variable étape par étape
        mot = mot.replace('-', '_')
        mot = mot.replace("'", '_')  # Apostrophe droite
        mot = mot.replace('’', '_')  # Apostrophe typographique
        
        # On fait un seul retour final
        return mot

    # MODIFICATION CRUCIALE : Ajout de \' et ’ dans les crochets pour que la Regex 
    # englobe toute la balise, même si elle contient des apostrophes.
    # CORRECTION : Utilisation de \w pour capturer les lettres accentuées (comme le é de états)
    regex_emji = re.compile(r'\b(EMJI_[\w\-\'’]+)\b', re.IGNORECASE)

    # 2. Lecture, remplacement et écriture
    with open(txt_file_path, mode='r', encoding='utf-8') as f_in, \
         open(output_file_path, mode='w', encoding='utf-8') as f_out:
        
        for line in f_in:
            # re.sub envoie chaque correspondance trouvée à la fonction "nettoyer_balise"
            line_modifiee = regex_emji.sub(nettoyer_balise, line)
            
            f_out.write(line_modifiee)

    print("Remplacement des tirets et apostrophes terminé avec succès !")

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
chemin_corpus = config.RAW_DATA_DIR / "descriptions" / "xDescStats_langID_EMJIfr_oneUSER.txt"

# 3. Exécution de la fonction
# On utilise str() par sécurité au cas où certaines anciennes fonctions Python
# auraient encore besoin d'une chaîne de caractères classique
remplacer_tirets_apostrophes_emojis(str(chemin_corpus))