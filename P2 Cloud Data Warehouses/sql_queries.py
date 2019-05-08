import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events;"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs;"
songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS times;"

# CREATE TABLES

staging_events_table_create= ("""
CREATE TABLE "staging_events" (
    "artist" VARCHAR(100),
    "auth" VARCHAR(30),
    "firstName" VARCHAR(100),
    "gender" VARCHAR(10),
    "itemInSession" SMALLINT,
    "lastName" VARCHAR(50),
    "length" numeric(10,5),
    "level" VARCHAR(10),
    "location" VARCHAR(250), 
    "method" VARCHAR(10),
    "page" VARCHAR(20),
    "registeration" DECIMAL,
    "sessionId" BIGINT,
    "song" VARCHAR(250),
    "status" VARCHAR(30),
    "ts" BIGINT,
    "userAgent" VARCHAR(300),
    "userId" INTEGER
);
""")

staging_songs_table_create = ("""
CREATE TABLE "staging_songs" (
    "num_songs" INTEGER ,
    "artist_id" VARCHAR(100),
    "artist_latitude" VARCHAR(100),
    "artist_longitude" VARCHAR(100),
    "artist_location" VARCHAR(250),
    "artist_name" VARCHAR(100),
    "song_id" VARCHAR(100),
    "title" VARCHAR(200),
    "duration" numeric(10,5),
    "year" INTEGER
);
""")

songplay_table_create = ("""
CREATE TABLE songplays 
(
    songplay_id INTEGER IDENTITY(0,1) PRIMARY KEY,
    start_time TIMESTAMP NOT NULL,
    user_id INTEGER NOT NULL,
    level VARCHAR,
    song_id VARCHAR distkey, 
    artist_id VARCHAR sortkey,
    session_id INTEGER,
    location VARCHAR,
    user_agent VARCHAR
);
""")

user_table_create = ("""CREATE TABLE users
(
    user_id INTEGER PRIMARY KEY NOT NULL sortkey,
    first_name VARCHAR,
    last_name VARCHAR,
    gender VARCHAR,
    level VARCHAR
);
""")

song_table_create = ("""
CREATE TABLE songs 
(
    song_id VARCHAR PRIMARY KEY NOT NULL sortkey distkey,
    title VARCHAR,
    artist_id VARCHAR,
    year INTEGER,
    duration numeric(10,5)
);
""")

artist_table_create = ("""CREATE TABLE artists 
(
    artist_id VARCHAR PRIMARY KEY NOT NULL sortkey,
    name VARCHAR,
    location VARCHAR, 
    lattitude VARCHAR,
    longitude VARCHAR
);
""")

time_table_create = ("""CREATE TABLE times 
(
    starttime TIMESTAMP PRIMARY KEY NOT NULL sortkey,
    hour INTEGER,
    day INTEGER,
    week INTEGER,
    month INTEGER,
    year INTEGER,
    weekday INTEGER
);
""")


# STAGING TABLES

staging_events_copy = """copy staging_events from {}
    credentials 'aws_iam_role={}'
    format as json {} compupdate off  TRUNCATECOLUMNS region 'us-west-2';
""".format(config.get('S3','LOG_DATA'), config.get('IAM_ROLE', 'ARN'), config.get('S3', 'LOG_JSONPATH'))


staging_songs_copy = """copy staging_songs from {}
    credentials 'aws_iam_role={}'
    format as json 'auto' compupdate off STATUPDATE ON TRUNCATECOLUMNS region 'us-west-2';
""".format(config.get('S3','SONG_DATA'), config.get('IAM_ROLE', 'ARN'))

# FINAL TABLES

songplay_table_insert = ("""
INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
    SELECT 
        TIMESTAMP 'epoch' + ts/1000 * interval '1 second',
        userId,
        level,
        song_id,
        artist_id,
        sessionId,
        location,
        userAgent
        FROM staging_songs s JOIN staging_events e
        ON s.artist_name = e.artist 
        AND s.title = e.song
        AND e.length = s.duration
        WHERE e.page ='NextSong' """)
                        

user_table_insert = ("""INSERT INTO users
    SELECT 
        DISTINCT userId,
        firstName,
        lastName,
        gender,
        level FROM staging_events where page != 'NextSong' 
        AND userId is not NULL """)
                    

song_table_insert = ("""INSERT INTO songs
    SELECT 
        DISTINCT song_id,
        title,
        artist_id,
        year,
        duration FROM staging_songs where song_id is not null """)
                    

artist_table_insert = ("""INSERT INTO artists
    SELECT 
        DISTINCT artist_id,
        artist_name,
        artist_location,
        artist_latitude,
        artist_longitude FROM staging_songs where artist_id is not null """)
        

time_table_insert = ("""INSERT INTO times
    SELECT 
        distinct starttime,
        EXTRACT(hour from starttime) as hour,
        EXTRACT(day from starttime) as day,
        EXTRACT(week from starttime) as week,
        EXTRACT(month from starttime) as month,
        EXTRACT(year from starttime) as year,
        EXTRACT(weekday from starttime) as weekday 
        FROM   
            (SELECT TIMESTAMP 'epoch' + e.ts/1000 * interval '1 second' AS starttime
            FROM staging_events e)
        """)

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
