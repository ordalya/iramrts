import csv
import os
import sys
from pathlib import Path

def csv_to_iramuteq_descriptions(csv_file_path):
    # 1. Gestion du nom du fichier de sortie
    base_name, ext = os.path.splitext(csv_file_path)
    output_file_path = f"{base_name}.txt"
    
    counter = 1
    while os.path.exists(output_file_path):
        output_file_path = f"{base_name}_{counter}.txt"
        counter += 1

    print(f"Le fichier de sortie sera généré sous le nom : {output_file_path}")

    # 2. Lecture du CSV et écriture du TXT
    with open(csv_file_path, mode='r', encoding='utf-8-sig') as csv_file, \
         open(output_file_path, mode='w', encoding='utf-8') as txt_file:
        
        reader = csv.DictReader(csv_file)
        
        for row in reader:
            # Récupération des variables (fixes pour toute la ligne)
            var1 = row.get('var1', '').strip()  # var1 = *rts
            var2 = row.get('var2', '').strip()  # var2 = *postID
            var3 = row.get('var3', '').strip().replace(' ', '_')    # var3 = *postLikes
            var4 = row.get('var4', '').strip().replace(' ', '_')    # var4 = *postComments
            var5 = row.get('var5', '').strip().replace(' ', '_') #   var5 = *postReposts
            var6 = row.get('var6', '').strip().replace(' ', '_') #   var6 = *postDate

            # Plus de .split() ni de boucle for ! 
            # On récupère directement la chaîne de caractères.
            user = row.get('username', '').strip()
            txt = row.get('text', '').strip()
            
            # Sécurité pour les descriptions manquantes
            if not txt:
                txt = "VIDE_aucun_texte"
                
            # Nettoyage des sauts de ligne internes à la description pour IRaMuTeQ
            txt_propre = txt.replace('\n', ' ')
            
            # Écriture dans le format Iramuteq (Une UCI par ligne de CSV)
            txt_file.write(f"**** *{var1} *{var2} *postLikes_{var3} *postComments_{var4} *postReposts_{var5} *postDate_{var6}\n")
            txt_file.write(f"-*{user}\n")
            txt_file.write(f"{txt_propre}\n")

    print(f"Conversion terminée avec succès ! Fichier disponible ici : {output_file_path}")

# ==========================================
# ESPACE POUR RENSEIGNER L'ADRESSE DU FICHIER
# ==========================================

# 1. Ajout du dossier racine pour importer config.py
chemin_racine = str(Path(__file__).resolve().parent.parent)
if chemin_racine not in sys.path:
    sys.path.append(chemin_racine)

import config

# 2. Construction du chemin dynamique vers le fichier CSV
chemin_du_fichier_csv = config.RAW_DATA_DIR / "descriptions" / "aDescStats.csv"
#chemin_du_fichier_csv = config.RAW_DATA_DIR / "descriptions" / "iDescStats.csv"

# 3. Exécution de la fonction
csv_to_iramuteq_descriptions(str(chemin_du_fichier_csv))