import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    api_key = '8265bd1679663a7ea12ac168da84d2e8'
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US')
    data = response.json()
    return 'https://image.tmdb.org/t/p/w500/'+data['poster_path']
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies_posters.append(fetch_poster(movie_id))
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies, recommended_movies_posters

movies_dict = pickle.load(open('./movie-recommender-system/movie_dict.pkl','rb'))
import bz2file as bz2
def decompress_pickle(file):
    data = bz2.BZ2File(file, 'rb')
    data = pickle.load(data)
    return data
similarity = decompress_pickle('similarity.pbz2')
movies = pd.DataFrame(movies_dict)
st.title('Movie Recommender System')


selected_movie_name = st.selectbox(
    'Movies',
    movies['title'].values
)
if st.button('Recommend'):
    names,posters = recommend(selected_movie_name)
    col1, col2,col3,col4,col5 = st.columns(5)
    cols = [col1,col2,col3,col4,col5]
    for i in range(len(names)):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
