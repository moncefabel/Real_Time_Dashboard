import os
import json
import glob
from datetime import datetime, timedelta
from pymongo import MongoClient

# Configuration
DIR = "/home/moncef/Downloads/moncef_bouhabel_linux_project"
client = MongoClient('mongodb://localhost:27017/')
db = client['meteo']
collection = db['resumes']

def resumer_journee():
    # Calculer la date d'hier pour filtrer les fichiers de la journée précédente
    hier = (datetime.now() - timedelta(1)).strftime('%Y%m%d')
    pattern = f"{DIR}/{hier}*_data_weather.json"
    fichiers = glob.glob(pattern)
    resume = {
        'date': hier,
        'temp_moy': 0,
        'humidite_moy': 0,
        'vent_moy': 0,
        'nb_fichiers': len(fichiers)
    }
    
    for fichier in fichiers:
        with open(fichier, 'r') as f:
            data = json.load(f)
            resume['temp_moy'] += data['main']['temp']
            resume['humidite_moy'] += data['main']['humidity']
            resume['vent_moy'] += data['wind']['speed']
    
    if resume['nb_fichiers'] > 0:
        resume['temp_moy'] /= resume['nb_fichiers']
        resume['humidite_moy'] /= resume['nb_fichiers']
        resume['vent_moy'] /= resume['nb_fichiers']
    
    # Stockage du résumé dans MongoDB
    collection.insert_one(resume)
    
    # Suppression des fichiers JSON de la journée précédente
    for fichier in fichiers:
        os.remove(fichier)





resumer_journee()
