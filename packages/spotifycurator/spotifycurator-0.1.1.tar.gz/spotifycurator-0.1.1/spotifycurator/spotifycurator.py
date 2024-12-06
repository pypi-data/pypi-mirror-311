import os
import requests
import base64
import json
import webbrowser
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv
from http.server import HTTPServer, BaseHTTPRequestHandler
import time

# Load environment variables
load_dotenv(dotenv_path=r'C:\Users\NTMat\OneDrive\Documents\CodeProjects\creds.env')

SPOTIFY_CLIENT_ID = 'dbe7036ccbf74248af5e5306b552f227'
SPOTIFY_CLIENT_SECRET = '2f6b829cf54a4ce19c616622ef9de6c7'
SPOTIFY_REDIRECT_URI = 'http://localhost:8888/callback/'

# Globals for access and refresh tokens
access_token = None
refresh_token = None

# Step 1: Define a lightweight HTTP server to capture the redirect URL
class SpotifyAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        query_components = parse_qs(urlparse(self.path).query)
        if "code" in query_components:
            self.server.auth_code = query_components["code"][0]
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Authorization successful! You can close this window.")
            print("Authorization code captured:", self.server.auth_code)
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Authorization failed. Please try again.")
            print("Authorization failed. Query components:", query_components)

def get_auth_code():
    server_address = ('localhost', 8888)
    httpd = HTTPServer(server_address, SpotifyAuthHandler)
    httpd.auth_code = None  # Initialize attribute

    print("Waiting for user authorization...")
    scope = "playlist-read-private playlist-modify-public playlist-modify-private user-library-read"
    auth_url = (
        f"https://accounts.spotify.com/authorize?client_id={SPOTIFY_CLIENT_ID}"
        f"&response_type=code&redirect_uri={SPOTIFY_REDIRECT_URI}&scope={scope}"
    )
    webbrowser.open(auth_url)
    httpd.handle_request()

    if not httpd.auth_code:
        raise Exception("Authorization code not captured. Ensure you completed the login process.")

    return httpd.auth_code

# Step 2: Exchange authorization code for tokens
def get_tokens():
    global access_token, refresh_token

    auth_code = get_auth_code()
    print(f"Authorization Code: {auth_code}")

    auth_str = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()

    token_url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": f"Basic {b64_auth_str}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": SPOTIFY_REDIRECT_URI
    }

    response = requests.post(token_url, headers=headers, data=data)
    if response.status_code != 200:
        print("Failed to get tokens:", response.text)
        response.raise_for_status()

    tokens = response.json()
    access_token = tokens.get('access_token')
    refresh_token = tokens.get('refresh_token')

    if not access_token or not refresh_token:
        raise Exception("Failed to retrieve tokens. Check your client credentials.")
    
    print("Tokens obtained successfully.")
    print(f"Access Token: {access_token}")
    print(f"Refresh Token: {refresh_token}")

# Step 3: Refresh access token
def refresh_access_token():
    global access_token

    auth_str = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()

    token_url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": f"Basic {b64_auth_str}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }

    response = requests.post(token_url, headers=headers, data=data)
    if response.status_code != 200:
        print("Failed to refresh token:", response.text)
        response.raise_for_status()

    tokens = response.json()
    access_token = tokens.get('access_token')

    if not access_token:
        raise Exception("Failed to refresh access token.")

    print("Access token refreshed.")

# Helper function to handle rate limits
def handle_rate_limit(response):
    if response.status_code == 429:
        retry_after = int(response.headers.get("Retry-After", 1))
        print(f"Rate limit hit. Retrying after {retry_after} seconds.")
        time.sleep(retry_after)
        return True
    return False

def make_request_with_retry(url, method="GET", headers=None, data=None, max_retries=5):
    retries = 0
    while retries < max_retries:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, headers=headers, data=data)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers, data=data)
        elif method == "PUT":
            response = requests.put(url, headers=headers, data=data)

        if response.status_code in [200, 201]:
            return response
        elif handle_rate_limit(response):
            retries += 1
        else:
            print("Error Response:", response.text)
            response.raise_for_status()

    raise Exception(f"Failed after {max_retries} retries.")

# Function to fetch user's "Liked Songs"
def get_liked_songs():
    url = "https://api.spotify.com/v1/me/tracks"
    headers = {"Authorization": f"Bearer {access_token}"}
    all_tracks = []

    while url:
        response = make_request_with_retry(url, method="GET", headers=headers)
        data = response.json()
        all_tracks.extend(data['items'])
        url = data['next']

    return [track['track']['uri'] for track in all_tracks]

# Function to find or create a playlist
def find_or_create_playlist(playlist_name="Public Liked Songs"):
    url = "https://api.spotify.com/v1/me/playlists"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = make_request_with_retry(url, method="GET", headers=headers)

    playlists = response.json()['items']
    for playlist in playlists:
        if playlist['name'] == playlist_name:
            return playlist['id']

    # Create the playlist with a name and description
    data = json.dumps({
        "name": playlist_name,
        "public": True,
        "description": "A public playlist containing all your liked songs."
    })
    response = make_request_with_retry(url, method="POST", headers=headers, data=data)
    return response.json()['id']

# Function to add tracks to the playlist
def add_tracks_to_playlist(playlist_id, track_uris):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = {"Authorization": f"Bearer {access_token}"}
    batch_size = 100  # Spotify allows up to 100 tracks per request

    # Add tracks in batches of 100
    for i in range(0, len(track_uris), batch_size):
        batch = track_uris[i:i+batch_size]
        data = json.dumps({"uris": batch})
        response = make_request_with_retry(url, method="POST", headers=headers, data=data)
        if response.status_code not in [200, 201]:
            raise Exception(f"Failed to add tracks: {response.status_code} - {response.text}")
    print(f"Added {len(track_uris)} tracks to playlist '{playlist_id}'.")

# Main workflow
def main():
    global access_token, refresh_token

    if not access_token or not refresh_token:
        print("No access or refresh token found. Initiating authorization flow.")
        get_tokens()

    choice = input("1. Make public liked songs playlist\n2. Exit\nEnter your choice: ")

    if choice == "1":
        playlist_id = find_or_create_playlist()
        liked_songs = get_liked_songs()
        print(f"Fetched {len(liked_songs)} liked songs.")

        add_tracks_to_playlist(playlist_id, liked_songs)
        print(f"Public liked songs playlist created and updated with liked songs.")
    else:
        print("Exiting.")

if __name__ == "__main__":
    main()
