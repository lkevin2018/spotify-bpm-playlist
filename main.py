from typing import Union
from fastapi import FastAPI
from utils.oauth import get_access_token
from utils.playlists import retreive_playlists
from utils.bpm import curate_playlist_by_ascending_bpm

app = FastAPI()

@app.get("/playlists/{user_id}")
async def read_playlists(user_id):
    return retreive_playlists(user_id)

@app.get("/curate")
async def read_playlists(user_id, bpm, playlist):
    return curate_playlist_by_ascending_bpm(user_id, bpm, playlist)