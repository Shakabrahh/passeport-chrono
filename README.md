Passport Chrono
===============

Ce script Python utilise l'API de rendezvouspasseport.ants.gouv.fr pour chercher des créneaux de rendez-vous disponibles
pour les passeports et les cartes d'identité. Une notification sonore est déclenchée dès qu'un créneau est trouvé.

Installation
------------

1. Clonez le dépôt GitHub en utilisant la commande `git clone https://github.com/Shakabrahh/passeport-chrono.git` ou
   téléchargez le code source sous forme de fichier ZIP.
2. Assurez-vous que Python 3.x est installé sur votre système.
3. Dans le dossier du projet, ouvrez un terminal et installez les dépendances en exécutant la
   commande `pip install -r requirements.txt`.

Configuration
-------------

Le fichier de configuration `config.ini` contient les paramètres de recherche de créneaux de rendez-vous. Voici une
explication de chaque paramètre :

* `api_url` : URL de l'API pour récupérer les créneaux disponibles (ne pas modifier)
* `latitude` : Latitude de la ville à partir de laquelle chercher les créneaux disponibles
* `longitude` : Longitude de la ville à partir de laquelle chercher les créneaux disponibles
* `radius_km` : Rayon maximal (en km) autour de la position de départ pour chercher les créneaux disponibles (valeurs
  possibles : 20, 40 ou 60)
* `address` : Adresse de la ville à partir de laquelle chercher les créneaux disponibles (nom de la rue + code postal)
* `reason` : Motif de rendez-vous (valeurs possibles : CNI pour carte nationale d'identité, PASSPORT pour passeport,
  CNI-PASSPORT pour les deux)
* `documents_number` : Nombre de personnes pour le rendez-vous
* `end_date` : Date limite de recherche des créneaux disponibles
* `sound_file_path` : Chemin du fichier audio à jouer lorsqu'un créneau est trouvé
* `sleep_time_sec` : Temps d'attente (en secondes) entre chaque recherche de créneaux ; ne pas mettre une valeur trop
  basse, risque de ban IP
* `log_file_path` : Chemin du fichier de log

Utilisation
-----------

Pour utiliser ce script, exécutez simplement la commande `python3 main.py` dans votre terminal.

Le script effectuera une recherche de créneaux toutes les `sleep_time_sec` secondes. Lorsqu'un créneau est trouvé, il
jouera le fichier audio spécifié dans `sound_file_path`.

Si aucun créneau n'est trouvé, le script continuera de chercher des créneaux disponibles toutes les `sleep_time_sec`
secondes.

Licence
-------

Ce script est distribué sous licence MIT. Voir le fichier LICENSE pour plus d'informations.
