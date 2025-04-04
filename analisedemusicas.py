import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd                                   
import matplotlib.pyplot as plt
import seaborn as sns 

# Credenciais do Spotify
client_id = '375964c128fd4a4095cb8522ae1c2754'         
client_secret = '6084025021dc46518e5e638036aba91b'

# Autenticação com a API
auth = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=auth)

# Link da playlist
playlist_link = "https://open.spotify.com/playlist/37i9dQZF1EJKgZph4Mb2Yw?si=ONzDWZuCRqeAbXcHWzNmUg"
playlist_uri = playlist_link.split("/")[-1].split("?")[0]

# Coleta de músicas com paginação
results = sp.playlist_tracks(playlist_uri)
tracks = results['items']

while results['next']:
    results = sp.next(results)
    tracks.extend(results['items'])

# Processamento das faixas
songs_data = []

for item in tracks:
    track = item['track']
    if track is None or track['id'] is None:
        continue
    
    features = sp.audio_features(track['id'])[0]
    
    if features:
        songs_data.append({
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'popularity': track['popularity'],
            'duration_ms': track['duration_ms'],
            'danceability': features['danceability'],
            'energy': features['energy'],
            'valence': features['valence'],
            'tempo': features['tempo']
        })

# Criação do DataFrame
df = pd.DataFrame(songs_data)
df['duration_min'] = df['duration_ms'] / 60000

# Exibição das primeiras músicas
print(df.head())

# Gráfico: Top 10 músicas mais populares
plt.figure(figsize=(12, 6))
top_10 = df.sort_values('popularity', ascending=False).head(10)
sns.barplot(data=top_10, x='name', y='popularity', palette='coolwarm')
plt.xticks(rotation=45, ha='right')
plt.title('Top 10 músicas mais populares')
plt.xlabel('Música')
plt.ylabel('Popularidade')
plt.tight_layout()
plt.show()

# Gráfico: Energia vs Danceabilidade
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='energy', y='danceability', hue='popularity', palette='viridis', size='popularity', sizes=(40, 200))
plt.title('Energia vs Danceabilidade')
plt.xlabel('Energia')
plt.ylabel('Danceabilidade')
plt.legend(title='Popularidade', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# Estatísticas descritivas
print(df.describe())


