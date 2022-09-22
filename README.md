# TV Series and Song Matcher: Project Overview
I love watching tv series, and I give extra attention the song choices for the tv series I watch. Also, I love listening music, and sometimes I think that for a particular song could be a perfect match for particular TV Series. Therefore, I wonder if Machine Learning can decide that. In order to achieve this, I followed the steps:</br>
* Scraped all of the songs that is played on the TV Series from tunefind.com by using Selenium.
* I extracted the audio features of the songs from Spotify Developer API.
* I tried different classification algorithms to get the best performance. (Since this is a classification task) 
* Lastly, I productionarize the project with the Flask web framework and built some simple UI.
## Web Scraping
### Selenium tunefind.com
I wanted to make classification for the TV series Sons of Anarchy, Silicon Valley, and Vikings. Therefore, I scraped for these 3 TV Series from tunefind.com with the help of Selenium. Unfortunately, small portion of the songs were not included on the spotify so I couldn't ge to use them. 
### Spotify API
For every single song, requests has been made to the url https://api.spotify.com/v1/audio-features/{track-id}. Track ids are obtained from tunefind.com. Spotify api returns audio features for the particular track. Attributes are listed as below:
* danceability -> how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. 
* energy -> represents a perceptual measure of intensity and activity
* key -> The key the track is in. Integers map to pitches using standard Pitch Class notation. E.g. 0 = C, 1 = C♯/D♭, 2 = D, and so on. If no key was detected, the value is -1.
* loudness -> the overall loudness of a track in decibels (dB) (-60 to 0)
* mode -> Mode indicates the modality (major or minor) of a track, the type of scale from which its melodic content is derived. Major is represented by 1 and minor is 0.
* speechiness -> Speechiness detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value.
* acousticness -> whether the track is acoustic
* instrumentalness -> predicts whether a track contains no vocals
* liveness -> higher liveness values represent an increased probability that the track was performed live.
* valence -> A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track.
* tempo -> The overall estimated tempo of a track in beats per minute (BPM)

For more detailed information you can visit https://developer.spotify.com/documentation/web-api/reference/#/operations/get-several-audio-features.
## Data Cleaning
There were some outliers on the dataset. I removed the outliers by every attribute so the song characteristics would be clean. The outliers could be detected from the below figure.
![alt text for screen readers](images/outliers.gif "Outliers")
Radar graph and bar graph are generated by Plotly as averages of the attributes. 
## Exploratory Data Analysis
<p float="left">
  <img align="top" src="/images/radar-graph.gif"/ width="500">
  <img align="top" src="/images/bar-graph.gif" width="300">
</p>

![alt text for screen readers](images/correlation.png "Feature Correlation")
* Vikings Song Characteristics
  * It is highly instrumental.
  * Less louder, less energetic, and less danceable songs.
  * Also, it is less tempo.
  * It is very accoustic.
  * More negative vibes conveyed by tracks. (angry, sad, unhappy etc.)
* Silicon Valley Song Characteristics
  * It is highly energetic and danceable songs.
  * More on the tempo.
  * More louder songs.
  * It is not accoustic.
  * More positive vibes conveyed by tracks. (happy, cheerful etc.)
* Sons of Anarchy Song Characteristics
  * It is energetic and somewhat danceable.
  * More on the tempo.
  * Louder songs.
  * It is somewhat accoustic
  * Both positive and negative vibes conveyed by tracks.
## Model Building
Data is over sampled in order to avoid the imbalance. Over sample is used on only training data, because we do not want to effect the test data. Different classification algorithms like; logistic regression, support vector machines, decsion trees, random forest, ada boost, gradient boost etc., are trained and tested. Also, stacking approch is applied. ROC scores on the test data could be examined from the below figure, for the most successfull models.
![alt text for screen readers](images/roc-score-comparison.png "ROC Scores")
The most succesful model is stacked algorithm with a little difference. Stacked algorithm structure and some of the performance metrics are as below:
* Test Accuracy: 0.907
* Test Precision: 0.905
* Test Recall: 0.915
* Test F1 Score: 0.906

![alt text for screen readers](images/model_structure.png "Stacked Algorithm Structure")
## Application
I built a simple web app with the Flask Framework. It can be shown on the below figure. I always thought that Ace of Spades by Motorhead could be a perfect match for Sons of Anarchy, and hopefully machine learning algorithm thinks the same way with the 98% probability score.

![alt text for screen readers](images/application.gif "Application")
