import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns 

client_id = 'SEU_CLIENT_ID'
client_secret = 'SEU_CLIENT_SECRET'

auth = SpotifyClientCredentials98(client_id=client_id, client_secret=client_secret)
sp = spotipy.spotipy(client_credentials_manager=auth)

playlist_link = "link"
playlist_uri = playlist_link.split("/")[-1].split("?")[0]

results= sp.playlist_tracks(playlist_uri)


tracks = []
for item in results['item']:
    track = item['track']
    features = sp.audio_features(track['id'])[0]
    tracks.append({
        'name': track['name'],
        'artist': track['artists'][0]['name'],
        'popylarity': track['popularity'],
        'duration_ms': track['duration_ms'],
        'danceability': features['danceability'],
        'energy': features['energy'],
        'valence': features['valence'],
        'tempo': features['tempo']
    })

    df = pd.DataFrame(tracks)

    df['duration_min'] = df['duration_ms'] / 60000

    df.head()

    plt.figure(figsize=(12,6))
    sns.barplot(data=df.sortvalues('popularity', ascending=false). head(10), x='name', y='popularity')
    plt.xticks(rotacion=45)
    plt.title('top 10 musicas mais populares')
    plt.show()

    sns.scatterplot(data=df, x='energy', y='danceability', hue='popularity', palette='viridis')
    plt.title('energia vc danceabilidade')
    plt.show()

    df.describe()



