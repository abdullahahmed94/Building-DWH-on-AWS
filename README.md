--*Project description

Sparkify is a music streaming startup with a growing user base and song database 
and want to move their processes and data onto the cloud.
Their data resides in S3, in a directory of JSON logs on user activity on the app
The goal of the current project is to build an ETL pipeline that extracts their data from S3,
stages them in Redshift, and transforms data into a set of dimensional tables for their analytics team 
to continue finding insights in what songs their users are listening to.

--*How to run
To run this project you need to :

1- build your redshift cluster then add you connection and security credintials into dwh.cfg file first:
2- Run the create_tables script to set up the database staging and analytical tables
3- run the etl script to extract data from the files in S3, stage it into the staging tables,
 and finally store it in the dimensional and the faclt tables  .

--*Database schema design

**Staging Tables:-

1- staging_events
2- staging_songs

**Fact Table:-

songplays - records in event data associated with song plays i.e. records with page NextSong - songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent

**Dimension Tables:-

1- users : users in the app - user_id, first_name, last_name, gender, level
2- songs : songs in music database - song_id, title, artist_id, year, duration
3- artists : artists in music database - artist_id, name, location, lattitude, longitude
4- time : timestamps of records in songplays broken down into specific units - start_time, hour, day, week, month, year, weekday
