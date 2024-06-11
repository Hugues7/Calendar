import json
import csv
import datetime
from copy import deepcopy
from random import shuffle
from icalendar import Calendar, Event

# Charger les données des fichiers
with open('dbSimu.json', 'r') as f:
    data = json.load(f)

from dispo import dispo

# Extraire les cours par classe
cours_par_classe = {}
for cours in data['cours']:
    for classe in cours['grs']:
        if classe not in cours_par_classe:
            cours_par_classe[classe] = []
        cours_par_classe[classe].append(cours)

# Fonction shuffle personnalisée
def shuffle(C, T):
    if len(C) == 0 or len(T) == 0:
        return []

    b = len(T)
    a = len(C)

    if a > b:
        a, b = b, a
        C, T = T, C

    Cbis = C[:]
    Tbis = T[:]
    ret = []

    q = b // a
    d = b * 1.0 / a - q

    k = 0
    acc = 0
    i = 0

    while k < b:
        acc += d
        ret.append(Tbis[k])
        if (k + 1) % q == 0 and i < len(Cbis):
            ret.append(Cbis[i])
            i += 1
        k += 1

    return ret

# Répartir les cours en utilisant les dates disponibles
cours_repartis = {}
typecOrd = ['CM','CMPrim','CD','CI','TD','TP','PRJ','NT','EXS','EXL','ORAUX','AUTRE']

for classe, cours_list in cours_par_classe.items():
    if classe not in dispo:
        print(f"Avertissement : La classe {classe} n'a pas de dates disponibles dans 'dispo'.")
        continue

    dates_disponibles = deepcopy(dispo[classe])
    
    CM_courses = [cours for cours in cours_list if cours['typec'] == 'CM']
    other_courses = [cours for cours in cours_list if cours['typec'] != 'CM' and cours['typec'] in typecOrd]
    
    other_courses_sorted = sorted(other_courses, key=lambda x: typecOrd.index(x['typec']))
    
    dates_melangees = shuffle(CM_courses, other_courses_sorted + dates_disponibles)
    
    cours_repartis[classe] = []
    date_idx = 0

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

# Générer le fichier ICS
cal = Calendar()

for classe, cours_list in cours_repartis.items():
    for cours, seances in cours_list:
        for idx, date in enumerate(seances):
            event = Event()
            event.add('summary', f"<b>{cours['titre']}</b> - {cours['prof']}")
            event.add('dtstart', date)
            event.add('dtend', date + datetime.timedelta(hours=1))
            event.add('description', f"Cours: {cours['titre']}\nProfesseur: {cours['prof']}")
            event.add('location', f"Salle: {cours['salles'] if 'salles' in cours else 'Non spécifiée'}")
            cal.add_component(event)

with open('cours_repartis.ics', 'wb') as f:
    f.write(cal.to_ical())

print("Le fichier calendrier 'cours_repartis.ics' a été généré avec succès.")
