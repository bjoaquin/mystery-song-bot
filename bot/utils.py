import re
import requests

def get_track_info(track_id):
    try:
        url = f"https://open.spotify.com/oembed?url=https://open.spotify.com/track/{track_id}"
        response = requests.get(url)
        if not response.ok:
            return None
        data = response.json()
        title_artist = data["title"]
        match = re.match(r"(.+?) by (.+)", title_artist)
        if not match:
            return None
        return {
            "title": match.group(1).strip(),
            "artist": match.group(2).strip()
        }
    except:
        return None

def is_correct_guess(guess, title, artist):
    guess = guess.lower()
    return (
        title.lower() in guess or
        artist.lower() in guess
    )
