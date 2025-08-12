# Dataset description

The original Spotify dataset contained multiple CSVs. For this project we used three cleaned CSVs:

- albums.csv
  - album_id, album_name, artist_id, release_date, album_popularity, ...

- artists.csv
  - id, artist_name, followers, genres, ...

- track.csv
  - track_id, track_name, album_id, track_popularity, danceability, energy, loudness, mode, speechiness, liveliness, valence, ...

Note: column names may vary depending on preprocessing. Adjust the ETL script to match your exact schema.
