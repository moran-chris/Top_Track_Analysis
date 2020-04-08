import psycopg2
import sql_credentials
import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np

plt.style.use('ggplot')


def pull_data(query,conn):
    return pd.read_sql_query(query,conn)

def genre__analysis(df):
    df['genre_list'] = df['genres'].apply(lambda x: x.split('|'))
    df = df.explode('genre_list')
    df['year'] = df['date'].apply(lambda x:int(x[:4]))
    df = df.loc[df['year'] != 1958]
    df= df.loc[df['year'] != 2020]
    return df 

def plot_top_n_genres(df,n):
    genre_count = df[['unique_id','genre_list']].groupby('genre_list', as_index = False).count().sort_values(by = 'unique_id', ascending = False)
    top_n = genre_count.head(n)
    fig,ax = plt.subplots(1,figsize= (8,8))
    ax.bar(top_n['genre_list'],top_n['unique_id'])
    plt.show()
def get_genre_dummies(df):
    return pd.get_dummies(df, columns = ['genre_list']).groupby('year',as_index = False).sum()
    
def plot_top_n_genres_over_time(df,columns,ax,color = [None]):
    #df_dummies = pd.get_dummies(df, columns = ['genre_list']).groupby('year',as_index = False).sum()
    #df = df[columns]
    if color[0]:
        pass 
    else:
        color = color * len(columns)

    for index, genre in enumerate(columns):
        ax.plot(df['year'],df[genre],color = color[index],label = genre.replace('genre_list_',''))
    #ax.set_xticklabels(labels = df['year'].apply(lambda x: int(x)),rotation = 45)
    #ax.set_xticklabels(list(np.arange(min(1958), max(2020)+1, 1.0)))
    ax.legend()

if __name__ == '__main__':

    conn = psycopg2.connect(database = 'billboard',user = sql_credentials.user, password = sql_credentials.password,host = 'localhost', port = '5432')
    
    query = ''' 
            SELECT s.unique_id,s.date,s.artist_id,a.name as artist, a.genres
            FROM songs s
            INNER JOIN artists a
            ON s.artist_id = a.uri
            '''

    
    source_df = pull_data(query,conn)
    genre_df = genre__analysis(source_df)
    genre_df_dummies = get_genre_dummies(genre_df)
    #plot_top_n_genres_over_time(genre_df,7)
    #plot_top_n_genres(genre_df,15)
    genre_list = ['genre_list_folk rock','genre_list_adult standards',
                'genre_list_mellow gold','genre_list_pop rap',
                'genre_list_dance pop','genre_list_pop']
    fig,ax = plt.subplots(1,figsize= (20,8))
    plot_top_n_genres_over_time(genre_df_dummies,genre_list,ax)
    fig.autofmt_xdate()
    plt.show()
    
    fig,ax = plt.subplots(1,figsize= (20,8))
    
    plot_top_n_genres_over_time(genre_df_dummies,genre_list,ax,color = ['#0000CD','#00008B','#0000FF','#FF0000','#8B0000','#FA8072'])
    fig.autofmt_xdate()

    plt.show()

    #fig,ax = plt.subplots(2,figsize=(20,10))
    #plot_top_n_genres_over_time(genre_df_dummies.loc[genre_df_dummies['year'].apply(lambda x: int(x)) <= 1985],genre_list,ax[0])
    #plot_top_n_genres_over_time(genre_df_dummies.loc[genre_df_dummies['year'].apply(lambda x: int(x)) >= 1985],genre_list,ax[1])