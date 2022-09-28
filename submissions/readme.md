## Submission README

This folder contains the files and scripts for Sportify API
    Data Engineering Project.


### Enviroment Variables

For use of code in this repo, Spotify API credentials have to be set in your .env 

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
is 
`main.py`

In `Python_Modules` folder:

* `spotify_db.py` - has the code for the custom database class using
    SQLite3 and class methods for creating, connecting to, inserting
    and querying to the database. 

* `data_ingestion.py` - holds the functions for making the Spotify API calls, 
    ingestion of data, formatting and transfroming data, and creating the 
    database tables for the given database.

* `data_viz.py` - functions for creating and saving plots 


#### Data Format
