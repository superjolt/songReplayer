import os
from flask import Flask, request, render_template, redirect, url_for
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Spotify credentials from .env file
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")

# Required scope: Playback control and status
SCOPE = "user-modify-playback-state user-read-playback-state"

# Initialize Spotipy with token caching in a custom file
auth_manager = SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope=SCOPE,
    cache_path=".cache-spotifyUI"
)
sp = spotipy.Spotify(auth_manager=auth_manager)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        query = request.form.get("query")
        if query:
            # Search for tracks matching the query
            results = sp.search(q=query, type="track", limit=10)
            tracks = results.get("tracks", {}).get("items", [])
            return render_template("results.html", tracks=tracks)
    return render_template("index.html")

@app.route("/play/<track_id>")
def play_track(track_id):
    # For this example, we'll try to play the track from the beginning.
    start_ms = 0
    try:
        sp.start_playback(uris=[f"spotify:track:{track_id}"], position_ms=start_ms)
        return f"Attempting to play track: {track_id}. (Requires Spotify Premium)"
    except Exception as e:
        return f"Error playing track: {e}"

if __name__ == "__main__":
    app.run(debug=True)
