#!/usr/bin/python3

import json
import requests


def get_settings_from_json():
    return json.load(open('settings.json', "r"))


def get_lastfm_total_artist_tracks(artist, username, api_key):
    params = {
        'artist': artist,
        'autocorrect': 1,
        'username': username,
        'api_key': api_key,
        'format': 'json'
    }
    r = requests.get('http://ws.audioscrobbler.com/2.0/?method=artist.getInfo', params=params)
    if r.status_code != requests.codes.ok:
        return 0
    if r.json().get('error', 0) > 0:
        return 0
    try:
        return r.json().get('artist').get('stats').get('userplaycount')
    except AttributeError:
        return 0


def get_artist_tracks(artist, username=None, api_key=None, use_cache=True, cache_directory='lastfm-cache'):
    if username is None or api_key is None:
        raise ValueError("username and api_key are required parameters")
    lastfm_total_artist_tracks = get_lastfm_total_artist_tracks(artist, username, api_key)
    return "hello world " + str(lastfm_total_artist_tracks)
