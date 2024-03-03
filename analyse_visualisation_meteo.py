import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pymongo import MongoClient

# MongoDB Connection
client = MongoClient('mongodb://localhost:27017/')
db = client['meteo']
collection = db['resumes']

# Fetch data from MongoDB
donnees = []
for document in collection.find():
    donnees.append({
        'date': document['date'],
        'temperature': document['temp_moy'],
        'humidite': document['humidite_moy'],
        'vent': document['vent_moy']
    })

# Conversion de la liste en DataFrame pandas
df = pd.DataFrame(donnees)

# Convert 'date' from string to datetime format
df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')

# Trier le DataFrame par date
df.sort_values('date', inplace=True)

# Assurez-vous que le DataFrame contient les données de la dernière semaine uniquement
df = df[df['date'] > (pd.to_datetime("today") - pd.Timedelta(weeks=1))]

# Visualisations
# Histogrammes pour chaque paramètre
plt.figure(figsize=(14, 8))
for i, param in enumerate(['temperature', 'humidite', 'vent'], 1):
    plt.subplot(2, 2, i)
    sns.histplot(df[param], bins=10, kde=True)
    plt.title(f'Histogramme des {param}')
    plt.xlabel(f'{param}')
    plt.ylabel('Fréquence')
plt.tight_layout()
plt.show()

# Courbes moyennes quotidiennes pour chaque paramètre
df_daily_avg = df.set_index('date').resample('D').mean()
plt.figure(figsize=(14, 8))
for param in ['temperature', 'humidite', 'vent']:
    plt.plot(df_daily_avg.index, df_daily_avg[param], marker='o', linestyle='-', label=param)
plt.title('Moyennes quotidiennes des paramètres')
plt.xlabel('Date')
plt.ylabel('Valeur')
plt.xticks(rotation=45)
plt.legend()
plt.show()

# Boxplot des paramètres
plt.figure(figsize=(10, 6))
sns.boxplot(data=df[['temperature', 'humidite', 'vent']])
plt.title('Distribution des paramètres météorologiques')
plt.show()

# Heatmap des paramètres par jour
df_heatmap = df.set_index('date').resample('D').mean().reset_index()
df_heatmap['jour'] = df_heatmap['date'].dt.strftime('%Y-%m-%d')
plt.figure(figsize=(10, 6))
sns.heatmap(df_heatmap.drop(columns='date').set_index('jour'), annot=True, cmap='coolwarm', fmt=".1f")
plt.title('Moyennes journalières des paramètres météorologiques')
plt.xticks(rotation=45)
plt.show()
