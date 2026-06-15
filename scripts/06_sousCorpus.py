import os
from contextlib import ExitStack

def diviser_corpus_iramuteq(chemin_corpus, modalites_cibles):
    base_name, ext = os.path.splitext(chemin_corpus)
    
    # 1. Génération automatique des noms de fichiers de sortie
    chemins_sortie = {}
    for mod in modalites_cibles:
        # On retire l'étoile initiale pour créer un nom de fichier lisible et propre
        nom_propre = mod.replace('*', '') 
        chemins_sortie[mod] = f"{base_name}_{nom_propre}{ext}"
        
    print("Début de la division du corpus...")
    
    # 2. Utilisation de ExitStack pour gérer élégamment un nombre dynamique de fichiers
    with ExitStack() as stack:
        # Ouverture du corpus source en lecture
        f_in = stack.enter_context(open(chemin_corpus, 'r', encoding='utf-8'))
        
        # Ouverture dynamique de tous les sous-corpus en écriture
        fichiers_out = {
            mod: stack.enter_context(open(chemin, 'w', encoding='utf-8'))
            for mod, chemin in chemins_sortie.items()
        }
        
        fichiers_cibles_actuels = []
        
        # 3. Parcours efficient du fichier ligne par ligne
        for ligne in f_in:
            # Dès qu'on repère une nouvelle unité de contexte (ligne d'étoiles)
            if ligne.startswith("****"):
                # On réinitialise la liste des fichiers qui doivent recevoir ce bloc de texte
                fichiers_cibles_actuels = []
                
                # On découpe la ligne pour isoler chaque variable de manière stricte
                variables_presentes = ligne.split()
                
                # On vérifie si la ligne contient l'une de nos modalités cibles
                for mod in modalites_cibles:
                    if mod in variables_presentes:
                        fichiers_cibles_actuels.append(fichiers_out[mod])
            
            # On écrit la ligne (qu'elle soit la ligne ****, le -*username ou le texte) 
            # dans tous les sous-corpus correspondants
            for f_out in fichiers_cibles_actuels:
                f_out.write(ligne)

    print("\nDivision terminée avec succès ! Sous-corpus générés dans le même dossier :")
    for chemin in chemins_sortie.values():
        print(f" -> {os.path.basename(chemin)}")

# =================================================================
# ESPACE POUR RENSEIGNER L'ADRESSE DU FICHIER + MODALITÉS À EXTRAIRE
# =================================================================
import sys
from pathlib import Path

# 1. Ajout du dossier racine pour importer config.py
chemin_racine = str(Path(__file__).resolve().parent.parent)
if chemin_racine not in sys.path:
    sys.path.append(chemin_racine)

import config

# 2. Construction du chemin dynamique vers le fichier TXT
chemin_corpus = config.RAW_DATA_DIR / "comments" / "rts_langID_EMJIfr_oneUSER_noDash_noURL.txt"
#chemin_corpus = config.IRAMUTEQ_DATA_DIR / "rtsDesc.txt"

# 3. Listez simplement les modalités exactes que vous souhaitez extraire.
# Le script créera automatiquement un fichier par modalité inscrite dans cette liste.
modalites_a_extraire = [
    "*rts_a",
    "*rts_i"
    #"*lang_fr",
    #"*lang_other",
    #"*lang_inconnu"
]

# 4. Exécution de la fonction
# On utilise str() par sécurité au cas où certaines anciennes fonctions Python
# auraient encore besoin d'une chaîne de caractères classique
diviser_corpus_iramuteq(str(chemin_corpus), modalites_a_extraire)