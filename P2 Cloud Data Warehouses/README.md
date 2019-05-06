Cloud Data Warehouses-redshift
==========================================
## Table of contents

1.Goal

2.Project Datasets

3.File Description

4.Schema for Song Play Analysis

5.Instructions

## Goal

A music streaming startup, Sparkify, has grown their user base and song database and want to move their processes and data onto the cloud. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

In this project 3, we are going to use two Amazon Web Services, S3 (Data storage) and Redshift (Data warehouse with columnar storage) and building an ETL pipeline that extracts their data from S3, stages them in Redshift, and transforms data into a set of dimensional tables for Sparkify analytics team to continue finding insights in what songs their users are listening to. You'll be able to test your database and ETL pipeline by running queries given to you by the analytics team from Sparkify and compare your results with their expected results.

## Project Datasets

There are two datasets that reside in S3. Here are the S3 links for each:

Song data: s3://udacity-dend/song_data
Log data: s3://udacity-dend/log_data
Log data json path: s3://udacity-dend/log_json_path.json

* Song Dataset

-song_data/A/B/C/TRABCEI128F424C983.json
-song_data/A/A/B/TRAABJL12903CDCF1A.json

And below is an example of what a single song file, TRAABJL12903CDCF1A.json, looks like.

-{"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}

* Log Dataset

-log_data/2018/11/2018-11-12-events.json
-log_data/2018/11/2018-11-13-events.json
below is an example of what the data in a log file, 2018-11-12-events.json, looks like
![example](./log-data.png)





## File Description

 
- create_tables.py: helper functions to create fact and dimension tables for the star schema in Redshift.

- etl.py : helper functions to load data from S3 into staging tables on Redshift and then process that data into your analytics tables on Redshift

- sql_queries.py: helper functions to define SQL statements, which will be imported into the two other files above.

- README.md is  providing discussion on your process and decisions for this ETL pipeline



## Schema for Song Play Analysis



*Fact Table


songplays - records in event data associated with song plays i.e. records with page NextSong

songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent


*Dimension Tables


users - users in the app
user_id, first_name, last_name, gender, level

songs - songs in music database
song_id, title, artist_id, year, duration

artists - artists in music database
artist_id, name, location, lattitude, longitude

time - timestamps of records in songplays broken down into specific units
start_time, hour, day, week, month, year, weekday


*Staging Table

staging songs-

num_songs, artist_latitude, artist_longitude, artist_location, artist_name, song_id, title, duration, year

staging event-

artist,auth,firstName,gender,itemInSession,lastName,length,level,location,method,page,registeration,sessionId,song,status,ts,userAgent,userId  


## Instructions


1.Fill in the requiered credentials in dwh.cfg file.

2.open the terminal

3.run create_tables.py -> python create_tables.py

4.run etl.py -> python etl.py
