from pyspark.sql import SparkSession

def olap_job(spark, input_data, output_data):
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

    df_songplays = spark.read.format('parquet').load('%ssongplays.parquet' % input_data)
    df_times = spark.read.format('parquet').load('%stimes.parquet' % input_data)
    df_artists = spark.read.format('parquet').load('%sartists.parquet' % input_data)
    df_users = spark.read.format('parquet').load('%susers.parquet' % input_data)
    df_songs = spark.read.format('parquet').load('%ssongs.parquet' % input_data)

    # artists.name, songplays.level, times.weekday
    cube_level_weekday_name = \
        df_songplays \
            .join(df_times, on='start_time', how='left') \
            .join(df_artists, on='artist_id', how='left') \
            .fillna("unknown", subset=['name']) \
            .cube('level', 'weekday', 'name')
    
    cube_level_weekday_name.count() \
        .write.format('parquet') \
        .mode('overwrite') \
        .save('%slevel-weekday-artist.parquet' % output_data)

    cube_year_week_gender = \
        df_songplays.select(['start_time', 'user_id', 'song_id']) \
            .join(df_times.select(['start_time', 'week']), on='start_time', how='left') \
            .join(df_users.select(['user_id', 'gender']), on='user_id', how='left') \
            .join(df_songs.select(['song_id', 'year']), on='song_id', how='left') \
            .fillna({
                'gender': "unknown",
                'year': -1
            }) \
            .cube('year', 'week', 'gender')

    cube_year_week_gender.count() \
        .write.format('parquet') \
        .mode('overwrite') \
        .save('%syear-week-gender.parquet' % output_data)

def main():
    """
    Description:
        This function is responsible for starting
        a spark session, defining input and output s3 bucket,
        starting sparkify olap job, and
        after that, closing spark session.
    
    Arguments:
        None.
    
    Returns:
        None.
    """
    # starting spark session
    spark = SparkSession.builder \
        .appName("Udacity - Data Lake Project (OLAP)") \
        .getOrCreate()
    
    # defining project sources paths 
    output_data = "s3a://udacity-dend/olap-cubes"
    input_data = "s3a://dutrajardim/udacity-dl-project/"

    # stating olap job
    olap_job(spark, input_data, output_data)
    
    # closing spark session
    spark.stop()