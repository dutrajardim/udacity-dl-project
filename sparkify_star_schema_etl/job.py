from pyspark.sql.functions import expr

from sparkify_star_schema_etl.tasks.users import save_users, extract_users
from sparkify_star_schema_etl.tasks.artists import save_artists, extract_artists
from sparkify_star_schema_etl.tasks.songplays import save_songplays, extract_songplays
from sparkify_star_schema_etl.tasks.songs import save_songs, extract_songs
from sparkify_star_schema_etl.tasks.times import save_times, extract_times
from sparkify_star_schema_etl.tasks.source_data import extract_log_data, extract_song_data


def sparkify_star_schema_job(spark, input_data, output_data):
    """
    Description:
        This function is responsible for running all needed tasks
        to retrive data, transform and save sparkify star schema in
        the output data address.

    Arguments:
        spark: Spark session.
        input_data: S3 address where the log data is stored.
        output_data: S3 address where the result will be stored. 

    Returns:
        None.
    """
    
    # loading staging song data
    df_song_data = extract_song_data(spark, input_data).alias('song_data')

    # loading staging log data
    df_log_data = extract_log_data(spark, input_data).alias('log_data')
    
    # merging song data columns tring to find song_id and artist_id
    columns = ["song_id", "artist_id", "title", "duration"]
    on_expr = "log_data.song = song_data.title AND ROUND(log_data.length, 4) = ROUND(song_data.duration, 4)"
    df_joined = df_log_data.join(
        df_song_data[columns],
        on=expr(on_expr),
        how="LEFT",
    )

    # extracting and saving songs
    df_songs = extract_songs(df_song_data)
    save_songs(spark, df_songs, output_data)

    # extracting and saving artists
    df_artists = extract_artists(df_song_data)
    save_artists(spark, df_artists, output_data)

    # extracting and saving users
    df_users = extract_users(df_log_data)
    save_users(spark, df_users, output_data)

    # extracting and saving songplays
    df_songplays = extract_songplays(df_joined)
    save_songplays(spark, df_songplays, output_data)

    # extracting and saving times
    df_times = extract_times(df_songplays)
    save_times(spark, df_times, output_data)