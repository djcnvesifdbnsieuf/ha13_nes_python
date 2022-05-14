# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import streamlit as st
#import numpy as np
import pandas as pd
import plotly.graph_objects as go
#import geopandas as gpd
#import matplotlib.pyplot as plt
#import folium

@st.cache
def load_data(a):
    x = pd.read_csv(a)
    return x

@st.cache
def create_movie(a):
    movie_df = imdb_df[imdb_df['Title'] == a]
    return movie_df



if __name__ == '__main__':
    imdb_df = load_data("imdbTop250.csv")

st.write('Hi, here you can explore movie perfomance in IMBD250 rating')

selected_movies = st.multiselect("Select Movie", imdb_df['Title'].unique())
st.write("Selected Movies:", selected_movies)

movie_fig = go.Figure()
for i in selected_movies:
    movie_df = create_movie(i)
    movie_fig.add_trace(go.Scatter(x = movie_df['IMDByear'], y = movie_df['Ranking'], name = i))
movie_fig.update_layout(title = 'Movie perfomance year by year',
                        xaxis_title="Year",
                        yaxis_title="IMDB Ranking",
                        legend_orientation="h",
                        legend=dict(y=-.15),
                        margin=dict(l=0, r=0, t=50, b=0),
                        height = 600
                        )
### FROM: (https://translated.turbopages.org/proxy_u/en-ru.ru.52e25f3a-627fb18c-74f4b159-74722d776562/https/stackoverflow.com/questions/59100115/plotly-how-to-reverse-axes)
movie_fig['layout']['yaxis']['autorange'] = "reversed"
### END FROM
st.write(movie_fig)

### Here I started the second vizualization

st.write('unfortunatelly I failed with other pics, Altair is the worsts libriary')

st.write('my code you can fing here: https://github.com/djcnvesifdbnsieuf/ha13_nes_python')

#happy_df = load_data('Happiness.csv')
#world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

#world_sorted = world.sort_values( by = ['name'])
#дальше я вручную подобрал значение из happy_df и добавил их в world_sorted

Ladder_score = [2.5669,
4.8827,
5.1951,
0,
0,
5.9747,
4.6768,
7.2228,
7.2942,
5.1648,
0,
4.8328,
5.5399,
6.8635,
0,
5.2160,
0,
5.7475,
5.6741,
3.4789,
6.3756,
0,
5.1015,
4.7687,
3.7753,
4.8484,
5.0849,
7.2321,
3.4759,
4.4227,
6.2285,
5.1239,
6.1634,
5.1944,
7.1214,
5.5047,
0,
0,
6.1590,
6.9109,
0,
7.6456,
0,
5.6892,
5.9252,
4.1514,
6.3483,
0,
0,
6.0218,
0,
4.1862,
0,
0,
7.8087,
0,
6.6638,
4.8293,
4.7506,
4.6726,
7.0758,
5.1480,
5.5150,
6.3989,
4.9493,
3.7208,
0,
0,
5.9532,
5.5104,
7.5045,
3.5733,
5.2856,
4.6724,
4.7848,
7.0937,
7.1286,
6.3874,
5.2333,
5.8708,
4.6334,
6.0579,
4.5830,
6.3252,
6.1021,
5.5415,
4.8886,
5.9500,
4.7715,
3.6528,
4.5579,
5.4888,
6.2155,
7.2375,
5.1598,
4.1656,
3.5380,
5.3843,
5.1976,
6.7728,
6.1013,
5.6075,
5.4562,5.5461,5.0948,4.6236,4.3080,7.4489,4.5528,7.2996,6.1371,4.9096,0,4.7241,5.5355,7.4880,5.6933,0,6.3048,0,5.6921,5.7968,6.1960,0,6.1863,5.9109,6.1237,5.5460,3.3123,0,0,6.4065,4.9808,5.7782,4.3081,3.9264,6.3771,6.2806,6.3634,5.8724,2.8166,0,0,0,6.4009,4.3270,7.3535,7.5599,0,0,5.5557,3.4762,0,5.9988,4.1872,6.1919,4.3922,
0,5.1318,
5.1191,4.4320,
4.5607,6.7908,
7.1645,6.9396,
6.4401,6.2576,5.0532,
5.3535,
3.5274,
3.7594,
3.2992,
3.5274,
3.7594,3.2992,0,0,]

#world_sorted['happy_score'] = Ladder_score

#f, ax = plt.subplots(1,1,figsize=(1,1))
#world_sorted.plot(column = 'happy_score', ax=ax)




#final_world = pd.join(world_sorted, Ladder_score_df)


