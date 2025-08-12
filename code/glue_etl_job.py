"""
AWS Glue ETL Job for Spotify Dataset
------------------------------------
This job:
1. Reads raw CSV data (tracks, artists, albums) from S3 staging bucket
2. Joins datasets to form enriched music metadata
3. Applies data quality validation (column count > 0)
4. Writes output to S3 data warehouse in Parquet (snappy)

- Adjust S3 paths and column names to match your dataset.
"""

import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsgluedq.transforms import EvaluateDataQuality

# Parse job arguments (Glue will inject JOB_NAME)
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

# Initialize Glue & Spark contexts
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)


# Configuration
STAGING_PREFIX = 's3://spotify-projbucket/staging/'
TRACKS_KEY = STAGING_PREFIX + 'track.csv'
ARTISTS_KEY = STAGING_PREFIX + 'artists.csv'
ALBUMS_KEY = STAGING_PREFIX + 'albums.csv'
TARGET_PREFIX = 's3://spotify-projbucket/data_warehouse/'

# Default data quality ruleset (simple example)
DEFAULT_DATA_QUALITY_RULESET = """
    Rules = [
        ColumnCount > 0
    ]
"""

# Read CSV files as DynamicFrames

tracks_dyf = glueContext.create_dynamic_frame.from_options(
    format_options={"quoteChar": '"', "withHeader": True, "separator": ',', "optimizePerformance": False},
    connection_type='s3',
    format='csv',
    connection_options={"paths": [TRACKS_KEY], "recurse": True},
    transformation_ctx='tracks_dyf')

artists_dyf = glueContext.create_dynamic_frame.from_options(
    format_options={"quoteChar": '"', "withHeader": True, "separator": ',', "optimizePerformance": False},
    connection_type='s3',
    format='csv',
    connection_options={"paths": [ARTISTS_KEY], "recurse": True},
    transformation_ctx='artists_dyf')

albums_dyf = glueContext.create_dynamic_frame.from_options(
    format_options={"quoteChar": '"', "withHeader": True, "separator": ',', "optimizePerformance": False},
    connection_type='s3',
    format='csv',
    connection_options={"paths": [ALBUMS_KEY], "recurse": True},
    transformation_ctx='albums_dyf')

# Join artists -> albums on artist id (artists.id == albums.artist_id)
artists_albums = Join.apply(frame1=artists_dyf, frame2=albums_dyf, keys1=['id'], keys2=['artist_id'], transformation_ctx='artists_albums')

# Join the above with tracks on track_id (assuming tracks.track_id matches)
joined = Join.apply(frame1=tracks_dyf, frame2=artists_albums, keys1=['track_id'], keys2=['track_id'], transformation_ctx='tracks_artists_albums')

# Drop fields that are duplicate or not needed
cleaned = DropFields.apply(frame=joined, paths=['id', '`.track_id`'], transformation_ctx='drop_unneeded')

# This will run simple data quality checks
EvaluateDataQuality().process_rows(
    frame=cleaned,
    ruleset=DEFAULT_DATA_QUALITY_RULESET,
    publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node", "enableDataQualityResultsPublishing": True},
    additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"}
)

# Write to S3 as Parquet
glueContext.write_dynamic_frame.from_options(
    frame=cleaned,
    connection_type='s3',
    format='glueparquet',
    connection_options={"path": TARGET_PREFIX, "partitionKeys": []},
    format_options={"compression": 'snappy'},
    transformation_ctx='write_s3')

job.commit()
