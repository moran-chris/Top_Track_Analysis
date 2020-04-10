# Overview 

The Billboard Hot 100 is the music industry standard for ranking songs by popularity. It has been around since 1958 and continues to release the week's most popular songs today. Billboard assigns its rankings based off of sales, number of radio plays and streams. Music has changed quite a bit since 1958 and the goal of this study is to understand how the different attributes of music, from genre to danceability, have changed in popular songs over time. 

# Data Pipeline 

The data for this analysis was compiled from two sources. 

First, I scraped the Billboard Hot 100 website to extract every weekly Hot 100 chart from  August 1958 - March 2020. This was accomplished using Python's Beautiful Soup. I then uploaded the scraped data to MongoDB for easy access and retrieval. This also allowed me to limit the requests I was making to Billboard's servers. To focus in on the most popular songs I decided to keep only the top 10 songs for each week in my analysis. 

The second source of data was the music streaming platform Spotify. Spotify assigns a unique ID to each song (track) and artist called a URI.  Using the songs' titles and artists' names I scraped from the Hot 100 charts, I was able to extract the track and artist URIs via Spotify's API. Once I had the track and artist URIs I was able to query Spotify for more interesting information such as songs' audio features (loudness, acousticness, etc.) and artist genre. Using the data I collected from Billboard and Spotify I created a SQL table according to the schema shown below. This helped me streamline my analysis by allowing me to dial in on specific attributes of interest and eliminated the need to continuallly make requests from Billboard and Spotify's servers. 

![](/images/flow_relationship.png)


# Genre Analysis 

The first feature I examined was genre, and how it changed throught the anlysis period. Note that I used artist genre as a proxy for song genre based on the assumption that tracks in the top 10 were most likely of the same genre as the artists' listed genre. The below histogram shows the most popular genres over the analysis period. 


![](/images/genre_histogram.png)
## Genre Descriptions
![](/images/genre_descriptions.png)

I decided to focus my analysis on six of the most popular genres. To understand how the popularity of genres evolved, I plotted the number of songs each genre had in the top 10 for each year. The plot shows that the popular genres have changed dramatically since the inception of the Hot 100. The genres indicated in shades of blue have declined in popularity while the genres indicated in shades of red have increased in popularity. 

![](/images/top_genres_over_time.png)
One interesting aspect of this change is the timeframe in which the switch occurs. There appears to be a drastic shift in genre popularity during the period of 1983 - 1994 (shaded region in the graph below). Throughout this period genres associated with bands and multiple instruments decline while genres associated with studio-produced sounds and solo artists skyrocket in popularity. One possible explanation for this is the advancement of technology in the music industry, which made recording music more accessible and experimental and led to more electronic styles.
![](/images/top_genres_over_time_2.png)

# Audio Feature Analysis 
Spotify assigns scores to several different features of each track based on certain song characterists. These features are intended to describe a song's mood, tempo, and scale, among other things. To gain a further understanding of these features and how they relate to music genre, I averaged the feature value for each year and plotted it over time.
## Danceability
The below chart shows the feature danceability plotted with the genre dance pop. Spotify describes danceability as how suitable a song is for dancing, 1 being the most suitable and 0 being the least suitable. Unsurprisingly, danceability and dance pop appear to be highly correlated. A more surprising insight is that dance pop's popularity appears to be driving the presence of danceability in other popular songs that aren't in the dance pop genre. This could suggest that features of popular genres influence features of other popular music.  
![](/images/dancepop_v_dance.png)

## Valence & Speechiness
Audio features also give us insight into the popularity of sub-genres and the characteristics that define genres. For example, the audio feature "valence" rates how happy and positive a song is, versus how sad or negative it is. There is a steep drop in average valence during the 90's, right when grunge music was becoming more mainstreem. 
The feature "speechiness" detects the presence of spoken words in songs. A dramatic increase in speechiness occurs in the early 2000s when Eminem, Nelly and other rap artist frequently appeared on the Hot 100. 

![](/images/valance_speechiness.png)

# Conclusion 

Music genre is an ever-changing landscape and genre popularity is just as variable. Over the past seven decades we have seen drastically different genres peak, including folk rock, rap, and dance pop. As genres become more popular their key features start to influence other genres and create new ones. As we look forward we can be almost certain that the popular genres will further evolve. 
I can't wait to hear what's next! 

