import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

IAM_ROLE = config['IAM_ROLE']['ARN']
LOG_DATA = config['S3']['LOG_DATA']
SONG_DATA = config['S3']['SONG_DATA']
LOG_JSONPATH = config['S3']['LOG_JSONPATH']

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events_table"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs_table"
songplay_table_drop = "DROP TABLE IF EXISTS songplay_table"
user_table_drop = "DROP TABLE IF EXISTS user_table"
song_table_drop = "DROP TABLE IF EXISTS song_table"
artist_table_drop = "DROP TABLE IF EXISTS artist_table"
time_table_drop = "DROP TABLE IF EXISTS time_table"

# CREATE TABLES
# Redshift default diststyle=AUTO

staging_events_table_create= ("""CREATE TABLE IF NOT EXISTS staging_events(
                                artist TEXT,
                                auth TEXT,
                                firstName TEXT,
                                gender CHAR(1),
                                itemInSession INTEGER,
                                lastName TEXT,
                                length NUMERIC,
                                level TEXT,
                                location TEXT,
                                method TEXT,
                                page TEXT,
                                registration NUMERIC,
                                sessionId INTEGER,
                                song TEXT,
                                status INTEGER,
                                ts BIGINT,
                                userAgent TEXT,
                                userId INTEGER 
                                )""")

staging_songs_table_create =  ("""CREATE  TABLE IF NOT EXISTS staging_songs(
                                num_songs INTEGER,
                                artist_id TEXT,
                                artist_latitude NUMERIC,
                                artist_longitude NUMERIC,
                                artist_location TEXT,
                                artist_name TEXT,
                                song_id TEXT,
                                title TEXT,
                                duration NUMERIC,
                                year INTEGER)""")

songplay_table_create =  ("""CREATE TABLE IF NOT EXISTS songplay(
                            songplay_id INT IDENTITY(1,1) PRIMARY KEY,
                            start_time TIMESTAMP,
                            user_id INTEGER NOT NULL,
                            level TEXT,
                            song_id TEXT,
                            artist_id TEXT,
                            session_id INTEGER,
                            location TEXT,
                            user_agent TEXT)""")

user_table_create = ("""CREATE TABLE IF NOT EXISTS users(
                        user_id INTEGER PRIMARY KEY,
                        first_name TEXT NOT NULL,
                        last_name TEXT NOT NULL,
                        gender CHAR(1),
                        level TEXT)""")

song_table_create = ("""CREATE TABLE IF NOT EXISTS songs(
                        song_id TEXT SORTKEY PRIMARY KEY,
                        title TEXT,
                        artist_id TEXT,
                        year INTEGER,
                        duration NUMERIC )""")

artist_table_create = ("""CREATE TABLE IF NOT EXISTS artist(
                          artist_id TEXT SORTKEY PRIMARY KEY,
                          name TEXT,
                          location TEXT,
                          latitude NUMERIC,
                          longitude NUMERIC )""")

time_table_create = ("""CREATE TABLE IF NOT EXISTS time(
                        start_time TIMESTAMP PRIMARY KEY,
                        hour INTEGER,
                        day INTEGER,
                        week INTEGER,
                        month INTEGER,
                        year INTEGER,
                        weekDay INTEGER  )""")

# STAGING TABLES

staging_events_copy = (F"""copy staging_events 
                          from {LOG_DATA}
                          iam_role {IAM_ROLE}
                          json {LOG_JSONPATH}; """)

staging_songs_copy = (F"""copy staging_songs 
                          from {SONG_DATA} 
                          iam_role {IAM_ROLE}
                          json 'auto'; """)

# FINAL TABLES

songplay_table_insert = ("""INSERT INTO songplay (
	start_time
	,user_id
	,LEVEL
	,song_id
	,artist_id
	,session_id
	,location
	,user_agent
	)
SELECT TIMESTAMP 'epoch' + e.ts / 1000 * interval '1 second' AS start_time
	,e.userId AS user_id
	,e.LEVEL
	,s.song_id
	,s.artist_id
	,e.sessionId AS session_id
	,e.location
	,e.userAgent AS user_agent
FROM staging_events e
	,staging_songs s
WHERE e.song = s.title
	AND e.artist = s.artist_name
	AND e.length = s.duration
    AND e.page = 'NextSong' """)


user_table_insert = ("""INSERT INTO users (
	user_id
	,first_name
	,last_name
	,gender
	,LEVEL
	)
SELECT DISTINCT userId AS user_id
	,firstName AS first_name
	,lastName AS last_name
	,gender
	,LEVEL
FROM staging_events
WHERE page = 'NextSong'""")


song_table_insert = ("""INSERT INTO songs (
	song_id
	,title
	,artist_id
	,year
	,duration
	)
SELECT song_id
	,title
	,artist_id
	,year
	,duration
FROM staging_songs
WHERE song_id IS NOT NULL""")

artist_table_insert = ("""INSERT INTO artist (
	artist_id
	,name
	,location
	,latitude
	,longitude
	)
SELECT DISTINCT artist_id
	,artist_name
	,artist_location
	,artist_latitude
	,artist_longitude
FROM staging_songs
WHERE artist_id IS NOT NULL""")

time_table_insert = ("""INSERT INTO TIME(start_time, hour, day, week, month, year, weekDay)
SELECT start_time
	,extract(hour FROM start_time)
	,extract(day FROM start_time)
	,extract(week FROM start_time)
	,extract(month FROM start_time)
	,extract(year FROM start_time)
	,extract(dayofweek FROM start_time)
FROM songplay""")


# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
