# ---------------- IMPORTS ----------------
import streamlit as st
import pandas as pd
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from difflib import get_close_matches
import matplotlib.pyplot as plt

# ---------------- CONFIG ----------------
API_KEY = "04b5baa75ed84e5ba810ffe7511fc414"
IMG_URL = "https://image.tmdb.org/t/p/w500"
st.set_page_config(layout="wide")

# ---------------- SESSION ----------------
st.session_state.setdefault("page", "home")
st.session_state.setdefault("selected_movie", None)
st.session_state.setdefault("watchlist", [])

# ---------------- UI ----------------
st.markdown("""
<style>
body {background-color: #0e1117; color: white;}
h1, h2, h3 {color: #E50914;}
.stButton>button {background-color:#E50914;color:white;}
</style>
""", unsafe_allow_html=True)

st.title("🎬 Netflix AI Recommender")

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    df = pd.read_csv("C:\\Users\\Harsh Singh\\Downloads\\ML PROJECT\\final_project\\tmdb_movies_data.csv")
    df = df[['original_title','overview','genres','keywords']]
    df.dropna(inplace=True)
    return df

movies = load_data()

# ---------------- FEATURES ----------------
movies['tags'] = (
    movies['overview'] + " " +
    movies['genres'] + " " +
    movies['keywords']
)

tfidf = TfidfVectorizer(max_features=5000, stop_words='english')
vectors = tfidf.fit_transform(movies['tags'])
similarity = cosine_similarity(vectors)

# ---------------- API ----------------
def fetch_movie(title):
    url = "https://api.themoviedb.org/3/search/movie"
    data = requests.get(url, params={"api_key": API_KEY, "query": title}).json()

    if data['results']:
        m = data['results'][0]
        return {
            "title": m['title'],
            "poster": IMG_URL + m['poster_path'] if m['poster_path'] else None,
            "rating": m['vote_average'],
            "overview": m['overview'],
            "release": m['release_date']
        }
    return None

def get_trending():
    url = "https://api.themoviedb.org/3/trending/movie/day"
    return requests.get(url, params={"api_key": API_KEY}).json()['results']

def get_top_rated():
    url = "https://api.themoviedb.org/3/movie/top_rated"
    return requests.get(url, params={"api_key": API_KEY}).json()['results']

# ---------------- RECOMMENDER ----------------
def recommend(movie):
    titles = movies['original_title'].tolist()
    match = get_close_matches(movie, titles, n=1, cutoff=0.6)

    if not match:
        return []

    movie = match[0]

    idx = movies[movies['original_title'] == movie].index[0]
    distances = similarity[idx]

    movie_list = sorted(list(enumerate(distances)),
                        reverse=True,
                        key=lambda x: x[1])[1:10]

    return [movies.iloc[i[0]].original_title for i in movie_list]

# ---------------- SIDEBAR ----------------
menu = st.sidebar.radio("Menu", ["Home", "Watchlist", "Analytics"])

# ================= HOME =================
if menu == "Home" and st.session_state.page == "home":

    query = st.text_input("🔍 Search Movie")

    if query:
        st.session_state.selected_movie = query
        st.session_state.page = "details"
        st.rerun()

    genre = st.selectbox("🎭 Genre Filter", ["All", "Action", "Comedy", "Drama"])

    if genre != "All":
        filtered = movies[movies['genres'].str.contains(genre, case=False)]

        st.subheader("🎬 Filtered Movies")
        cols = st.columns(5)

        for i, name in enumerate(filtered['original_title'].head(10)):
            data = fetch_movie(name)

            with cols[i % 5]:
                if data and data["poster"]:
                    st.image(data["poster"])
                st.caption(name)

                if st.button("🎬 View", key=f"genre_{i}_{name}"):
                    st.session_state.selected_movie = name
                    st.session_state.page = "details"
                    st.rerun()

    # 🔥 TRENDING
    st.subheader("🔥 Trending")
    trending = get_trending()
    cols = st.columns(5)

    for i, movie in enumerate(trending[:5]):
        with cols[i]:
            if movie['poster_path']:
                st.image(IMG_URL + movie['poster_path'])
            st.caption(movie['title'])

            if st.button("View", key=f"trend_{i}"):
                st.session_state.selected_movie = movie['title']
                st.session_state.page = "details"
                st.rerun()

    # ⭐ TOP RATED
    st.subheader("⭐ Top Rated")
    top = get_top_rated()
    cols = st.columns(5)

    for i, movie in enumerate(top[:5]):
        with cols[i]:
            if movie['poster_path']:
                st.image(IMG_URL + movie['poster_path'])
            st.caption(movie['title'])

            if st.button("View", key=f"top_{i}"):
                st.session_state.selected_movie = movie['title']
                st.session_state.page = "details"
                st.rerun()

# ================= DETAILS =================
if st.session_state.page == "details":

    movie = st.session_state.selected_movie
    data = fetch_movie(movie)

    if data:
        col1, col2 = st.columns([1,2])

        with col1:
            if data["poster"]:
                st.image(data["poster"])

        with col2:
            st.header(data["title"])
            st.write(f"⭐ {data['rating']}")
            st.write(f"📅 {data['release']}")
            st.write(data['overview'])

            if st.button("➕ Add to Watchlist", key=f"watch_{data['title']}"):
                if data["title"] not in st.session_state.watchlist:
                    st.session_state.watchlist.append(data["title"])
                    st.success("Added!")
                else:
                    st.warning("Already added")

        # 🔥 SIMILAR MOVIES
        st.subheader("🔥 Similar Movies")
        recs = recommend(movie)

        if not recs:
            st.info("Showing trending instead")
            recs_api = get_trending()
            cols = st.columns(5)

            for i, m in enumerate(recs_api[:5]):
                with cols[i]:
                    if m['poster_path']:
                        st.image(IMG_URL + m['poster_path'])
                    st.caption(m['title'])
        else:
            cols = st.columns(5)
            for i, name in enumerate(recs[:5]):
                rec_data = fetch_movie(name)

                with cols[i]:
                    if rec_data and rec_data["poster"]:
                        st.image(rec_data["poster"])
                    st.caption(name)

                    if st.button("View", key=f"rec_{i}_{name}"):
                        st.session_state.selected_movie = name
                        st.rerun()

    if st.button("⬅ Back"):
        st.session_state.page = "home"
        st.rerun()

# ================= WATCHLIST =================
if menu == "Watchlist":
    st.subheader("📌 Watchlist")

    if not st.session_state.watchlist:
        st.write("No movies added yet")

    for movie in st.session_state.watchlist:
        data = fetch_movie(movie)

        col1, col2 = st.columns([1,2])
        with col1:
            if data and data["poster"]:
                st.image(data["poster"])

        with col2:
            st.write(movie)

# ================= ANALYTICS =================
if menu == "Analytics":
    st.subheader("📊 Movie Analytics Dashboard")

    # 🎯 Genre Distribution
    st.write("### 🎭 Genre Distribution")

    genre_counts = movies['genres'].str.split().explode().value_counts().head(10)

    plt.figure()
    genre_counts.plot(kind='bar')
    st.pyplot(plt)

    # 🎯 Top Keywords
    st.write("### 🔑 Top Keywords")

    keyword_counts = movies['keywords'].str.split().explode().value_counts().head(10)

    plt.figure()
    keyword_counts.plot(kind='bar')
    st.pyplot(plt)

    # 🎯 Dataset Overview
    st.write("### 📈 Dataset Info")
    st.write(f"Total Movies: {len(movies)}")
    st.write(f"Unique Genres: {movies['genres'].nunique()}")