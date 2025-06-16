import re
import requests
import base64
import os

def get_spotify_token():
    auth_str = f"{os.getenv('SPOTIFY_CLIENT_ID')}:{os.getenv('SPOTIFY_CLIENT_SECRET')}"
    b64_auth = base64.b64encode(auth_str.encode()).decode()
    headers = {
        "Authorization": f"Basic {b64_auth}"
    }
    data = {
        "grant_type": "client_credentials"
    }
    response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)
    if response.ok:
        return response.json()["access_token"]
    return None

def get_track_info(track_id):
    token = get_spotify_token()
    if not token:
        return None

    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(f"https://api.spotify.com/v1/tracks/{track_id}", headers=headers)
    if not response.ok:
        return None

    data = response.json()
    return {
        "title": data["name"],
        "artist": data["artists"][0]["name"]
    }

def is_correct_guess(guess, title, artist):
    guess = guess.lower()
    return (
        title.lower() in guess or
        artist.lower() in guess
    )
