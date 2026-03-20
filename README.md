# ML-PROJECT-movie recommendation system
🎬 Netflix-Style Movie Recommendation System

### Using Machine Learning (TF-IDF + Cosine Similarity)

---

## 📌 Abstract

With the rapid growth of digital streaming platforms, users often face difficulty in finding relevant content due to the vast number of available movies. This project presents a Netflix-style movie recommendation system that suggests similar movies based on content features such as genres, keywords, and movie descriptions. The system uses TF-IDF vectorization and cosine similarity to generate recommendations and integrates TMDB API to fetch real-time movie details like posters, ratings, and trending data. The application is built using Streamlit with an interactive user interface.

---

## 📖 1. Introduction

### 1.1 Background

Online streaming platforms like Netflix and Amazon Prime rely heavily on recommendation systems to enhance user experience and engagement. These systems help users discover relevant content efficiently.

### 1.2 Objective

The objective of this project is to build a content-based movie recommendation system that:

* Suggests similar movies based on user selection
* Displays movie details such as posters, ratings, and overview
* Provides a Netflix-like user interface

### 1.3 Problem Statement

Users struggle to find relevant movies due to the overwhelming amount of available content. This system aims to solve this problem by recommending movies based on similarity in content.

---

## 📊 2. Dataset Description

### 2.1 Data Source

* TMDB (The Movie Database)
* Kaggle dataset

### 2.2 Dataset Size

* Approximately 5000 movies
* Multiple features per movie

### 2.3 Features Used

* `original_title` – Movie name
* `overview` – Movie description
* `genres` – Category of movie
* `keywords` – Important tags

### 2.4 Data Preprocessing

* Removed missing values
* Selected relevant columns
* Combined features into a single "tags" column
* Converted text into lowercase
* Removed stopwords

---

## ⚙️ 3. Methodology

### 3.1 Feature Engineering

All relevant textual data (overview, genres, keywords) were combined into a single column called **tags**.

### 3.2 Vectorization

TF-IDF (Term Frequency - Inverse Document Frequency) was used to convert text into numerical vectors.

### 3.3 Similarity Calculation

Cosine similarity was applied to calculate similarity between movies.

### 3.4 Recommendation Logic

* Find selected movie
* Compute similarity scores
* Sort and return top similar movies

---

## 🤖 4. System Architecture

### Components:

1. Dataset Processing (Pandas)
2. Feature Engineering (Text processing)
3. TF-IDF Vectorization
4. Cosine Similarity Model
5. TMDB API Integration
6. Streamlit UI

---

## 💻 5. Implementation

### Tools & Technologies:

* Python
* Pandas, NumPy
* Scikit-learn
* Streamlit
* TMDB API

### Features:

* Search movies
* Display posters and ratings
* Show similar recommendations
* Trending and top-rated movies
* Watchlist system
* Analytics dashboard

---

## 📈 6. Model Evaluation

Unlike classification models, recommendation systems are evaluated based on:

* Relevance of recommendations
* Similarity scores
* User satisfaction

### Result:

The system successfully generates meaningful recommendations based on content similarity.

---

## 📊 7. Analytics Dashboard

The project includes a dashboard with:

* Genre distribution
* Keyword frequency
* Dataset statistics

This helps in understanding movie trends and data insights.

---

## ⚠️ 8. Limitations

* Does not use user behavior (no collaborative filtering)
* Dependent on dataset quality
* Cannot recommend new movies without data (cold-start problem)

---

## 🚀 9. Future Enhancements

* Add collaborative filtering
* Use deep learning models
* Implement user login system
* Add movie trailers
* Deploy on cloud

---

## 🎯 10. Conclusion

This project demonstrates a complete movie recommendation system using machine learning techniques. It successfully combines content-based filtering with real-time API integration and provides a user-friendly Netflix-like interface. The system enhances content discovery and can be extended for real-world applications.

---

## 📚 References

* TMDB API Documentation
* Scikit-learn Documentation
* Kaggle Dataset
* Streamlit Documentation

---

---
