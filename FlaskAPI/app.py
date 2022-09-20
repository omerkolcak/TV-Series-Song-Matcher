from flask import Flask, render_template, url_for, request, flash
import requests
import json
import pickle
import numpy as np
import plotly.graph_objects as go
from dotenv import load_dotenv
import os
import pandas as pd

app = Flask(__name__)

load_dotenv() # load the environment variables

@app.route("/")
def hello_spotify():
    return render_template("index.html")


def load_models():
    file_name = "models/stacked_clf.p"
    with open(file_name, 'rb') as pickled:
        data = pickle.load(pickled)
        model = data['model']
    return model

def get_class_mappings():
    classes = []

    with open("models/class_mappings.txt",'r') as file:
        line = file.readline()

        while line:
            classes.append(line.strip())

            line = file.readline()
    
    return classes


def make_prediction(song_attributes):
    model = load_models()
    class_mappings = get_class_mappings()

    probs = model.predict_proba(song_attributes)
    idx = np.argmax(probs)

    series_name = class_mappings[idx]
    probability = probs[0][idx]

    return series_name, probability, str(idx)

def generate_radar_graph(data,series_name,track_name):

    attribute_names = ['acousticness','danceability','energy','instrumentalness','liveness','speechiness','valence']
    attribute_values = [data['acousticness'], data['danceability'], data['energy'], data['instrumentalness'], data['liveness'], data['speechiness'], data['valence']]

    fig = go.Figure(layout=go.Layout(title='Audio Features'))

    series_audio_fetaures = pd.read_csv("models/audio_features.csv")
    df = series_audio_fetaures[series_audio_fetaures.series_name == series_name]


    fig.add_trace(go.Scatterpolar(
        r=attribute_values,
        theta=attribute_names,
        fill='toself',
        name=track_name
    ))

    fig.add_trace(go.Scatterpolar(
        r=df['value'],
        theta=df['audio_feature'],
        fill='toself',
        name=series_name
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
            visible=True
            ),
        ),
        showlegend=True,
        legend=dict(y=0.5)
    )

    # in order to render to the html
    graph = fig.to_html(full_html=False, default_height=400, default_width=450, include_plotlyjs="cdn")

    return graph


@app.route("/get_track", methods = ['POST','GET'])
def get_track():

    ACCESS_TOKEN = os.environ["ACCESS_TOKEN"] # get ACCESS_TOKEN for spotify api from .env file
    endpoint = "https://api.spotify.com/v1/audio-features/"
    
    track_id = request.args['track_id']

    headers = {"Authorization" : f"Bearer  {ACCESS_TOKEN}"}
    audio_features_request_url = endpoint + track_id

    response = requests.get(audio_features_request_url, headers=headers)

    if response.status_code == 200:
        audio_features_data = response.json()
        
        attributes = [audio_features_data['danceability'], audio_features_data['energy'],audio_features_data['loudness'], audio_features_data['speechiness'], audio_features_data['instrumentalness'], audio_features_data['liveness'], audio_features_data['valence'], audio_features_data['tempo'], audio_features_data['acousticness']]
        attributes = np.array(attributes).reshape(1,-1)

        series_name, prob, idx = make_prediction(attributes)

        # if probability is less than 0.65, dont match with the series
        if prob < 0.65:
            error_message = f"There is no suitable tv series for the song with the track id : {track_id}"
        
            return render_template("index.html", error = error_message)

        # get song information
        track_info_url = f"https://api.spotify.com/v1/tracks/{track_id}"

        track_info = requests.get(track_info_url, headers=headers).json()

        artist_name = track_info['album']['artists'][0]['name']
        image = track_info['album']['images'][0]
        track_name = track_info['name']

        track_info = {
            'artist_name' : artist_name,
            'track_name' : track_name,
            'album_image_src' : image['url'],
            'series_image_src' : f"../static/images/{idx}.png",
            'additional_audio_features' : {
                'loudness' : audio_features_data['loudness'],
                'tempo' : audio_features_data['tempo']
            }
        }

        radar_graph = generate_radar_graph(audio_features_data,series_name,track_name)

        return render_template("song_dashboard.html",graph=radar_graph,track_info=track_info,prediction={'series_name' : series_name, 'probability' : prob})
    else:
        error_message = f"There is no song with the track id : {track_id}"
        
        return render_template("index.html", error = error_message)


if __name__ == "main":
    app.run(debug=True)
