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

artist_columns = ['artist_id1','artist_id2','artist_id3','artist_id4',
                    'artist_id5','artist_id6','artist_id7','artist_id8',
                    'artist_id9','artist_id10']
song_columns = ['song_id1','song_id2','song_id3','song_id4',
                'song_id5','song_id6','song_id7','song_id8',
                'song_id9','song_id10']
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

def get_artist_stats(artist_list,to_mongo = False):
    cols = ['uri','name','popularity','genres','followers']
    df = pd.DataFrame(columns = cols)
    
    for artist in artist_list:
            query = sp.artist(artist[0])
            if to_mongo:
                db['artists'].insert_one(query)
            row = {'uri':[query['uri']],'name':[query['name']],'popularity':[float(query['popularity'])],
                    'genres':['|'.join(query['genres'])],'followers':[int(query['followers']['total'])]}     
            new_row = pd.DataFrame.from_dict(row)
            df = pd.concat([df,new_row]) 
                                                      
    return df 

def get_audio_features(song_list, to_mongo =False):
    cols = ['danceability', 'energy', 'key', 'loudness', 'mode',
             'speechiness', 'acousticness', 'instrumentalness', 'liveness',
              'valence', 'tempo', 'type', 'id', 'uri', 'track_href', 'analysis_url',
               'duration_ms', 'time_signature']
    df = pd.DataFrame(columns = cols)
    for song in song_list:
        query = sp.audio_features(song[0])[0]
        #if to_mongo:
            #   db['song_features'].insert_one(query)
        new_row = pd.DataFrame(query,index = [0])
        df = pd.concat([df,new_row])
    return df

def sql_upload(df,table_name):
    engine = create_engine(sql_credentials.engine_path)
    df.to_sql(table_name,engine)
def create_song_table():
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
    conn = psycopg2.connect(database = 'billboard',user = sql_credentials.user, password = sql_credentials.password,host = 'localhost', port = '5432')
    cur = conn.cursor()
    
    song_table = create_song_table()
    sql_upload(song_table,'songs')


    #unique_artists = grab_unique_artists()
    #unique_artists.remove(('NA',))
    
    #artist_data = get_artist_stats(unique_artists,False)
    #artist_data.to_csv('artist_data.csv')
    #engine = create_engine(sql_credentials.engine_path)
    #artist_data.to_sql('artists',engine)
    
    #unique_songs = grab_unique_values(song_columns)
    #unique_songs.remove(('NA',))
    #audio_features = get_audio_features(unique_songs,True)
    #sql_upload(audio_features,'audio_features')

