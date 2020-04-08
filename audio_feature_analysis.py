import psycopg2
import sql_credentials
import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np

plt.style.use('ggplot')


class AudioFeatures():
    
    def __init__(self,query,conn):
        self.query = query 
        self.conn = conn 
        self.data = pd.read_sql_query(self.query,self.conn)
        self.grouped_data = None 

    def add_year_column(self):
        df = self.data 
        df['year'] = df['date'].apply(lambda x: int(x[:4]))
        self.data = df 

    def group(self):
        df = self.data  
        df_grouped = df.groupby('year', as_index = False).mean()
        self.grouped_data = df_grouped

    def plot(self,column,ax):
        df = self.grouped_data 
        ax.plot(df['year'],df[column])









if __name__ == '__main__':


    conn = psycopg2.connect(database = 'billboard',user = sql_credentials.user, password = sql_credentials.password,host = 'localhost', port = '5432')
    
    feature_list = ['danceability','energy','key','loudness','mode','speechiness',
                    'acousticness','instrumentalness','liveness','valence','tempo',
                    'time_signature']


    fig,ax = plt.subplots(4,3,figsize = (40,40))
    ax_list = ax.flatten()
    for index,feature in enumerate(feature_list):
        query = f''' 
                SELECT s.unique_id,s.date,s.song_id,af.{feature}
                FROM songs s
                INNER JOIN audio_features af
                ON s.song_id = af.uri
                '''
        data = AudioFeatures(query,conn)
        data.add_year_column()
        data.group()
        data.plot(feature,ax_list[index])
        ax_list[index].set_title(feature)

    plt.show()
    duration_query = ''' 
            SELECT s.unique_id,s.date,s.song_id,af.duration_ms
            FROM songs s
            INNER JOIN audio_features af
            ON s.song_id = af.uri
            '''
    duartion_analysis = AudioFeatures(duration_query,conn)
    duartion_analysis.add_year_column()
    duartion_analysis.group()
    df = duartion_analysis.grouped_data 
    df['minutes'] = df['duration_ms'].apply(lambda x: x/60000)

    
    
    fig,ax = plt.subplots(1,figsize = (8,8))
    ax.plot(df['year'],df['minutes'])
    fig.autofmt_xdate()
    plt.show()

    dance_query = ''' 
            SELECT s.unique_id,s.date,s.song_id,af.danceability
            FROM songs s
            INNER JOIN audio_features af
            ON s.song_id = af.uri
            '''

    fig,ax = plt.subplots(1,figsize = (8,8))
    dance_analysis = AudioFeatures(dance_query,conn)
    dance_analysis.add_year_column()
    dance_analysis.group()
    dance_analysis.plot('danceability',ax)
    