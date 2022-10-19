import spotipy
    from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from spotify_db import *

#Data ingestion using spotify api
def artist_col(spotify, artist_list: list):
    #Creates dictionary of lists, intializing with data type for SQLite3 table
    #Then populate dictionay with api calls to spotify per artist in artist_list
    artist_dic = {'artist_id': ['varchar(50)'],
                  'artist_name': ['varchar(255)'],
                  'external_url': ['varchar(100)'],
                  'genre': ['varchar(100)'],
                  'image_url': ['varchar(100)'],
                  'followers': ['int'],
                  'popularity': ['int'],
                  'type': ['varchar(50)'],
                  'artist_uri': ['varchar(50)']
                  }
    for name in artist_list:
        #Spotify api request for artist
        results = spotify.search(q='artist:' + name, type='artist')
        items = results['artists']['items']
        #Only keep results for which there is an artist in Spotify database
        if len(items) > 0:
            artist = items[0]
            artist_dic['artist_id'].append(artist['id'])
            artist_dic['artist_name'].append(artist['name'])
            artist_dic['external_url'].append(artist['external_urls']['spotify'])
            artist_dic['genre'].append(artist['genres'][0])
            artist_dic['image_url'].append(artist['images'][0]['url'])
            artist_dic['followers'].append(artist['followers']['total'])
            artist_dic['popularity'].append(artist['popularity'])
            artist_dic['type'].append(artist['type'])
            artist_dic['artist_uri'].append(artist['uri'])

    artist_df = pd.DataFrame(artist_dic)
    #Return Artist dataframe and list of ids, excluding datatype
    return artist_df, artist_dic['artist_id'][1:]


def album_col(spotify, artist_ids: list):
    #Create Album dictionary, intializing first item in list with data type when creating tables
    #Each list is populated with results from api call for albums correspoinding to artist_ids
    #Album results can contain missing keys
    album_dic = {'album_id': ['varchar(50)'],
                 'album_name': ['varchar(255)'],
                 'external_url': ['varchar(100)'],
                 'image_url': ['varchar(100)'],
                 'release_date': ['date'],
                 'total_tracks': ['int'],
                 'type': ['varchar(50)'],
                 'album_uri': ['varchar(50)'],
                 'artist_id': ['varchar(100)']
                 }
    for artist_id in artist_ids:
        album_results = spotify.artist_albums(artist_id=artist_id, album_type='album', country='US')
        for album in album_results['items']:
            # Check if there are any images available in results from api call
            image_url = album['images'][0]['url'] if len(album['images']) > 0 else None

            album_dic['album_id'].append(album['id'])
            album_dic['album_name'].append(album['name'])
            album_dic['external_url'].append(album['external_urls']['spotify'])
            album_dic['image_url'].append(image_url)
            album_dic['release_date'].append(album['release_date'])
            album_dic['total_tracks'].append(album['total_tracks'])
            album_dic['type'].append(album['type'])
            album_dic['album_uri'].append(album['uri'])
            album_dic['artist_id'].append(artist_id)

    album_df = pd.DataFrame(album_dic)
    # Return Album dataframe and list of ids, excluding datatype
    return album_df, album_dic['album_id'][1:]

def track_col(spotify, album_ids: list):
    #Create Track dictionary, intializing first item in list with data type when creating tables
    #Each list is populated with results from api call for albums correspoinding to album_ids
    #Album results can contain missing keys
    track_dic = {'track_id': ['varchar(50)'],
                 'song_name': ['varchar(255)'],
                 'external_url': ['varchar(100)'],
                 'duration_ms': ['int'],
                 'explicit': ['boolean'],
                 'disc_number': ['int'],
                 'type': ['varchar(50)'],
                 'song_uri': ['varchar(100)'],
                 'album_id': ['varchar(50)']
                 }
    for album_id in album_ids:
    #Store all track ids from current album in loop to use for audio_feature api call
        track_results = spotify.album_tracks(album_id=album_id, limit=50, offset=0)
        for track in track_results['items']:
            track_dic['track_id'].append(track['id'])
            track_dic['song_name'].append(track['name'])
            track_dic['external_url'].append(track['external_urls']['spotify'])
            track_dic['duration_ms'].append(track['duration_ms'])
            track_dic['explicit'].append(track['explicit'])
            track_dic['disc_number'].append(track['disc_number'])
            track_dic['type'].append(track['type'])
            track_dic['song_uri'].append(track['uri'])
            track_dic['album_id'].append(album_id)

    track_df = pd.DataFrame(track_dic)
    # Return Track dataframe and list of ids, excluding datatype
    return track_df, track_dic['track_id'][1:]

def features_col(spotify, track_ids: list):
    #Create Feature dictionary, intializing first item in list with data type when creating tables
    #Each list is populated with results from api call for albums correspoinding to track_ids
    #Track_id can result in null return from api call
    feature_dic = {'track_id': ['varchar(50)'],
                   'danceability': ['double'],
                   'energy': ['double'],
                   'instrumentalness': ['double'],
                   'liveness': ['double'],
                   'loudness': ['double'],
                   'speechiness': ['double'],
                   'tempo': ['double'],
                   'type': ['varchar(50)'],
                   'valence': ['double'],
                   'song_uri': ['varchar(100)']
                   }
    #Need to section track_ids because Spotify audio_feature only accepts 100 ids per call
    for i in range(0,len(track_ids),100):
        track_ids_sec = track_ids[i:i+100]
        features_results = spotify.audio_features(track_ids_sec)
        for features in features_results:
            #Check if track_id api call did not return null
            if features is not None:
                feature_dic['track_id'].append(features['id'])
                feature_dic['danceability'].append(features['danceability'])
                feature_dic['energy'].append(features['energy'])
                feature_dic['instrumentalness'].append(features['instrumentalness'])
                feature_dic['liveness'].append(features['liveness'])
                feature_dic['loudness'].append(features['loudness'])
                feature_dic['speechiness'].append(features['speechiness'])
                feature_dic['tempo'].append(features['tempo'])
                feature_dic['type'].append(features['type'])
                feature_dic['valence'].append(features['valence'])
                feature_dic['song_uri'].append(features['uri'])

    features_df = pd.DataFrame(feature_dic)
    return features_df



def process_data(df,columns: list):
    #Drop rows for given key columns
    df = df.dropna(axis=0, subset=columns)
    #Return dataframe after dropping duplicate rows
    return df.drop_duplicates(keep='first')


def create_tables(spotify, artist_names: list, db):
    #Create and processes dataframes from previous functions
    #Uses database class to insert dataframes as tables
    artist_df, artist_ids = artist_col(spotify, artist_names)
    album_df, album_ids = album_col(spotify, artist_ids)
    track_df, track_ids = track_col(spotify, album_ids)
    track_feature_df = features_col(spotify, track_ids)

    #Key columns for tables, null values in these columns make joins unavailable
    artist_df = process_data(artist_df, ['artist_id', 'artist_uri'])
    album_df  = process_data(album_df, ['album_id', 'album_uri', 'artist_id'])
    track_df  = process_data(track_df, ['track_id', 'song_uri', 'album_id'])
    track_feature_df = process_data(track_feature_df, ['track_id', 'song_uri'])

    dfs = [artist_df, album_df, track_df, track_feature_df]
    table_names = ['artist', 'album', 'track', 'track_feature']
    #Create table with data schema from dataframe first row
    for i, df in enumerate(dfs):
        db.add_table(table_names[i], df.iloc[1:,:], df.iloc[0,:].to_list())
    return
