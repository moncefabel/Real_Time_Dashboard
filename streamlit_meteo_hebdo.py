import streamlit as st
import pandas as pd
from pymongo import MongoClient
import matplotlib.pyplot as plt
import seaborn as sns

def lire_donnees_from_db():
    # MongoDB Connection
    client = MongoClient('mongodb://localhost:27017/')
    db = client['meteo']
    collection = db['resumes']

    # Fetch data from MongoDB
    donnees = []
    for document in collection.find():
        donnees.append({
            'date': pd.to_datetime(document['date'], format='%Y%m%d'),
            'temperature': document['temp_moy'],
            'humidite': document['humidite_moy'],
            'vent': document['vent_moy']
        })
    return donnees

# Fetching data from MongoDB
donnees = lire_donnees_from_db()
df = pd.DataFrame(donnees)
df.sort_values('date', inplace=True)
df = df[df['date'] > (pd.to_datetime("today") - pd.Timedelta(weeks=1))]

# Début de l'application Streamlit
st.title('Analyse des données météorologiques récentes')

# Affichage des données
st.write("Données des deux derniers jours :", df)

# Choix du graphique à afficher
option = st.selectbox(
    'Choisissez le type de graphique à afficher',
    ('Histogrammes des paramètres', 'Courbes moyennes quotidiennes', 'Boxplot des paramètres', 'Heatmap des moyennes journalières')
)

# Génération des graphiques en fonction du choix
if option == 'Histogrammes des paramètres':
    fig, axs = plt.subplots(3, figsize=(10, 15))
    for ax, param in zip(axs, ['temperature', 'humidite', 'vent']):
        sns.histplot(df[param], bins=10, kde=True, ax=ax)
        ax.set_title(f'Histogramme de {param}')
    st.pyplot(fig)
elif option == 'Courbes moyennes quotidiennes':
    df_daily_avg = df.set_index('date').resample('D').mean()
    fig, ax = plt.subplots(figsize=(10, 6))
    for param in ['temperature', 'humidite', 'vent']:
        ax.plot(df_daily_avg.index, df_daily_avg[param], marker='o', linestyle='-', label=param)
    ax.set_title('Moyennes quotidiennes des paramètres')
    ax.set_xlabel('Date')
    ax.set_ylabel('Valeur')
    plt.xticks(rotation=45)
    plt.legend()
    st.pyplot(fig)
elif option == 'Boxplot des paramètres':
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(data=df[['temperature', 'humidite', 'vent']], ax=ax)
    st.pyplot(fig)
elif option == 'Heatmap des moyennes journalières':
    df_heatmap = df.set_index('date').resample('D').mean().reset_index()
    df_heatmap['jour'] = df_heatmap['date'].dt.strftime('%Y-%m-%d')
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(df_heatmap.drop(columns='date').set_index('jour'), annot=True, cmap='coolwarm', fmt=".1f", ax=ax)
    st.pyplot(fig)
