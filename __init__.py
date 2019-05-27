#!/usr/bin/python3

import json
import requests


def get_settings_from_json():
    return json.load(open('/home/ksm/lastfm-revive/settings.json', "r"))


def get_lastfm_total_artist_tracks(artist, settings):
    params = {
        'artist': artist,
        'autocorrect': 1,
        'username': settings['username'],
        'api_key': settings['api_key'],
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
    #
    # print(json.dumps(r.json(), indent=2))
    # return 0


def get_artist_tracks(artist):
    settings = get_settings_from_json()
    lastfm_total_artist_tracks = get_lastfm_total_artist_tracks(artist, settings)
    return "hello world " + str(lastfm_total_artist_tracks)


# if __name__ == "__main__":
#     tracks = get_artist_tracks('Foo Fighters')
#     print(tracks)
