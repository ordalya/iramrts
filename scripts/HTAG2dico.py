import os
import re

def generer_dictionnaire_hashtags_minuscules(liste_fichiers_txt, fichier_sortie="dico_htag_iramuteq.txt"):
    hashtags_uniques = set()
    
    # Regex pour capturer toutes les balises commençant par HTAG_ (insensible à la casse avec re.IGNORECASE)
    regex_htag = re.compile(r'\b(HTAG_[a-zA-Z0-9_-]+)\b', re.IGNORECASE)
    
    print("Analyse des fichiers en cours...")
    
    for fichier in liste_fichiers_txt:
        if os.path.exists(fichier):
            print(f"  - Lecture de : {os.path.basename(fichier)}")
            with open(fichier, mode='r', encoding='utf-8') as f:
                texte = f.read()
                hashtags_uniques.update(regex_htag.findall(texte))
        else:
            print(f"  /!\\ Fichier introuvable : {fichier}")

    print(f"\nCréation du dictionnaire ({len(hashtags_uniques)} hashtags uniques trouvés)...")
    
    with open(fichier_sortie, mode='w', encoding='utf-8') as f_out:
        for htag in sorted(hashtags_uniques):
            # AJOUT : On force la mise en minuscules de la balise pour IRaMuTeQ
            htag_minuscule = htag.lower()
            
            # Format attendu : Forme \t Lemme \t Type_grammatical
            f_out.write(f"{htag_minuscule}\t{htag_minuscule}\tnom\n")
            
    print(f"Dictionnaire en minuscules généré avec succès : {fichier_sortie}")

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

# 2. Construction dynamique de la liste des fichiers
# On utilise str() sur chaque élément pour s'assurer que la fonction 
# lise bien une chaîne de caractères (chemin texte).
fichiers_a_analyser = [
    str(config.IRAMUTEQ_DATA_DIR / "full" / "rtsV3_EMJIfr_noUSER_noDash_noURL_langID_noVIDE.txt"),
    str(config.IRAMUTEQ_DATA_DIR / "full" / "xDescStats_EMJIfr_noUSER_noDash_noURL_langID_noVIDE.txt")
    # Ajoutez d'autres fichiers ici au besoin, toujours avec config... / "nom.txt"
]

# 3. Exécution de la fonction
generer_dictionnaire_hashtags_minuscules(fichiers_a_analyser)