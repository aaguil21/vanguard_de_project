#This script will create/establish connection to a dataframe
#Then create API calls to Spotify and ingest data and transform it
#Afterwards data will be loaded to database
#Queries are then used to create Views in the database and to create plots

#In this ETL process, it is important that enviormental variables for Spotify API are set
#Otherwise an error will occur when checking credentials
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import matplotlib.pyplot as plt
import sys
import os

client_id = os.getenv('SPOTIPY_CLIENT_ID')
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
sys.path.insert(1, './Python_Modules')

import data_ingestion
import data_viz
import spotify_db as sp

artist_list = ['Arctic Monkeys', 'The Strokes', 'BTS', 'Bad Bunny', 'Epik High', 'DPR LIVE', 'Led Zeppelin',
               'The Black Keys', 'Yui', 'GOT7', 'The Beatles', 'Day6', 'Lee Hi', 'Yerin Baek', 'Justin Bieber',
               'Red Velvet', 'Red Hot Chili Peppers', 'Ed Maverick', 'ASIAN KUNG-FU GENERATION', 'Mino Song']


db = sp.spotify_db()
spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))
#spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
data_ingestion.create_tables(spotify, artist_list, db)

# Create view for top 10 songs by artists in terms of duration_ms
#
query_1 = """
CREATE VIEW IF NOT EXISTS top_songs_by_duration AS
SELECT
    artist_name, duration_ms, album_name, song_name
FROM(
    SELECT
        a.artist_name , aa.album_name,  t.song_name,
        t.duration_ms,
        ROW_NUMBER() OVER(PARTITION BY a.artist_name ORDER BY t.duration_ms) as rank
    FROM artist a
    JOIN album aa
    ON a.artist_id = aa.artist_id
    JOIN track t
    ON aa.album_id = t.album_id
    )
WHERE rank <= 10
ORDER BY artist_name ASC , duration_ms DESC
;
"""
db.query_view(query_1, 'top_songs_by_duration')

# View for top 20 artists in the database ordered by # of followers
#
query_2 = """
CREATE VIEW IF NOT EXISTS top_artists_by_followers AS
SELECT artist_name AS Artist, followers, popularity, genre
FROM artist
ORDER by followers DESC
;
"""
db.query_view(query_2, 'top_artists_by_followers')

# View for songs by artist in terms of tempo
#
query_3 = """
CREATE VIEW IF NOT EXISTS top_songs_by_tempo AS
SELECT
    artist_name, tempo, song_name, album_name, duration_ms, danceability,
    energy
FROM(
    SELECT
        a.artist_name , aa.album_name, t.song_name,
        t.duration_ms, tf.tempo, tf.danceability, tf.energy,
        ROW_NUMBER() OVER (PARTITION BY a.artist_name ORDER BY tf.tempo) as rank
    FROM artist a
    JOIN album aa
        ON a.artist_id = aa.artist_id
    JOIN track t
        ON aa.album_id = t.album_id
    JOIN track_feature tf
        ON t.track_id = tf.track_id
    )
WHERE rank <= 10
ORDER BY artist_name ASC, tempo DESC
;
"""
db.query_view(query_3, 'top_songs_by_tempo')

# View for top artist in terms of explicit tracks
query_4 = """
CREATE VIEW IF NOT EXISTS top_artist_by_explicit_tracks AS
SELECT a.artist_name, t.*, a.followers, a.popularity, a.genre
FROM artist a
JOIN (
    SELECT
        count(CASE WHEN track.explicit THEN 1 END) as num_explicit, album.artist_id as artist_id,
        AVG(loudness) as avg_loudness, AVG(energy) as avg_energy, AVG(tempo) as avg_tempo,
        AVG(valence) as avg_valence
    FROM album
    JOIN track
        ON album.album_id = track.album_id
    JOIN track_feature tf
        ON track.track_id = tf.track_id
    GROUP BY album.artist_id
    ) AS t
ON t.artist_id = a.artist_id
ORDER BY t.num_explicit Desc
;
"""
db.query_view(query_4, 'top_artist_by_explicit_tracks')

# View for albums order by average song duration
#
query_5 = """
CREATE VIEW IF NOT EXISTS top_albums_by_avg_duration AS
SELECT album_len.*, artist_name, followers, popularity
FROM (
    SELECT
        album_name, sum(duration_ms)/(total_tracks) as avg_song_duration,
        AVG(loudness) as avg_loudness, AVG(tempo) as avg_tempo,
        AVG(instrumentalness) as avg_instrumentalness,
        AVG(danceability) as avg_danceability, AVG(valence) as avg_valence,
        AVG(energy) as avg_energy, AVG(liveness) as avg_liveness, artist_id
    FROM album
    JOIN track ON album.album_id = track.album_id
    JOIN track_feature tf
        ON track.track_id = tf.track_id
    GROUP BY album_name
    ) as album_len
LEFT JOIN artist
    ON artist.artist_id = album_len.artist_id
ORDER BY avg_song_duration
;
"""
db.query_view(query_5, 'top_albums_by_avg_duration')

# Query to create dataframe for the plotting of a correlation heat map between audio
#
corr_viz_query = """
SELECT *
FROM top_albums_by_avg_duration
"""

#Visualtion of box plot for danceablity distribution per genre
#
violin_viz_query = """
SELECT genre, danceability
FROM track_feature tf
JOIN track ON track.track_id = tf.track_id
JOIN album ON album.album_id = track.album_id
JOIN artist ON artist.artist_id = album.artist_id
"""

# Visualization query to create violin plot for energy by follower quantile
#
boxplot_viz_query = """
SELECT Followers, Energy
FROM artist as a
JOIN album aa
    ON a.artist_id = aa.artist_id
JOIN track t
    ON aa.album_id = t.album_id
JOIN track_feature tf
    ON t.track_id = tf.track_id
"""

fig1, fig2, fig3 = data_viz.save_plots(corr_viz_query, violin_viz_query, boxplot_viz_query, db)
plt.show()
