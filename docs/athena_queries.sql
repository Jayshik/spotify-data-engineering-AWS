-- Athena sample queries for the Spotify data warehouse table (replace table name accordingly)

-- 1) Top 10 most popular tracks
SELECT track_name, track_popularity
FROM spotify_db.data_warehouse
ORDER BY track_popularity DESC
LIMIT 10;

-- 2) Average danceability by artist
SELECT artist_name, AVG(danceability) AS avg_danceability
FROM spotify_db.data_warehouse
GROUP BY artist_name
ORDER BY avg_danceability DESC
LIMIT 20;

-- 3) Albums released per year (requires release_date in ISO format)
SELECT year(from_iso8601_timestamp(release_date)) AS release_year, count(*) AS albums
FROM spotify_db.data_warehouse
GROUP BY year
ORDER BY release_year DESC;
