import os
import re
import base64
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
from utils import get_track_info, is_correct_guess

load_dotenv()

app = Flask(__name__)
CORS(app)  # esto habilita CORS para todos los endpoints
client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))
SLACK_CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID")
WEB_HOST_URL = os.getenv("WEB_HOST_URL")

# In-memory mystery song
current_mystery = {}

@app.route("/")
def home():
    return "Mystery Song Bot is running!"

@app.route("/post_song", methods=["POST"])
def post_song():
    data = request.json
    track_id = data.get("track_id")
    if not track_id:
        return jsonify({"error": "track_id missing"}), 400

    info = get_track_info(track_id)
    if not info:
        return jsonify({"error": "invalid track ID"}), 400

    link = f"{WEB_HOST_URL}/mystery/{track_id}"
    try:
        result = client.chat_postMessage(
            channel=SLACK_CHANNEL_ID,
            text=f"🎧 Mystery Song! ▶️ {link}"
        )
        ts = result["ts"]
        current_mystery.clear()
        current_mystery.update({
            "track_id": track_id,
            "title": info["title"],
            "artist": info["artist"],
            "ts": ts
        })
        return jsonify({"ok": True}), 200
    except SlackApiError as e:
        return jsonify({"error": str(e)}), 500

@app.route("/slack/events", methods=["POST"])
def slack_events():
    data = request.json

    # URL verification challenge
    if data.get("type") == "url_verification":
        return jsonify({"challenge": data["challenge"]})

    # Listen for message events
    if "event" in data:
        event = data["event"]
        if event.get("type") == "message" and event.get("thread_ts") == current_mystery.get("ts"):
            user_guess = event.get("text", "")
            if is_correct_guess(user_guess, current_mystery["title"], current_mystery["artist"]):
                try:
                    client.chat_postMessage(
                        channel=SLACK_CHANNEL_ID,
                        thread_ts=current_mystery["ts"],
                        text=f"🎉 <@{event['user']}> guessed it right! It was *{current_mystery['title']}* by *{current_mystery['artist']}*!"
                    )
                except SlackApiError as e:
                    print("Slack error:", e)

    return jsonify({"ok": True}), 200

@app.route("/preview/<track_id>")
def get_preview(track_id):
    # 1. Obtener token desde Spotify
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

    auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    token_response = requests.post(
        "https://accounts.spotify.com/api/token",
        headers={"Authorization": f"Basic {auth_header}"},
        data={"grant_type": "client_credentials"}
    )

    if not token_response.ok:
        return jsonify({"error": "Failed to authenticate with Spotify"}), 500

    token = token_response.json().get("access_token")

    # 2. Buscar track info
    track_response = requests.get(
        f"https://api.spotify.com/v1/tracks/{track_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    if not track_response.ok:
        return jsonify({"error": "Track not found"}), 404

    data = track_response.json()
    return jsonify({"preview_url": data.get("preview_url")})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))  # 5000 is a fallback for local testing
    app.run(host="0.0.0.0", port=port)