# Overview 

The Billboard Hot 100 is the music industry standard for ranking songs by popularity. It has been around since 1958 and continues to release the week's most popular songs. Music has undergone many transformations since 1958 and my goal of this study is to highlight attributes of music that have changed overtime. 

# Data Pipeline 

The data for this analysis came from two sources. 

First, I scraped the Billboard Hot 100 website using Python's beautiful soup to extract each Hot 100 chart from  ***** to . I then uploaded the scraped data to a mongo database for easy access/retreival. Note: To focus in on the most popular songs I decided to keep only the top 10 songs for each week in my analysis. 

The second source of data was the music streaming platform Spotify. Using the songs and artists I scraped from the Hot 100 charts I was able to extract a unique song ID and artist ID features via Spotify's API through the Python module spotipy. I uploaded then uploaded this data to a SQL database. Using the unique song and artist IDs compiled in the previous step I created a SQL table for song attributes and artist attributes. This helped streamline my analysis by allowing my to look at attributes I was currently interested in via the use of SQL joins.

# Database Structure 

# Genre Analysis 

The first feature I decided to look at was genre and how it changed throught the anlysis period. Note that I used artist genre as a proxy for song genre based on the assumption that tracks in the top 10 were most likely of the same genre as the artists' listed genre. The below histogram shows the most popular genres over the anlysis period. 


![](/images/genre_histogram.png)

I decided to focus my analysis on the most popular genres. To understand how the popularity of genres changed I plotted the number of songs each genre had in the top 10 for each year. The plot clearly shows that the popularity of the genres has changed since the inception of the Hot 100. 

![](/images/top_genres_over_time.png)

![](/images/top_genres_over_time_2.png)