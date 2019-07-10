import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *

def process_airport_file(cur, filepath):
    # open song file
    df = pd.read_csv(filepath, lines=True)

    airport_df = df[['ident','type','name','elevation_ft','continent','gps_code','municipality','iso_country','iata_code','local_code','latitude', 'longitude']]

    for i, row in airport_df.iterrows():
        cur.execute(airport_table_insert, row)

    coordinates_df = df[['ident','type','name','elevation_ft','latitude','longitude']]

    for i, row in coordinates_df.iterrows():
        cur.execute(airport_coordinates_insert, row)



    region_df =df[['ident','continent','municipality','iso_country']]

    for i, row in region_df.iterrows():
        cur.execute(airport_region_insert, row)

    
    codes_df = df[['ident','gps_code','iata_code','local_code']]
    for i, row in codes_df.iterrows():
        cur.execute(airport_codes_insert, row)


    





def process_data(cur, conn, filepath, func):
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.csv'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    # Run the full ETL process to load and insert all data from the song and log files.

    conn = psycopg2.connect("host=127.0.0.1 dbname=airport_code user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/aiport_data', func=process_airport_file)
    

    conn.close()


if __name__ == "__main__":
    main()