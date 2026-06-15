import os

def combler_textes_vides(txt_file_path):
    # 1. Gestion du nom du fichier de sortie
    base_name, ext = os.path.splitext(txt_file_path)
    output_base = f"{base_name}_noVIDE"
    output_file_path = f"{output_base}{ext}"
    
    counter = 1
    while os.path.exists(output_file_path):
        output_file_path = f"{output_base}_{counter}{ext}"
        counter += 1

    print(f"Génération du corpus avec textes comblés : {output_file_path}")

    # 2. Lecture, analyse et écriture
    with open(txt_file_path, mode='r', encoding='utf-8') as f_in, \
         open(output_file_path, mode='w', encoding='utf-8') as f_out:
        
        # On lit toutes les lignes en mémoire (très rapide et peu coûteux en RAM)
        lines = f_in.readlines()
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # Si on détecte une balise de locuteur / thématique
            if line.startswith("-*"):
                f_out.write(line)
                
                # On inspecte la ligne qui suit directement
                if i + 1 < len(lines):
                    next_line = lines[i+1]
                    
                    # Cas A : La ligne de texte est complètement vide (juste un saut de ligne ou des espaces)
                    if next_line.strip() == "":
                        f_out.write("VIDE_aucun_texte\n")
                        i += 1  # On saute la ligne vide d'origine pour ne pas créer un double saut
                        
                    # Cas B : Il n'y a pas de ligne de texte, on passe directement aux variables ou au locuteur suivant
                    elif next_line.startswith("****") or next_line.startswith("-*"):
                        f_out.write("VIDE_aucun_texte\n")
                        
                # Cas C : On est à la toute dernière ligne du fichier et le texte manque
                else:
                    f_out.write("VIDE_aucun_texte\n")
                    
            else:
                # Écriture normale pour les autres lignes (texte existant ou variables ****)
                f_out.write(line)
                
            i += 1

    print("Remplissage des textes vides terminé avec succès !")

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
#chemin_corpus = config.RAW_DATA_DIR / "descriptions" / "xDescStats.txt"
chemin_corpus = config.RAW_DATA_DIR / "full" / "xDescStats_EMJIfr_noUSER_noDash_noURL_langID.txt"

# 3. Exécution de la fonction
# On utilise str() par sécurité au cas où certaines anciennes fonctions Python
# auraient encore besoin d'une chaîne de caractères classique
combler_textes_vides(str(chemin_corpus))