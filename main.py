# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import spotipy
from bottle import route, run
from flask import Flask, url_for, request, session, redirect
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)

app.secret_key = "anr%%!e(tv%+q1siv-e5xkb!k"
app.config['SESSION_COOKIE_NAME'] = 'SpotifyProject Cookie'


@app.route('/')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


@app.route('/redirect')
def redirect():
    return 'redirect'


@app.route('/getTracks')
def getTracks():
    return "Users History"


def create_spotify_oauth():
    return SpotifyOAuth(
        client_id="616278c94375429084e241be7cef4949",
        client_secret='dbe93ff256e74afb83bceeb59f33fb4b',
        redirect_uri=url_for('/redirect', _external=True),
        scope="user-library-read"
    )


app.run(host='localhost', port=8080)
