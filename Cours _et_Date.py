import json
import csv
import datetime
from copy import deepcopy
import datetime

# import la fonction shuffle() contenue dans le fichier "prog.py"
from prog import shuffle
from dispo import dispo

# importer le Type de cours ordonné
from prog import typecOrd

# Charger les données du  fichier dbSimu.json
with open('dbSimu.json', 'r') as f:
    data = json.load(f)

#Extraire les cours par classe
cours_par_classe = {}
for cours in data['cours']:
    for classe in cours['grs']:
        if classe not in cours_par_classe:
            cours_par_classe[classe] = []
        cours_par_classe[classe].append(cours)
       
        

# # Extraire les cours par identifiant
# cours_par_id = {}
# for cours in data['cours']:
#     cours_par_id[cours['id']] = cours


# Répartir les cours en utilisant les dates disponibles
cours_repartis = {}
for classe, cours_list in cours_par_classe.items():
    if classe not in dispo:
        print(f"Avertissement : La classe {classe} n'a pas de dates disponibles dans 'dispo'.")
        continue
    dates_disponibles = deepcopy(dispo[classe])    
   
# Séparer les cours de type 'CM' et les autres types
    CM_courses = [cours for cours in cours_list if cours['typec'] == 'CM']
    print(CM_courses)
    other_courses = [cours for cours in cours_list if cours['typec'] != 'CM']

# Filtrer les cours avec un type de cours valide
    other_courses = [cours for cours in other_courses if cours['typec'] in typecOrd]
    

    # Trier les autres cours par type selon l'ordre défini
    other_courses_sorted = sorted(other_courses, key=lambda x: typecOrd.index(x['typec']))

    # Mélanger les dates disponibles avec les CM et autres cours triés
    dates_melangees = shuffle(CM_courses, other_courses_sorted + dates_disponibles)
    cours_repartis[classe] = []
    date_idx = 0
    
    # Répartir les dates pour les cours CM
    for cours in CM_courses:
        nombre_seances = int(float(cours['nb']))
        seances = []
        for _ in range(nombre_seances):
            if date_idx < len(dates_melangees):
                seances.append(dates_melangees[date_idx])
                date_idx += 1
            else:
                break
        cours_repartis[classe].append((cours, seances))

    # Répartir les dates pour les autres types de cours
    for cours in other_courses_sorted:
        nombre_seances = int(float(cours['nb']))
        seances = []
        for _ in range(nombre_seances):
            if date_idx < len(dates_melangees):
                seances.append(dates_melangees[date_idx])
                date_idx += 1
            else:
                break
        cours_repartis[classe].append((cours, seances))

# Générer le fichier CSV
with open('cours_repartis.csv', 'w', newline='') as csvfile:
    fieldnames = ['Classe','Semestre','Cours', 'Type', 'Professeur', 'Séance', 'Date']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for classe, cours_list in cours_repartis.items():
        for cours, seances in cours_list:
            for idx, date in enumerate(seances):
                writer.writerow({
                    'Classe': classe,
                    'Semestre': cours['sem'],
                    'Cours': cours['titre'],
                    'Type': cours['typec'],
                    'Professeur': cours['prof'],
                    'Séance': idx + 1,
                    'Date': date.strftime('%Y-%m-%d')
                })
