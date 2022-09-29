## Submission

This folder contains the files and scripts for Spotify API
    Data Engineering Project by Andres Aguilar


### Environment Variables

For use of code in this repo, Spotify API credentials have to be set in your working environment

`SPOTIFY_CLIENT_ID`

`SPOTIFY_CLIENT_SECRET`

`SPOTIFY_REDIRECT_URL`

These can be created at [Spotify for Developers](https://developer.spotify.com/dashboard/login)

### File Structure

```
submissions
├── main.py
├── visualization.pdf
└── Python_Modules
    ├── data_ingestion.py          # Data ingestion and transformation
    ├── data_viz.py                # Plotting funtions
    └── spotify_db.py              # Database class

```
The script for creating database with list of artists and wiriting View and Query statments
is `main.py`

In `Python_Modules` folder:

* `spotify_db.py` - has the code for the custom database class using
    SQLite3 and class methods for creating, connecting to, inserting
    and querying to the database.

* `data_ingestion.py` - holds the functions for making the Spotify API calls,
    ingestion of data, formatting and transforming data, and creating the 
    database tables for the given database.

* `data_viz.py` - functions for creating and saving plots

### Python Requirements

The following python packages are required to be installed to run the scripts in this repository:

* `seaborn`
* `spotipy`
* `sqlite3`
* `numpy`
* `pandas`

### Data Format

The following tables describe the columns and their respective datatypes for tables in the Database

#### ARTIST

| Column       |   Data Type  | Description                                                                           |
|--------------|:------------:|---------------------------------------------------------------------------------------|
| artist_id    |  varchar(50) | Spotify ID of the artist                                                              |
| artist_name  | varchar(255) | Name of the artist                                                                    |
| external_url | varchar(100) | Spotify URL for the artist                                                            |
| genre        | varchar(100) | One genre that the artist  is associate with                                          |
| image_url    | varchar(100) | The source URL for the image of the artist                                            |
| followers    |      int     | The total number of followers                                                         |
| popularity   |      int     | Popularity value from 0 to 100. Calculated from the popularity of the artist's tracks |
| type         |  varchar(50) | Object type, in this case: 'artist'                                                   |
| artist_uri   | varchar(100) | The Spotify resource indentifier  for the artist                                      |

#### ALBUM

| Column       |   Data Type  | Description                                             |
|--------------|:------------:|---------------------------------------------------------|
| album_id     |  varchar(50) | Spotify ID of the album                                 |
| album_name   | varchar(255) | Name of the album                                       |
| external_url | varchar(100) | Spotify URL for the album                               |
| image_url    | varchar(100) | The source URL for the image of the album               |
| release_date |     date     | The date the album was first released                   |
| total_tracks |      int     | The total number of tracks in  the album                |
| type         |  varchar(50) | Object type, in this case: 'album'                      |
| album_uri    | varchar(100) | The Spotify resource identifier for the album           |
| artist_uri   | varchar(100) | The Spotify resource identifier  for the album's artist |

#### TRACK

| Column       |   Data Type  | Description                                           |
|--------------|:------------:|-------------------------------------------------------|
| track_id     |  varchar(50) | Spotify ID of the track                               |
| song_name    | varchar(255) | Name of the track                                     |
| external_url | varchar(100) | Spotify URL for the track                             |
| duration_ms  |      int     | The track length in milliseconds                      |
| explicit     |    boolean   | Whether or not the track has  explicit lyrics         |
| disc_number  |      int     | The disc number, usually 1                            |
| type         |  varchar(50) | Object type, in this case: 'track'                    |
| song_uri     | varchar(100) | The Spotify resource identifier  for the track        |
| album_uri    |  varchar(50) | The Spotify resource identifier for the track's album |

##### TRACK_FEATURE

| Column           |   Data Type  | Description                                                                                                                                                               |
|------------------|:------------:|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| track_id         |  varchar(50) | Spotify ID of the track                                                                                                                                                   |
| danceability     |    double    | Represents how suitable the track is for dancing based on a<br>combination of musical elements including tempo, rhythm <br>stability, beat strength and overall regularity |
| energy           |    double    | Measure from 0.0 to 1.0 that represents the <br>perceptual measure of intensity and activity                                                                              |
| instrumentalness |    double    | Predicts whether a track contains no vocals.                                                                                                                              |
| liveness         |    double    | Detects the presence of an audience in the<br>recording                                                                                                                   |
| loudness         |    double    | The overall loudness of a track in decibels (dB)                                                                                                                          |
| tempo            | double       | The overall estimated tempo of a track in<br>beats per minute                                                                                                             |
| type             |  varchar(50) | Object type, in this case: 'audio_features'                                                                                                                               |
| valence          | double       | A measure from 0.0 to 1.0 describing the musical<br>positiveness conveyed by the track                                                                                    |
| song_uri         | varchar(100) | The Spotify resource identifier <br>for the track                                                                                                                         |
