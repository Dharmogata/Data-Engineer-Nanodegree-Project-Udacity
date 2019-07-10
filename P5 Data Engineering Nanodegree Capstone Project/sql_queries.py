# DROP TABLES

airport_full_table_drop = "DROP TABLE IF EXISTS airport_full"
airport_coordinates_table_drop = "DROP TABLE IF EXISTS airport_coordinates"
airport_region_table_drop = "DROP TABLE IF EXISTS airport_region"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES



airport_full_table_create = ("""
CREATE TABLE IF NOT EXISTS airport_full (
    ident varchar,
    type varchar,
    name varchar,
    elevation_ft float,
    continent varchar,
    gps_code varchar,
    municipality varchar,
    iso_country varchar,
    iata_code varchar,
    local_code varchar,
    latitude float, 
    longitude float

);
""")

airport_coordinates_table_create = ("""
CREATE TABLE IF NOT EXISTS airport_coordinates (
    ident varchar,
    type varchar,
    name varchar,
    elevation_ft float,
    latitude float, 
    longitude float
);
""")



airport_region_table_create = ("""
CREATE TABLE IF NOT EXISTS airport_region (
    ident varchar,
    continent varchar,
    municipality varchar,
    iso_country varchar
);
""")

airport_codes_table_create = ("""
CREATE TABLE IF NOT EXISTS airport_codes (
    ident varchar,
    gps_code varchar,
    iata_code varchar,
    local_code varchar
);
""")



# INSERT RECORDS



airport_table_insert = ("""
INSERT INTO airport_full (ident,type,name,elevation_ft,continent,gps_code,municipality,iso_country,iata_code,local_code,latitude, longitude) \
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
""")

airport_coordinates_insert = ("""
INSERT INTO airport_coordinates (ident,type,name,elevation_ft,latitude,longitude) \
VALUES (%s, %s, %s, %s, %s, %s);
""")

airport_region_insert = ("""
INSERT INTO airport_region (ident,continent,municipality,iso_country) \
VALUES (%s, %s, %s, %s);
""")

airport_codes_insert = ("""
INSERT INTO airport_codes (ident,gps_code,iata_code,local_code) \
VALUES (%s, %s, %s, %s);
""")



# QUERY LISTS
create_table_queries = [airport_full_table_create, airport_coordinates_table_create, airport_region_table_create, airport_codes_table_create ]

drop_table_queries = [airport_full_table_drop, airport_coordinates_table_drop, airport_region_table_drop, airport_codes_table_drop]