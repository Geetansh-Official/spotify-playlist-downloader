import os
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

SPOTIFY_CLIENT_ID = os.environ.get('CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.environ.get('CLIENT_SECRET')

scopes = "user-library-read playlist-modify-private playlist-modify-public"

sp_oauth = SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    scope=scopes,
    redirect_uri="https://example.com",
    show_dialog=True,
    cache_path="token.txt",
)

sp = spotipy.Spotify(auth_manager=sp_oauth)
user_id = sp.current_user()['id']

# Getting all the playlists that the user have
all_playlists = sp.user_playlists(user_id)
i = 0
for playlist in all_playlists['items']:
    print(f"{i+1}.{playlist['name']}: {playlist['id']}")
    i += 1

selected_playlist = int(input(f"Select a playlist download: (1 - {len(all_playlists['items'])}): ")) - 1

playlist_id = all_playlists['items'][selected_playlist]['id']
playlist_name = all_playlists['items'][selected_playlist]['name']


# Starting the Download Process
session = requests.Session()

def get_songs_data(playlist_id):
    URL = f"https://api.spotifydown.com/trackList/playlist/{playlist_id}"

    req = requests.get(URL)

    headers = {
        'authority': 'api.spotifydown.com',
        'method': 'GET',
        'origin': 'https://spotifydown.com',
        'referer': 'https://spotifydown.com/',
        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'sec-fetch-mode': 'cors',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    }
    response = session.get(url=URL, headers=headers)
    print(response.status_code)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None



def V2catch(SONG_ID):
    headers = {
        "authority": "api.spotifydown.com",
        "method": "POST",
        "path": '/download/68GdZAAowWDac3SkdNWOwo',
        "scheme": "https",
        "Accept": "*/*",

        'Sec-Ch-Ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
        "Dnt": '1',
        "Origin": "https://spotifydown.com",
        "Referer": "https://spotifydown.com/",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
    }
    x = session.get(url=f'https://api.spotifydown.com/download/{SONG_ID}', headers=headers)
    if x.status_code == 200:

        try:
            return {
                'link': x.json()['link'],
                'metadata': None
            }
        except:
            return {
                'link': None,
                'metadata': None
            }
    return None

data = get_songs_data(playlist_id)
all_songs_id = [sid['id'] for sid in data['trackList']]
all_songs_title = [sid['title'] for sid in data['trackList']]

# Checking if there are already downloaded songs
downloaded = []

folder_name = f"./songs/{playlist_name}/"
os.makedirs(folder_name, exist_ok=True)
files_in_folder = os.listdir(folder_name)
for file_name in files_in_folder:
    downloaded.append(file_name.split('.mp3')[0])

for i in range(len(all_songs_title)):
    if all_songs_title[i] in downloaded:
        continue
    v2 = V2catch(SONG_ID=all_songs_id[i])
    try:
        r = requests.get(v2['link'])
        r.raise_for_status()  # Raise an exception for HTTP errors

        with open(f"./songs/{playlist_name}/{all_songs_title[i]}.mp3", "wb") as f:
            f.write(r.content)
        print(f"{all_songs_title[i]} downloaded successfully!")
    except requests.exceptions.RequestException as e:
        print("Error downloading the song:", e)


