import os
from flask import Flask, request, jsonify
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

load_dotenv()

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID")
WEB_HOST_URL = os.getenv("WEB_HOST_URL")

client = WebClient(token=SLACK_BOT_TOKEN)

app = Flask(__name__)

@app.route("/")
def home():
    return "Mystery Song Bot is running!"

@app.route("/post_song", methods=["POST"])
def post_song():
    data = request.json
    track_id = data.get("track_id")

    if not track_id:
        return jsonify({"error": "track_id missing"}), 400

    mystery_link = f"{WEB_HOST_URL}/mystery/{track_id}"

    try:
        client.chat_postMessage(
            channel=SLACK_CHANNEL_ID,
            text=f"🎧 Mystery Song! ▶️ {mystery_link}"
        )
        return jsonify({"ok": True}), 200
    except SlackApiError as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
