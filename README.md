Projet de Génération de Calendrier de Cours
Description

Ce projet permet de générer un fichier de calendrier (ICS) pour des cours en utilisant des données provenant de fichiers JSON et Python. Les cours sont répartis en fonction des dates disponibles et un fichier ICS est généré pour être importé dans un calendrier électronique.
Prérequis

    Python 3.x
    Module icalendar

Installation

    Cloner le dépôt ou télécharger les fichiers nécessaires :

    sh

git clone <url_du_depot>
cd <nom_du_repertoire>

Installer les dépendances :

sh

    pip install icalendar

Structure des Fichiers

    dbSimu.json : Contient les informations des cours.
    dispo.py : Contient les dates disponibles pour chaque classe.
    generer_le_calendrier.py : Script principal pour générer le fichier ICS.

Contenu de dbSimu.json

json

{
  "cours": [
    {
      "id": 69,
      "forma": "B",
      "sem": "S3",
      "titre": "stat",
      "typec": "CMPrim",
      "ut": "1.83",
      "nb": "6",
      "prof": "ISM",
      "grs": ["E2b"],
      "apres": "59",
      "dateDeb": "2024-08-24T22:00:00.000Z",
      "dateFin": "2025-01-31T23:00:00.000Z",
      "crenos": [0],
      "salles": []
    },
    ...
  ]
}

Contenu de dispo.py

python

dispo = {
  'E2b': [
    datetime.date(2023, 9, 4),
    datetime.date(2023, 9, 5),
    ...
  ],
  ...
}

Utilisation

    Vérifier et mettre à jour les fichiers de données :
        Assurez-vous que dbSimu.json contient les informations des cours.
        Assurez-vous que dispo.py contient les dates disponibles pour chaque classe.

    Exécuter le script pour générer le calendrier :

    sh

    python generer_le_calendrier.py

    Importer le fichier ICS généré dans votre application de calendrier préférée :
        Le fichier cours_repartis.ics sera généré dans le répertoire courant.

Fonctionnalités

    Répartition des cours : Les cours sont répartis en fonction des dates disponibles pour chaque classe.
    Génération d'événements de calendrier : Chaque cours est transformé en événement avec le titre en gras et le nom du professeur.
    Exportation en format ICS : Le fichier ICS peut être importé dans des applications de calendrier comme Google Calendar, Outlook, etc.

Exemples
Exemple de sortie ICS

Un exemple d'entrée dans le fichier ICS généré :

ruby

BEGIN:VEVENT
SUMMARY:<b>stat</b> - ISM
DTSTART;VALUE=DATE:20230904
DTEND;VALUE=DATE:20230905
DESCRIPTION:Cours: stat\nProfesseur: ISM
LOCATION:Salle: Non spécifiée
END:VEVENT

Avertissements

Si une classe n'a pas de dates disponibles dans dispo.py, un avertissement sera affiché dans la console.