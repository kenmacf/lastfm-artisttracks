#!/usr/bin/python3

import json
import requests


def lastfm_artist_getinfo(artist, username, api_key):
    params = {
        'artist': artist,
        'autocorrect': 1,
        'username': username,
        'api_key': api_key,
        'format': 'json'
    }
    r = requests.get('http://ws.audioscrobbler.com/2.0/?method=artist.getInfo', params=params)
    if r.status_code != requests.codes.ok:
        return {'error': 1, 'message': 'artist.getInfo HTTP response code error {}'.format(r.status_code)}
    if r.json().get('error', 0) > 0:
        return {'error': 2, 'message': 'artist.getInfo Last.FM error response {}'.format(r.json().get('error'))}
    try:
        user_play_count = r.json().get('artist').get('stats').get('userplaycount')
        artist_mbid = r.json().get('artist').get('mbid')
        return {'error': 0, 'user_play_count': user_play_count, 'mbid': artist_mbid}
    except AttributeError:
        return {'error': 3, 'message': 'attributes not found in JSON response'}


def get_artist_tracks_from_cache_file(mbid, cache_location):
    return {'artist_play_count': 0, 'artist_plays': [], 'tracks': []}

def get_artist_tracks_from_cache(mbid, cache_method, cache_location):
    if cache_method == 'file':
        return get_artist_tracks_from_cache_file(mbid, cache_location)

    return {'artist_play_count': 0, 'artist_plays': [], 'tracks': []}


def get_artist_tracks(artist, username=None, api_key=None, cache_method='file', cache_location='lastfm-cache'):
    if username is None or api_key is None:
        raise ValueError("username and api_key are required parameters")
    getinfo_object = lastfm_artist_getinfo(artist, username, api_key)
    if getinfo_object.get('error', 0) > 0:
        return "error: {}".format(getinfo_object.get('message'))
    cached_artist_object = get_artist_tracks_from_cache(getinfo_object.get('mbid'), cache_method, cache_location)
    return "artist {} {}".format(artist, getinfo_object)
