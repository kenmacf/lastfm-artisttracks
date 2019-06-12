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
        return -1
    if r.json().get('error', 0) > 0:
        return -2
    try:
        user_play_count = r.json().get('artist').get('stats').get('userplaycount')
        # artist_mbid = r.json().get('artist')
        return user_play_count
    except AttributeError:
        return -3


def get_artist_tracks(artist, username=None, api_key=None, cache_method='file', cache_location='lastfm-cache'):
    if username is None or api_key is None:
        raise ValueError("username and api_key are required parameters")
    lastfm_total_artist_tracks = get_lastfm_total_artist_tracks(artist, username, api_key)
    return "artist {} tracks {}".format(artist, lastfm_total_artist_tracks)
