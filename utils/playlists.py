from utils.oauth import get_access_token
import requests
import os
from dotenv import load_dotenv

load_dotenv()

token = get_access_token("https://accounts.spotify.com/api/token", os.getenv('SPOTIFY_CLIENT_ID'), os.getenv('SPOTIFY_CLIENT_SECRET'))
headers = {"Authorization": f"Bearer {token}"}

def retreive_playlists(user_id):
    playlists_response = requests.get(
        f'https://api.spotify.com/v1/users/{user_id}/playlists',
        headers=headers
    )

    playlists = playlists_response.json()

    return playlists

def retreive_playlist(playlist_uri):
    playlist_response = requests.get(
        f'https://api.spotify.com/v1/playlists/{playlist_uri}/tracks',
        headers=headers
    )

    playlist = playlist_response.json()

    return playlist

def find_playlist(user_id, playlist_name):
    playlists_response = requests.get(
        f'https://api.spotify.com/v1/users/{user_id}/playlists',
        headers=headers
    )

    playlists = playlists_response.json()

    for playlist in playlists["items"]:
        if playlist["name"] == playlist_name:
            return playlist["id"]

def retrieve_audio_features(song_uri):
    af_response = requests.get(
        f'https://api.spotify.com/v1/audio-features/{song_uri}',
        headers=headers
    )

    af = af_response.json()
    
    return af

def retrieve_payload_audio_features(payload):
    af_response = requests.get(
        f'https://api.spotify.com/v1/audio-features/?ids={payload}',
        headers=headers
    )

    af = af_response.json()
    
    return af

def create_playlist(user_id, payload, bpm, pub):
    playlist_response = requests.post(
        f'https://api.spotify.com/v1/users/{user_id}/playlists',
        data = {"name":f'{int(bpm)} Playlist', "public": pub, "description": f'A custom tailored playlist based on your monthly playlists of tracks above {int(bpm)} BPM.'},
        headers=headers
    )

    playlist = playlist_response.json()

    return playlist

def update_playlist(playlist_uri, payload):
    playlist_response = requests.put(
        f'https://api.spotify.com/v1/playlists/{playlist_uri}/tracks',
        data = {"uris": payload},
        headers=headers
    )

    playlist = playlist_response.json()

    return playlist