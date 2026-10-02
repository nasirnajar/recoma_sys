import json
from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


DATA_DIR = Path(__file__).resolve().parent


def _names(value):
    if not isinstance(value, str) or not value:
        return []
    try:
        entries = json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return []
    return [entry["name"] for entry in entries if isinstance(entry, dict) and entry.get("name")]


def load_recommender():
    movies = pd.read_csv(DATA_DIR / "tmdb_5000_movies.csv")
    credits = pd.read_csv(DATA_DIR / "tmdb_5000_credits.csv")
    credits = credits.drop_duplicates("movie_id")
    movies = movies.merge(credits[["movie_id", "cast", "crew"]], left_on="id", right_on="movie_id", how="left")
    movies = movies.drop_duplicates("title").reset_index(drop=True)

    movies["genres_text"] = movies["genres"].map(_names)
    movies["keywords_text"] = movies["keywords"].map(_names)
    movies["cast_text"] = movies["cast"].map(lambda value: _names(value)[:3])
    movies["director_text"] = movies["crew"].map(
        lambda value: [
            member["name"]
            for member in json.loads(value) if isinstance(member, dict) and member.get("job") == "Director"
        ] if isinstance(value, str) and value else []
    )

    features = ["genres_text", "keywords_text", "cast_text", "director_text"]
    for feature in features:
        movies[feature] = movies[feature].map(lambda values: " ".join(name.replace(" ", "") for name in values))
    movies["overview_text"] = movies["overview"].fillna("").astype(str)
    movies["tags"] = movies[features + ["overview_text"]].agg(" ".join, axis=1).str.lower()

    vectorizer = CountVectorizer(stop_words="english", max_features=10000)
    vectors = vectorizer.fit_transform(movies["tags"])
    return movies, vectors


def recommend(title, movies, vectors, limit=6):
    matches = movies.index[movies["title"] == title]
    if len(matches) == 0:
        return movies.iloc[0:0].copy()

    movie_index = matches[0]
    scores = cosine_similarity(vectors[movie_index], vectors).ravel()
    scores[movie_index] = -1
    ranked_indices = scores.argsort()[::-1][:limit]
    return movies.iloc[ranked_indices].assign(similarity=scores[ranked_indices])