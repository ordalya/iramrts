import csv
import os

def csv_to_iramuteq_comments(csv_file_path):
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
            # Récupération des variables de post (fixes pour toute la ligne)
            var1 = row.get('var1', '').strip()                    # var1 = *rts
            var2 = row.get('var2', '').strip()                    # var2 = *postID
            var3 = row.get('var3', '').strip().replace(' ', '_')  # var3 = *postLikes
            var4 = row.get('var4', '').strip().replace(' ', '_')  # var4 = *postComments
            var5 = row.get('var5', '').strip().replace(' ', '_')  # var5 = *postReposts
            var6 = row.get('var6', '').strip().replace(' ', '_')  # var6 = *postDate
            
            # Scission des colonnes à valeurs multiples
            # Double line break (\n\n) pour username, text et var8 = *commentLikes
            usernames = row.get('username', '').split('\n\n')
            texts = row.get('text', '').split('\n\n')
            var8_list = row.get('var8', '').split('\n\n')
            
            # Simple line break (\n) pour la spécificité de var7 = *commentDate
            var7_list = row.get('var7', '').split('\n')
            
            # Parcours de chaque commentaire
            for i in range(len(usernames)):
                user = usernames[i].strip()
                
                # Récupération sécurisée du texte
                try:
                    txt = texts[i].strip()
                except IndexError:
                    txt = ""
                
                if not txt:
                    txt = "GIF_inconnu"
                    
                txt_propre = txt.replace('\n', ' ')
                
                # Récupération sécurisée de var7 et var8 (avec valeur de secours si manquant)
                v7 = var7_list[i].strip().replace(' ', '_') if i < len(var7_list) else "inconnu"
                v8 = var8_list[i].strip().replace(' ', '_') if i < len(var8_list) else "inconnu"
                
                # Écriture dans le format Iramuteq (Une UCI par commentaire)
                txt_file.write(f"**** *{var1} *{var2} *postLikes_{var3} *postComments_{var4} *postReposts_{var5} *postDate_{var6} *commentDate_{v7} *commentLikes_{v8}\n")
                txt_file.write(f"{txt_propre}\n")

    print(f"Conversion terminée avec succès ! Fichier disponible ici : {output_file_path}")

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

# 2. Construction du chemin dynamique vers le fichier CSV
chemin_du_fichier_csv = config.RAW_DATA_DIR / "rts_a.csv"
#chemin_du_fichier_csv = config.RAW_DATA_DIR / "rts_i.csv"

# 3. Exécution de la fonction
# On utilise str() par sécurité au cas où certaines anciennes fonctions Python
# auraient encore besoin d'une chaîne de caractères classique
csv_to_iramuteq_comments(str(chemin_du_fichier_csv))