from utils.oauth import get_access_token
from utils.playlists import *
import requests
import re
import time
 
pattern = r'^(1[0-2]|0?[1-9])\.\d{2}$'

def curate_playlist_by_ascending_bpm(user_id, bpm=125.0, playlist=None):
    playlists_response = retreive_playlists(user_id)
    playlists = []
    valid_tracks = []
    for item in playlists_response["items"]:
        if re.match(pattern, item["name"]):
            playlists.append(item["id"])
    
    all_songs = []
    for playlist in playlists:
        playlist_response = retreive_playlist(playlist)
        songs_response = playlist_response["items"]
        # songs = [song["track"]["id"] for song in songs_response] #
        songs = [song.get("track", {}).get("id") for song in songs_response if song.get("track") is not None]
        all_songs.extend(songs)

    song_partition = [all_songs[i:i + 100] for i in range(0, len(all_songs), 100)]

    for song in song_partition:
        flattened_string = ",".join(str(sg) for sg in song)
        af_response = retrieve_payload_audio_features(flattened_string)
        for af in af_response["audio_features"]:
            if af["tempo"] > float(bpm):
                valid_tracks.append(f'spotify:track:{af["id"]}')
    
    payload_partition = [valid_tracks[i:i + 100] for i in range(0, len(valid_tracks), 100)]
    responses = []

    if playlist == None:
        return valid_tracks
    else:
        playlist_uri = find_playlist(user_id, playlist)
        for payload in payload_partition:
            responses.append(update_playlist(playlist_uri, payload))
        return responses
        





