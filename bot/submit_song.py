import requests

BOT_URL = "http://localhost:3000/post_song"  # Change to Render URL when deployed

def extract_track_id(url_or_id):
    if "spotify.com/track/" in url_or_id:
        return url_or_id.strip().split("/")[-1].split("?")[0]
    return url_or_id.strip()

def main():
    user_input = input("🎧 Enter Spotify Track URL or ID: ")
    track_id = extract_track_id(user_input)

    response = requests.post(BOT_URL, json={"track_id": track_id})
    if response.ok:
        print("✅ Mystery song posted!")
    else:
        print("❌ Error:", response.json())

if __name__ == "__main__":
    main()
