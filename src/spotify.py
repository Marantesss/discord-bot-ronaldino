import os
import json
from json.decoder import JSONDecodeError
# spotify API written in python
import spotipy
import spotipy.util as util
import spotipy.oauth2 as oauth

# getting top secret information
with open("settings.json") as settingsFile:
	settings = json.load(settingsFile)

# getting credentials
username = settings["spotify_user_id"]
scope = 'playlist-read-private,' \
		' playlist-read-collaborative,' \
		' user-read-playback-state,' \
		' user-modify-playback-state,' \
		' user-read-currently-playing'
client_id = settings["spotify_client_id"]
client_secret = settings["spotify_client_secret"]
redirect_uri = settings["spotify_redirect_uri"]

# creating spotify credentials manager
spotify_auth = oauth.SpotifyOAuth(
			client_id=client_id,
			client_secret=client_secret,
			redirect_uri=redirect_uri,
			scope=scope,
			cache_path=f".cache-{username}")

# 'logging in' to spotify
def spotify_log_in(username):
    try:
        # if cache file exists, then we have a chached token
        if os.path.isfile(f".cache-{username}"):
            cached_token = spotify_auth.get_cached_token()
            token = cached_token["access_token"]
        # if not then we need to create the cache file
        else:
            token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
        print(token)
        return spotipy.Spotify(auth=token)
    except (AttributeError, JSONDecodeError):
        os.remove(f".cache-{username}")
        token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
        return spotipy.Spotify(auth=token)

# logging in the the bot is booted
spotify = spotify_log_in(username)

def refresh_token():
    global spotify
    cached_token = spotify_auth.get_cached_token()
    print(cached_token)
    refreshed_token = cached_token['refresh_token']
    new_token = spotify_auth.refresh_access_token(refreshed_token)
    print(new_token)
    # also we need to specifically pass `auth=new_token['access_token']`
    spotify = spotipy.Spotify(auth=new_token['access_token'])

def spotify_command(message, handler, args):
    try:
        # getting the full search string and search results
        searchResults = spotify.search(" ".join(args),1,0,"artist")
        # getting info from JSON file
        artistInfo = searchResults["artists"]["items"][0]
        msg = ":musical_note: **Artist** :microphone:\n"
        msg += "**Name:** {}\n**Genres:** {}\n**Followers:** {}\n**Image:** {}".format(artistInfo["name"], artistInfo["genres"], artistInfo["followers"]["total"], artistInfo["images"][0]["url"])
        return msg
    # This exception will be caught when .search() fails
    # That means that the token has expired and we need a new one
    except spotipy.SpotifyException as se:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(se).__name__, se.args)
        print(message)
        refresh_token()
        msg = ":no_entry: **ERROR** :no_entry: : Spotify token has expired\n"
        msg += "Spotify token was refreshed, enjoy :notes:"
        return msg
    except Exception as e:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(e).__name__, e.args)
        print(message)