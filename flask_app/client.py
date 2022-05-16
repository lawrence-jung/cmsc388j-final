import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from decouple import config

def get_songs(q):

    auth_manager = SpotifyClientCredentials(config('SPOTIPY_CLIENT_ID'), config('SPOTIPY_CLIENT_SECRET'))
    sp = spotipy.Spotify(auth_manager=auth_manager)

    results = sp.search(q, limit=10, offset=0, type='track', market=None)
    tracks = results['tracks']

    songs = []
    for i in tracks['items']:

        s = i['name'] + " by "
        for a in i['album']['artists']:
            s += (a['name'] + ", ")
        songs.append(s[:-2])
    
    return songs