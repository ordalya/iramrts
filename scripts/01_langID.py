import os
import re
import langid

def tagger_langue_corpus(txt_file_path):
    # 1. Gestion du nom du fichier de sortie
    base_name, ext = os.path.splitext(txt_file_path)
    output_base = f"{base_name}_langID"
    output_file_path = f"{output_base}{ext}"
    
    counter = 1
    while os.path.exists(output_file_path):
        output_file_path = f"{output_base}_{counter}{ext}"
        counter += 1

    print(f"Génération du corpus avec tags de langue : {output_file_path}")

    # 2. Variables de stockage temporaire
    current_stars_line = ""
    current_user_line = ""
    
    # 3. Lecture, détection et écriture
    with open(txt_file_path, mode='r', encoding='utf-8') as f_in, \
         open(output_file_path, mode='w', encoding='utf-8') as f_out:
        
        for line in f_in:
            # Si c'est la ligne des variables (commence par ****)
            if line.startswith("****"):
                current_stars_line = line.strip()
                
            # Si c'est la ligne du nom d'utilisateur (commence par -*)
            elif line.startswith("-*"):
                current_user_line = line
                
            # Si c'est la ligne du texte du commentaire
            else:
                texte_commentaire = line.strip()
                
                # S'il y a du texte à analyser (et pas juste des balises ou du vide)
                if texte_commentaire and texte_commentaire != "GIF_inconnu":
                    
                    # On nettoie temporairement les balises EMJI_ & HTAG_ pour ne pas fausser la détection
                    texte_pour_detection = re.sub(r'EMJI_[a-zA-Z0-9_]+', '', texte_commentaire)
                    texte_pour_detection = re.sub(r'HTAG_[a-zA-Z0-9_]+', '', texte_commentaire)
                    
                    # Détection de la langue avec langid
                    # langid.classify renvoie un tuple (code_langue, score_de_confiance)
                    # ex: ('fr', 0.99) ou ('en', 0.85)
                    try:
                        lang, score = langid.classify(texte_pour_detection)
                    except:
                        lang = "inconnu"
                        
                    # On regroupe toutes les langues non-françaises sous "other" pour simplifier
                    # (Vous pouvez modifier ceci pour garder le code exact si vous préférez)
                    lang_tag = "fr" if lang == "fr" else "other"
                    
                else:
                    # Si c'est juste un GIF ou du vide, on taggue "inconnu"
                    lang_tag = "inconnu"
                
                # On ajoute la nouvelle variable *lang_ à la ligne d'étoiles
                nouvelle_ligne_etoiles = f"{current_stars_line} *lang_{lang_tag}\n"
                
                # On écrit le bloc complet dans le nouveau fichier
                f_out.write(nouvelle_ligne_etoiles)
                f_out.write(current_user_line)
                f_out.write(line)

    print("Détection des langues terminée avec succès !")

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
chemin_corpus = config.RAW_DATA_DIR / "rts_x.txt"

# 3. Exécution de la fonction
# On utilise str() par sécurité au cas où certaines anciennes fonctions Pythonsource 
# auraient encore besoin d'une chaîne de caractères classique
tagger_langue_corpus(str(chemin_corpus))