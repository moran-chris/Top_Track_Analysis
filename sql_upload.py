import psycopg2
import sql_credentials
import pandas as pd

create_chart_query = '''
        CREATE TABLE charts (
            date VARCHAR,
            song_1 VARCHAR,
            artist_1 VARCHAR,
            song_id1 VARCHAR,
            artist_id1 VARCHAR,
            song_2 VARCHAR,
            artist_2 VARCHAR,
            song_id2 VARCHAR,
            artist_id2 VARCHAR,
            song_3 VARCHAR,
            artist_3 VARCHAR,
            song_id3 VARCHAR,
            artist_id3 VARCHAR,
            song_4 VARCHAR,
            artist_4 VARCHAR,
            song_id4 VARCHAR,
            artist_id4 VARCHAR,
            song_5 VARCHAR,
            artist_5 VARCHAR,
            song_id5 VARCHAR,
            artist_id5 VARCHAR,
            song_6 VARCHAR,
            artist_6 VARCHAR,
            song_id6 VARCHAR,
            artist_id6 VARCHAR,
            song_7 VARCHAR,
            artist_7 VARCHAR,
            song_id7 VARCHAR,
            artist_id7 VARCHAR,
            song_8 VARCHAR,
            artist_8 VARCHAR,
            song_id8 VARCHAR,
            artist_id8 VARCHAR,
            song_9 VARCHAR,
            artist_9 VARCHAR,
            song_id9 VARCHAR,
            artist_id9 VARCHAR,
            song_10 VARCHAR,
            artist_10 VARCHAR,
            song_id10 VARCHAR,
            artist_id10 VARCHAR);'''
chart_file = 'charts_cleaned.csv'
populate_chart_sql = """
                COPY charts FROM stdin WITH CSV HEADER
                DELIMITER as ','
                """

def create_table(query):
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()

def populate_table(file_path,sql_script):
    cur = conn.cursor()
    copy_sql = sql_script

    with open(file_path, 'r') as f:
        cur.copy_expert(sql=copy_sql, file=f)
        conn.commit()
        cur.close()
    conn.commit()

if __name__ == '__main__':
    conn = psycopg2.connect(database = 'billboard',user = sql_credentials.user, password = sql_credentials.password,host = 'localhost', port = '5432')
    cur = conn.cursor()

    query = ''' SELECT DISTINCT artist_8,artist_id8
                FROM hot_charts
                WHERE date = '2013-02-02';'''
    cur.execute(query)
    test = cur.fetchall()
    #create_table(create_chart_query)
    #populate_table(chart_file,populate_chart_sql)
    