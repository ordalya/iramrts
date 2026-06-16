import os
import re

def extraire_exclusivement_emojis(txt_file_path):
    # 1. Gestion du nom du fichier de sortie
    base_name, ext = os.path.splitext(txt_file_path)
    output_base = f"{base_name}_onlyEMJI"
    output_file_path = f"{output_base}{ext}"
    
    counter = 1
    while os.path.exists(output_file_path):
        output_file_path = f"{output_base}_{counter}{ext}"
        counter += 1

    print(f"Génération du corpus 'uniquement emojis' : {output_file_path}")

    # Regex pour capturer exclusivement les balises EMJI_
    # \b délimite le mot, [a-zA-Z0-9_-]+ capture les caractères de la balise
    regex_emji = re.compile(r'\b(EMJI_[a-zA-Z0-9_-]+)\b', re.IGNORECASE)

    # 2. Lecture, extraction et écriture
    with open(txt_file_path, mode='r', encoding='utf-8') as f_in, \
         open(output_file_path, mode='w', encoding='utf-8') as f_out:
        
        for line in f_in:
            # Préservation stricte de la syntaxe IRaMuTeQ pour les variables et locuteurs
            if line.startswith("****") or line.startswith("-*"):
                f_out.write(line)
            else:
                # Extraction sous forme de liste de toutes les balises EMJI_ de la ligne
                emojis_trouves = regex_emji.findall(line)
                
                if emojis_trouves:
                    # On rassemble les emojis trouvés, séparés par un espace simple
                    nouvelle_ligne = " ".join(emojis_trouves)
                else:
                    # Sécurité : on insère une balise neutre si le commentaire n'avait pas d'emoji
                    # pour éviter de créer une Unité de Contexte (UC) vide.
                    nouvelle_ligne = "VIDE_aucun_emji"
                    
                f_out.write(f"{nouvelle_ligne}\n")

    print("Extraction exclusive des emojis terminée avec succès !")

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
chemin_corpus = config.RAW_DATA_DIR / "comments" / "rts_langID_EMJIfr_oneUSER_noDash_noURL.txt"
#chemin_corpus = config.RAW_DATA_DIR / "comments" / "rts_langID_EMJIfr_oneUSER_noDash_noURL_lang_fr.txt"
#chemin_corpus = config.IRAMUTEQ_DATA_DIR / "rtsDesc.txt"

# 3. Exécution de la fonction
# On utilise str() par sécurité au cas où certaines anciennes fonctions Python
# auraient encore besoin d'une chaîne de caractères classique
extraire_exclusivement_emojis(str(chemin_corpus))