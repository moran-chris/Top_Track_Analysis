import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pymongo import MongoClient
import datetime 
import pandas as pd 
from time import sleep
import Spotify_Credentials
import sql_credentials
from sqlalchemy import create_engine

client = MongoClient('localhost',27017)
db = client['billboard_3']
table = db['hot_100']

client_credentials_manager = SpotifyClientCredentials(Spotify_Credentials.Client_ID,Spotify_Credentials.Secret_ID)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
engine = create_engine(sql_credentials.engine_path)



# '''Grabs and cleans data from Mongo and collects song and artist attributes via 
#   Spotify's API
    
#    Date = week of hot 100 chart 
#    N = number of top songs to grab from hot 100 chart '''

class HotWeek:


    def __init__(self,date,n):
        self.date = date
        self.n = n
        self.data = self._get_data()
        self.songs = self._get_songs(self.n)
        self.artists = self._get_artist(self.n)
        self.spotify_ids = self._get_spotify_id(self.n)
        self.row = self._to_dict(self.n)

    # Grabs a specific Hot 100 chart based on date 
    def _get_data(self):
        return table.find({'date':self.date}).limit(1)[0]

    # Cleans the song data from self. data and outputs a list of songs names included in that weeks chart 
    def _get_songs(self,n):
        raw_song_list = self.data['songs']
        clean_song_list = []
        for song in raw_song_list[:n]:
            start = song.find('primary">')
            end = song.find('</span')
            clean_song = song[start + len('primary">'):end]
            clean_song_list.append(clean_song)
        return clean_song_list
    #Cleans artist data from self.data and outputs list of artist names in that weeks chart
    def _get_artist(self,n):
        raw_artist_list = self.data['artist']
        clean_artist_list = []
        for artist in raw_artist_list[:n]:
            start = artist.find('secondary">')
            end = artist.find('</span')
            clean_artist = artist[start + len('secondary">'):end]
            if '&amp' in clean_artist.lower():
                clean_artist = clean_artist[:clean_artist.lower().find('&amp')-1]
            if 'featuring' in clean_artist.lower():
                clean_artist = clean_artist[:clean_artist.lower().find('featuring')-1]
            clean_artist_list.append(clean_artist)
        return clean_artist_list
    
    # '''Queries Spotify's API and returns Spotify's unique identifier, urn, 
    #   for the passed combination of song and artist 
    #   '''
    def _get_spotify_id(self,n):
        spotify_ids = []
        for item in range(n):
            try:
                song = self.songs[item]
                artist = self.artists[item]
                query = sp.search(q = f'artist:{artist} track:{song}', type = 'track',limit=1)
                song_uri = query['tracks']['items'][0]['uri']
                artist_uri = query['tracks']['items'][0]['artists'][0]['uri']
                spotify_ids.append((song_uri,artist_uri))
            except:
                spotify_ids.append(('NA','NA'))
        return spotify_ids
    
    def _to_dict(self,n):
        row = {'date': self.date}
        for index in range(n):
            row['song_'+str(index+1)] = [self.songs[index]]
            row['artist_'+str(index+1)] = [self.artists[index]]
            row['song_id'+str(index+1)] = [self.spotify_ids[index][0]]
            row['artist_id'+str(index+1)] = [self.spotify_ids[index][1]]
        return row

# ''' Creates a data frame with each row being a date and columns of 
#       song_1, song_id1, artist_1, artist_id1 ....artist_idn '''
def to_dataframe(start_date,end_date,n):
    cols = ['date']
    for index in range(n):
        cols.append('song_'+str(index+1))
        cols.append('artist_'+str(index+1))
        cols.append('song_id'+str(index+1))
        cols.append('artist_id'+str(index+1))
    df = pd.DataFrame(columns = cols)
    count = 0
        
    while start_date != end_date:
        chart = HotWeek(str(start_date.date()),10)
        new_row = pd.DataFrame.from_dict(chart.row)
        df = pd.concat([df,new_row])
        start_date = start_date + datetime.timedelta(days=7)
        sleep(1)
    return df


if __name__ == '__main__':

    start_date = datetime.datetime.strptime('1958/08/23','%Y/%m/%d')
    end_date = datetime.datetime.strptime('2020/03/28','%Y/%m/%d')

    data = to_dataframe(start_date,end_date,10)

    # Uploads dataframe to SQL
    data.to_sql('hot_charts',engine)

    



    

