# Frame Finder

A content-based movie recommender built from the TMDB 5000 movies and credits datasets. It combines genres, keywords, the top three cast members, director, and overview text, then ranks films using cosine similarity.

## Run locally

```bash
python3 -m pip install -r requirements.txt
streamlit run app.py
```

Keep `tmdb_5000_movies.csv` and `tmdb_5000_credits.csv` in this directory. The app builds its feature vectors locally on startup; no API key or pre-generated model files are needed.