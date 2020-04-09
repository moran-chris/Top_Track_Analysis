import psycopg2
import sql_credentials
import pandas as pd
import matplotlib 
import matplotlib.pyplot as plt 
import numpy as np
from audio_feature_analysis import AudioFeatures 
plt.style.use('ggplot')


# Pulls data from passed SQL query
def pull_data(query,conn):
    return pd.read_sql_query(query,conn)

#Takes df with column genre_list and data type list and returns df with each unique 
# list item as a new row with all previous attributes held constant 
def genre__analysis(df):
    df['genre_list'] = df['genres'].apply(lambda x: x.split('|'))
    df = df.explode('genre_list')
    df['year'] = df['date'].apply(lambda x:int(x[:4]))
    df = df.loc[df['year'] != 1958]
    df= df.loc[df['year'] != 2020]
    return df 

# Takes df with column genre_list and returns df where each unique value in genre_list 
# becomes a column with True or False values (1,0)
def get_genre_dummies(df):
    return pd.get_dummies(df, columns = ['genre_list']).groupby('year',as_index = False).sum()

#Plots the top n genres by count 
def plot_top_n_genres(df,n):
    genre_count = df[['unique_id','genre_list']].groupby('genre_list', as_index = False).count().sort_values(by = 'unique_id', ascending = False)
    top_n = genre_count.head(n)
    fig,ax = plt.subplots(1,figsize= (7,6.5))
    ax.bar(top_n['genre_list'],top_n['unique_id'])
    ax.set_xticklabels(labels = top_n['genre_list'],rotation = 20,horizontalalignment = 'right')
    ax.set_title('Number of Songs in Top 10 by Genre')
    plt.savefig('images/genre_histogram.png')
    plt.show()


#plots the passed column list over time 
#Each column is its own line plot 
def plot_genres_over_time(df,columns,ax,color = [None]):
    if color[0]:
        pass 
    else:
        color = color * len(columns)
    for index, genre in enumerate(columns):
        ax.plot(df['year'],df[genre],color = color[index],label = genre.replace('genre_list_',''))
    
    ax.legend(fontsize = 18,loc = 2)
    ax.axvspan(xmin =  1986, xmax = 1996, color = 'lightgray', alpha = .85 )
    ax.set_title('Top Genres Over Time',fontsize = 38)
    
if __name__ == '__main__':
    #Instantiate SQL connection
    conn = psycopg2.connect(database = 'billboard',user = sql_credentials.user, password = sql_credentials.password,host = 'localhost', port = '5432')
    
    #Grab data 
    query = ''' 
            SELECT s.unique_id,s.date,s.artist_id,a.name as artist, a.genres
            FROM songs s
            INNER JOIN artists a
            ON s.artist_id = a.uri
            '''
    source_df = pull_data(query,conn)
    genre_df = genre__analysis(source_df)
    genre_df_dummies = get_genre_dummies(genre_df)

    #Histogram 
    plot_top_n_genres(genre_df,10)
    
    #Line plot over time 
    matplotlib.rc('xtick', labelsize = 20)
    matplotlib.rc('ytick', labelsize = 20)
    
    genre_list = ['genre_list_folk rock','genre_list_adult standards',
                'genre_list_mellow gold','genre_list_pop rap',
                'genre_list_dance pop','genre_list_pop']
    
    fig,ax = plt.subplots(1,figsize= (20,12))
    
    plot_genres_over_time(genre_df_dummies,genre_list,ax,color = ['teal','deepskyblue','mediumblue','#FF0000','#8B0000','#FA8072'])
    fig.autofmt_xdate()
    plt.savefig('images/top_genres_over_time_2.png')
    plt.show()

    #Danceability and dance pop ploted on different y axis
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
    ax.plot(dance_analysis.grouped_data['year'],dance_analysis.grouped_data['danceability'],label = 'danceability',color = 'red')
    ax.legend()

    ax2 = ax.twinx()
    ax2.plot(genre_df_dummies['year'],genre_df_dummies['genre_list_dance pop'],color = 'blue',label = 'dance pop')

    plt.show()