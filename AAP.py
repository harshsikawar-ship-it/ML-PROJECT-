# ---------------- IMPORTS ----------------
import streamlit as st
import pandas as pd
import os
import requests
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---------------- API CONFIG ----------------
API_KEY = "04b5baa75ed84e5ba810ffe7511fc414"
IMG_URL = "https://image.tmdb.org/t/p/w500"

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")
st.title("🎬 Movie Recommender System")

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    file_path = "C:\\Users\\Harsh Singh\\Downloads\\ML PROJECT\\final_project\\tmdb_movies_data.csv"
    
    if not os.path.exists(file_path):
        st.error(f"File not found: {file_path}")
        return None
    
    df = pd.read_csv(file_path)
    return df

movies = load_data()

# ---------------- PROCESS DATA ----------------
@st.cache_data
def process_data(movies):

    movies = movies[['original_title','overview','genres','keywords']]
    movies.dropna(inplace=True)

    movies['tags'] = (
        movies['overview'].astype(str) + " " +
        movies['genres'].astype(str) + " " +
        movies['keywords'].astype(str)
    )

    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(movies['tags']).toarray()

    similarity = cosine_similarity(vectors)

    return movies, similarity

movies, similarity = process_data(movies)

# ---------------- TMDB FUNCTIONS ----------------
def fetch_movie_data(title):
    url = "https://api.themoviedb.org/3/search/movie"
    params = {
        "api_key": API_KEY,
        "query": title
    }
    data = requests.get(url, params=params).json()
    
    if data['results']:
        movie = data['results'][0]
        return {
            "poster": IMG_URL + movie['poster_path'] if movie['poster_path'] else None,
            "rating": movie['vote_average'],
            "overview": movie['overview']
        }
    return None

# ---------------- RECOMMEND ----------------
def recommend(movie):
    index = movies[movies['original_title'] == movie].index[0]
    distances = similarity[index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    results = []
    for i in movies_list:
        title = movies.iloc[i[0]].original_title
        results.append(title)

    return results

# ---------------- UI ----------------
selected_movie = st.selectbox(
    "🎥 Select a movie",
    movies['original_title'].values
)

# 🔍 Show selected movie details
movie_data = fetch_movie_data(selected_movie)

if movie_data:
    st.subheader("🎯 Selected Movie")
    col1, col2 = st.columns([1,2])

    with col1:
        if movie_data["poster"]:
            st.image(movie_data["poster"],)

    with col2:
        st.write(f"⭐ Rating: {movie_data['rating']}")
        st.write(f"📝 {movie_data['overview'][:200]}...")

# 🚀 Recommendations
if st.button("🚀 Recommend"):
    names = recommend(selected_movie)

    st.subheader("🔥 Top Recommendations")

    cols = st.columns(5)

    for i, name in enumerate(names):
        data = fetch_movie_data(name)

        with cols[i]:
            if data and data["poster"]:
                st.image(data["poster"])
            st.caption(name)

            if data:
                st.write(f"⭐ {data['rating']}")