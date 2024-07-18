import csv,os
import json
from authlib.integrations.requests_client import OAuth2Session
import requests

CLIENT_ID = '83789b983aa74bcfa88786014c735e33'
CLIENT_SECRET = 'd6995ef8cc1b45a49cf9e6a27e8d2ad6'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
USERNAME = os.getenv('SPOTIFY_USERNAME')
PASSWORD = os.getenv('SPOTIFY_PASSWORD')
PLAYLIST_ID = '7BbFLWRCVgcEfykB7BzInZ'
client = OAuth2Session(CLIENT_ID, CLIENT_SECRET,USERNAME,PASSWORD)
token = client.fetch_token(TOKEN_URL)

def fetch_playlist_data():
    access_token = token['access_token']
    RESOURCE_URL = f'https://api.spotify.com/v1/playlists/{PLAYLIST_ID}'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    
    response = requests.get(RESOURCE_URL, headers=headers)

    if response.status_code == 200:
        playlist_data = json.loads(response.text)
        user_name = playlist_data['owner']['display_name']
        track_names = []
        for item in playlist_data['tracks']['items']:
            track_names.append(item['track']['name'])

        csv_file = 'playlist_tracks.csv'
        with open(csv_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Owner', 'Track Name'])
            for track_name in track_names:
                writer.writerow([user_name, track_name])
        print(f"Data written to {csv_file} successfully.")

    elif response.status_code == 401:
        refresh_token = token.get('refresh_token')
        if refresh_token:
            new_token = client.refresh_token(TOKEN_URL, refresh_token=refresh_token)
            token.update(new_token)
            fetch_playlist_data()
        else:
            print("Failed to refresh token. No refresh token found.")
    else:
        print(f"Failed to retrieve playlists: {response.status_code}")
        print(response.text)

fetch_playlist_data()
