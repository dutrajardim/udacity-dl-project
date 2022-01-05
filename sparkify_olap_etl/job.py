from pyspark.sql import SparkSession

def olap_job(spark, input_data, output_data):
    """
    Description:
        This function is responsible for running all needed tasks
        to retrive data, transform and save sparkify olap cube queries in
        the output data address.

    Arguments:
        spark: Spark session.
        input_data: S3 address where the log data is stored.
        output_data: S3 address where the result will be stored. 

    Returns:
        None.
    """

    # loading fact table
    df_songplays = spark.read.format("parquet").load("%ssongplays.parquet" % input_data)

    # loading dimension tables
    df_times = spark.read.format("parquet").load("%stimes.parquet" % input_data)
    df_artists = spark.read.format("parquet").load("%sartists.parquet" % input_data)
    df_users = spark.read.format("parquet").load("%susers.parquet" % input_data)
    df_songs = spark.read.format("parquet").load("%ssongs.parquet" % input_data)

    # creating a olap cube with artist name, user level and weekday
    # artists.name, users.level, times.weekday
    cube_level_weekday_name = \
        df_songplays \
            .join(df_times, on="start_time", how="left") \
            .join(df_artists, on="artist_id", how="left") \
            .fillna("unknown", subset=["name"]) \
            .cube("level", "weekday", "name") \
            .count()
    
    # saving to s3 bucket
    cube_level_weekday_name \
        .write \
        .format("parquet") \
        .mode("overwrite") \
        .save("%susers_level-times_weekday-artist_name.parquet" % output_data)

    # creating a olap cube with song year, user gender and week of the year
    # times.week, users.gender, songs.weekday
    cube_year_week_gender = \
        df_songplays.select(["start_time", "user_id", "song_id"]) \
            .join(df_times.select(["start_time", "week"]), on="start_time", how="left") \
            .join(df_users.select(["user_id", "gender"]), on="user_id", how="left") \
            .join(df_songs.select(["song_id", "year"]), on="song_id", how="left") \
            .fillna({
                "gender": "unknown",
                "year": -1
            }) \
            .cube("year", "week", "gender") \
            .count()

    # saving to s3 bucket
    cube_year_week_gender \
        .write \
        .format("parquet") \
        .mode("overwrite") \
        .save("%ssongs_year-times_week-users_gender.parquet" % output_data)

def main(sparkConf = None):
    """
    Description:
        This function is responsible for starting
        a spark session, defining input and output s3 bucket,
        starting sparkify olap job, and
        after that, closing spark session.
    
    Arguments:
        sparkConf: spark session configuration (pyspark.SparkConf)
    
    Returns:
        None.
    """

    # starting spark session
    if sparkConf:
        spark = SparkSession.builder \
            .config(conf=sparkConf) \
            .getOrCreate()
    else:
        spark = SparkSession.builder \
            .appName("Udacity - Data Lake Project (OLAP)") \
            .getOrCreate()
    
    # defining project sources paths 
    output_data = "s3a://dutrajardim/udacity-dl-project/olap-cubes/"
    input_data = "s3a://dutrajardim/udacity-dl-project/"

    # stating olap job
    olap_job(spark, input_data, output_data)
    
    # closing spark session
    spark.stop()