import psycopg2
import sql_credentials
import pandas as pd
import Spotify_Credentials
from pymongo import MongoClient
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from sqlalchemy import create_engine

client_credentials_manager = SpotifyClientCredentials(Spotify_Credentials.Client_ID,Spotify_Credentials.Secret_ID)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

client = MongoClient('localhost',27017)
db = client['billboard_3']





# ''' Grabs all values from passed columns from SQL and returns 
#       one list of unique values'''
def grab_unique_values(column_list):
    
    unique_list = []
    for column in column_list:
        cur = conn.cursor()
        query = f'''
                Select DISTINCT {column}
                FROM hot_charts;
                '''
        cur.execute(query)
        result = cur.fetchall()
        unique_list= unique_list + result
    return list(set(unique_list))

# '''Queries Spotify's API for the artist identifiers passed
#   Returns dataframe with each row being a unique artist and the columns being 
#    artist identifier, name, popularity, genres, and followers '''

def get_artist_stats(artist_list):
    cols = ['uri','name','popularity','genres','followers']
    df = pd.DataFrame(columns = cols)
    
    for artist in artist_list:
            query = sp.artist(artist[0])
            row = {'uri':[query['uri']],'name':[query['name']],'popularity':[float(query['popularity'])],
                    'genres':['|'.join(query['genres'])],'followers':[int(query['followers']['total'])]}     
            new_row = pd.DataFrame.from_dict(row)
            df = pd.concat([df,new_row]) 
                                                      
    return df 

# ''' Queries Spotify's API for the song identifiers passed 
#   Returns dataframe with each row being a unique song with different audio features 
#   as the columns'''

def get_audio_features(song_list):
    cols = ['danceability', 'energy', 'key', 'loudness', 'mode',
             'speechiness', 'acousticness', 'instrumentalness', 'liveness',
              'valence', 'tempo', 'type', 'id', 'uri', 'track_href', 'analysis_url',
               'duration_ms', 'time_signature']
    df = pd.DataFrame(columns = cols)
    for song in song_list:
        query = sp.audio_features(song[0])[0]
        new_row = pd.DataFrame(query,index = [0])
        df = pd.concat([df,new_row])
    return df

#Uploads passed dataframe to SQL Table with passed table name 
def sql_upload(df,table_name):
    engine = create_engine(sql_credentials.engine_path)
    df.to_sql(table_name,engine)

#''' Creates dataframe from SQL table hot_charts. The returned dataframe  has each song in 
#   that appeared in the top 10 of the Hot 100 as a row. Note that songs can and often are 
#   repeated if they appeared in the top 10 for multiple weeks.  
def create_song_table(conn):
    cur = conn.cursor()
    query = """ 
            SELECT * 
            FROM hot_charts
            """
    cur.execute(query)
    chart_data = cur.fetchall()
    cols = ['unique_id','date','song_id','artist_id']
    df = pd.DataFrame(columns = cols)

    for index,row in enumerate(chart_data):
        unique_ids = [str(index)+str(x) for x in range(10)]
        new_row = {'unique_id': unique_ids,'date': [row[1]] * 10, 'song_id':row[4::4],
                    'artist_id': row[5::4]}
        df = pd.concat([df,pd.DataFrame.from_dict(new_row)])
    return df

if __name__ == '__main__':
    
    
    #Instantiate connection to PostgreSQL 
    conn = psycopg2.connect(database = 'billboard',user = sql_credentials.user, password = sql_credentials.password,host = 'localhost', port = '5432')
    engine = create_engine(sql_credentials.engine_path)

    artist_columns = ['artist_id1','artist_id2','artist_id3','artist_id4',
                    'artist_id5','artist_id6','artist_id7','artist_id8',
                    'artist_id9','artist_id10']

    song_columns = ['song_id1','song_id2','song_id3','song_id4',
                'song_id5','song_id6','song_id7','song_id8',
                'song_id9','song_id10']

    unique_artists = grab_unique_values(artist_columns)
    unique_artists.remove(('NA',))
    artist_data = get_artist_stats(unique_artists)
    sql_upload(artist_data,'artists')

    unique_songs = grab_unique_values(song_columns)
    unique_songs.remove(('NA',))
    audio_features = get_audio_features(unique_songs)
    sql_upload(audio_features,'audio_features')



    song_table = create_song_table(conn)
    sql_upload(song_table,'songs')


    
    
    
    

