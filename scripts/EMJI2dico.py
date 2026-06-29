import os
import re

def generer_dictionnaire_emojis_minuscules(liste_fichiers_txt, fichier_sortie):
    # 1. Gestion du nom du fichier de sortie (pour ne pas écraser les existants)
    base_name, ext = os.path.splitext(fichier_sortie)
    output_file_path = fichier_sortie
    
    counter = 1
    while os.path.exists(output_file_path):
        output_file_path = f"{base_name}_{counter}{ext}"
        counter += 1

    emojis_uniques = set()
    
    # Regex pour capturer toutes les balises commençant par EMJI_ (insensible à la casse avec re.IGNORECASE)
    regex_emji = re.compile(r'\b(EMJI_\w+)\b', re.IGNORECASE)
    
    print("Analyse des fichiers en cours...")
    
    for fichier in liste_fichiers_txt:
        if os.path.exists(fichier):
            print(f"  - Lecture de : {os.path.basename(fichier)}")
            with open(fichier, mode='r', encoding='utf-8') as f:
                texte = f.read()
                emojis_uniques.update(regex_emji.findall(texte))
        else:
            print(f"  /!\\ Fichier introuvable : {fichier}")

    print(f"\nCréation du dictionnaire ({len(emojis_uniques)} emojis uniques trouvés)...")
    
    # 2. Écriture du fichier avec le nom unique généré
    with open(output_file_path, mode='w', encoding='utf-8') as f_out:
        for emji in sorted(emojis_uniques):
            # On force la mise en minuscules de la balise pour IRaMuTeQ
            emji_minuscule = emji.lower()
            
            # Format attendu : Forme \t Lemme \t Type_grammatical
            f_out.write(f"{emji_minuscule}\t{emji_minuscule}\tnom\n")
            
    print(f"Dictionnaire en minuscules généré avec succès : {output_file_path}")

# ==========================================
# ESPACE POUR RENSEIGNER L'ADRESSE DES FICHIERS
# ==========================================
import sys
from pathlib import Path

# 1. Ajout du dossier racine pour importer config.py
chemin_racine = str(Path(__file__).resolve().parent.parent)
if chemin_racine not in sys.path:
    sys.path.append(chemin_racine)

import config

# 2. Construction dynamique de la liste des fichiers en entrée
# On utilise str() sur chaque élément pour s'assurer que la fonction 
# lise bien une chaîne de caractères (chemin texte).
fichiers_a_analyser = [
    str(config.IRAMUTEQ_DATA_DIR / "rts_onlyEMJI_1.txt"),
    str(config.IRAMUTEQ_DATA_DIR / "rtsDesc_onlyEMJI_1.txt")
    # Ajoutez d'autres fichiers ici au besoin
]

# 3. Construction dynamique du chemin de sortie de base pour le dictionnaire
chemin_dictionnaire_base = str(config.DICO_DIR / "lexique_emji.txt")

# 4. Exécution de la fonction
generer_dictionnaire_emojis_minuscules(fichiers_a_analyser, fichier_sortie=chemin_dictionnaire_base)