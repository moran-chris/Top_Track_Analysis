# Overview 

The Billboard Hot 100 is the music industry standard for ranking songs by popularity. It has been around since 1958 and continues to release the week's most popular songs. Music has undergone many transformations since 1958 and the goal of this study is to highlight attributes of music that have changed overtime. 

# Data Pipeline 

The data for this analysis came from two sources. 

First, I scraped the Billboard Hot 100 website using Python's beautiful soup to extract every weekly Hot 100 chart from  August 1958 - March 2020. I then uploaded the scraped data to a mongo database for easy access/retreival. Note: To focus in on the most popular songs I decided to keep only the top 10 songs for each week in my analysis. 

The second source of data was the music streaming platform Spotify. Using the songs and artists I scraped from the Hot 100 charts I was able to extract a unique song ID and artist ID features via Spotify's API through the Python module spotipy. I  then uploaded this data to a SQL database. Using the unique song and artist IDs compiled in the previous step I created a SQL table for song attributes and artist attributes by once again scraping Spotify's API, this time using Spotify's unique identifiers. This helped streamline my analysis by allowing me to look at attributes I was currently interested in via the use of SQL joins.

![](/images/flow_relationship.png)

# Database Structure 

# Genre Analysis 

The first feature I decided to look at was genre and how it changed throught the anlysis period. Note that I used artist genre as a proxy for song genre based on the assumption that tracks in the top 10 were most likely of the same genre as the artists' listed genre. The below histogram shows the most popular genres over the anlysis period. 


![](/images/genre_histogram.png)

I decided to focus my analysis on the most popular genres. To understand how the popularity of genres changed I plotted the number of songs each genre had in the top 10 for each year. The plot clearly shows that the popularity of genres has changed since the inception of the Hot 100. Specifically, the genres indicated by shades of blue have declined in popularity while the genres indicated by shades of red have increased in popularity. 

![](/images/top_genres_over_time.png)
An interesting aspect of this change is the timeframe the switch occurs. There appears to be a drastic shift in genre taste during the period of 1983 - 1994 (shaded region below). Throughout this period genres associated with bands and multiple instruments decline while genres associated with studio produced sounds skyrocket in popularity.  
![](/images/top_genres_over_time_2.png)

# Audio Feature Analysis 

![](/images/valance_speechiness.png)