from pyspark.sql.functions import (expr, broadcast)
from pyspark.sql import SparkSession

from sparkify_star_schema_etl.tasks.users import (save_users, extract_users)
from sparkify_star_schema_etl.tasks.artists import (save_artists, extract_artists)
from sparkify_star_schema_etl.tasks.songplays import (save_songplays, extract_songplays)
from sparkify_star_schema_etl.tasks.songs import (save_songs, extract_songs)
from sparkify_star_schema_etl.tasks.times import (save_times, extract_times)
from sparkify_star_schema_etl.tasks.source_data import (extract_log_data, extract_song_data)
from sparkify_star_schema_etl.helpers import s3_path_exists

def process_song_data(spark, input_data, output_data):
    """
    Description:
        This function is responsible for running all needed tasks
        to process, transform and save songs data in the output data address.

    Arguments:
        spark: Spark session.
        input_data: S3 address where the log data is stored.
        output_data: S3 address where the result will be stored. 

    Returns:
        None.
    """
    
    # loading staging song data
    df_song_data = extract_song_data(spark, input_data).alias('song_data')

    # check if there is old data stored
    is_first_save = not s3_path_exists(spark.sparkContext, '%ssongs.parquet' % output_data)

    # filtering new data
    if is_first_save:

        # when there is no data stored, everthing is new
        df_song_data_news = df_song_data

    else:
        # recovering stored songs to filter new data
        df_stored_songs = spark.read.format('parquet') \
            .load('%ssongs.parquet' % output_data) \
            .select('artist_id', 'song_id')

        # fitering by left anti join   
        df_song_data_news = df_song_data.join(
            other=df_stored_songs,
            on=['artist_id', 'song_id'],
            how='leftanti'
        ).persist()

    # extracting and saving songs
    df_songs = extract_songs(df_song_data_news)
    save_songs(spark, df_songs, output_data, is_first_save)

    # extracting and saving artists
    df_artists = extract_artists(df_song_data_news)
    save_artists(spark, df_artists, output_data, is_first_save)


def process_log_data(spark, input_data, output_data):
    """
    Description:
        This function is responsible for running all needed tasks
        to process, transform and save log data in the output data address.

    Arguments:
        spark: Spark session.
        input_data: S3 address where the log data is stored.
        output_data: S3 address where the result will be stored. 

    Returns:
        None.
    """
    
    # loading staging log data
    df_log_data = extract_log_data(spark, input_data).alias('log_data')

    # check if there is old data stored
    is_first_save = not s3_path_exists(spark.sparkContext, '%ssongplays.parquet' % output_data)
    
    # filtering new data
    if is_first_save:
        # when there is no data stored, everthing is new
        df_log_data_news = df_log_data
        
    else:
        # recovering stored songs to filter new data
        df_stored_songplays = spark.read.format('parquet') \
            .load('%ssongplays.parquet' % output_data) \
            .select('session_id', 'start_time') \
            .alias('stored_songplays')

        # fitering by left anti join   
        on_condition= expr("""
            log_data.sessionId = stored_songplays.session_id AND
            to_timestamp(log_data.ts / 1000) = stored_songplays.start_time
        """)
        df_log_data_news = df_log_data.join(df_stored_songplays, on_condition, 'leftanti').persist()
    

    # extracting and saving users
    df_users = extract_users(df_log_data_news)
    save_users(spark, df_users, output_data, is_first_save)

    # recovering stored songs to find ids
    df_stored_songs = spark.read.format('parquet') \
        .load('%ssongs.parquet' % output_data) \
        .select("song_id", "artist_id", "title", "duration") \
        .alias('song_data')

    # merging song data columns tring to find song_id and artist_id
    on_condition = expr("""
        log_data.song = song_data.title AND 
        ROUND(log_data.length, 4) = ROUND(song_data.duration, 4)
    """)
    df_joined = df_stored_songs.join(broadcast(df_log_data_news), on_condition, "right")

    # extracting and saving songplays
    df_songplays = extract_songplays(df_joined).persist()
    save_songplays(spark, df_songplays, output_data, is_first_save)

    # extracting and saving times
    df_times = extract_times(df_songplays)
    save_times(spark, df_times, output_data, is_first_save)


def main():
    """
    Description:
        This function is responsible for starting
        a spark session, defining input and output s3 bucket,
        starting sparkify star schema job, and
        after that, closing spark session.
    
    Arguments:
        None.
    
    Returns:
        None.
    """
    # starting spark session
    spark = SparkSession.builder \
        .appName("Udacity - Data Lake Project") \
        .getOrCreate()
    
    # defining project sources paths 
    input_data = "s3a://udacity-dend/"
    output_data = "s3a://dutrajardim/udacity-dl-project/"

    # processing data
    process_song_data(spark, input_data, output_data)
    process_log_data(spark, input_data, output_data)
    
    # closing spark session
    spark.stop()