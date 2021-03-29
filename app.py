# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import time
import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, url_for, redirect, session, request

app = Flask(__name__)

app.secret_key = 'anr%%!e(tv%+q1siv-e5xkb!k'
app.config['SESSION_COOKIE_NAME'] = 'spotify-login-session'
TOKEN_INFO = "token_info"


@app.route('/')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    print(auth_url)
    return redirect(auth_url)


@app.route('/authorise')
def is_user_authorised():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session['token_info'] = token_info
    return redirect('/getPlaylists')

@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect(url_for('login', _external=False))

@app.route('/getPlaylists')
def get_all_playlists():
    session['token_info'], is_user_authorised = get_token()
    session.modified = True
    if not is_user_authorised:
        return redirect(url_for('login', _external=False))
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    playlist_id = []
    iter = 0
    while True:
        offset = iter * 50
        iter += 1
        current_playlist = sp.current_user_playlists(limit=50, offset=offset)['items']

        for idx, item in enumerate(current_playlist):

            tracks = item['tracks']
            val = tracks['name'] + " - " + tracks['artists'][0]['name']
            playlist_id += [val]

        if len(current_playlist) < 50:
            break

        return playlist_id

def get_track_ids(playlist_id):
    session['token_info'], is_user_authorised = get_token()
    session.modified = True
    if not is_user_authorised:
        return redirect(url_for('login', _external=False))
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    track_id_list = []
    while True:
        playlist = sp.playlist(playlist_id)

        for item in playlist['tracks']['items']:
            track = item['track']
            track_id_list.append(track['id'])
        return track_id_list


def get_track_data(track_id):
    session['token_info'], is_user_authorised = get_token()
    session.modified = True
    if not is_user_authorised:
        return redirect(url_for('login', _external=False))
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    while True:
        metadata = sp.track(track_id)
        track_metadata = {"name": metadata['name'], "album": metadata['album']['name'],
                          "artist": metadata['album']['artist'][0]['name'],
                          "release_date": metadata['album']['release_date'],
                          "duration_min": round((metadata['duration_ms'] * 0.001) / 60.0,
                                                2)}
        return track_metadata


def get_token():
    token_valid = False
    token_info = session.get("token_info", {})

    # Checking if the session has already stored a token
    if not (session.get('token_info', False)):
        token_valid = False
        return token_info, token_valid

    # Checking if the token has expired
    now = int(time.time())
    is_token_expired = session.get('token_info').get('expires_at') - now < 60

    # Refreshing token if it has expired
    if (is_token_expired):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(session.get('token_info').get('refresh_token'))

    token_valid = True
    return token_info, token_valid


def create_spotify_oauth():
    return SpotifyOAuth(
        client_id="616278c94375429084e241be7cef4949",
        client_secret='dbe93ff256e74afb83bceeb59f33fb4b',
        redirect_uri=url_for('is_user_authorised', _external=True),
        scope="user-library-read"
    )
