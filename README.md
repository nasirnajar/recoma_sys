# Frame Finder

Frame Finder is a content-based movie recommender built with Python and Streamlit. Choose a movie to see six recommendations ranked by similarity to the selected film.

It uses the TMDB 5000 Movies and Credits CSV files. Recommendation features include genres, keywords, the top three cast members, director, and overview. No TMDB API key or pre-generated model file is required.

## Features

- Search and select from the movie collection.
- View the selected film's genres, release year, rating, and overview.
- Browse six recommendations with genres, synopsis, TMDB rating, and similarity score.
- Use a dark Streamlit theme configured in `.streamlit/config.toml`.

## How Recommendations Work

1. The movie and credits tables are joined using movie ID.
2. Genre and keyword JSON are parsed, the first three cast members are selected, and the director is extracted from crew data.
3. Those fields and the movie overview are combined into one text document per movie.
4. Scikit-learn's `CountVectorizer` removes English stop words and converts the documents to sparse vectors with up to 10,000 terms.
5. Cosine similarity ranks other movies against the selected movie. The selected movie itself is excluded.

The displayed match percentage is cosine similarity formatted as a percentage; it is not a probability or audience rating. Feature vectors are built locally at app startup, so no model artifact needs to be committed.

## Dataset

Download the TMDB 5000 Movie Dataset from [Kaggle](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata) and place both CSVs in the project root, alongside `app.py`:

| File | Purpose | Columns used |
| --- | --- | --- |
| `tmdb_5000_movies.csv` | Movie details | `id`, `title`, `genres`, `keywords`, `overview`, `release_date`, `vote_average` |
| `tmdb_5000_credits.csv` | Cast and crew details | `movie_id`, `cast`, `crew` |

Credits are joined using `movies.id = credits.movie_id`. Duplicate credit IDs and movie titles are removed before features are built. Missing overview text is treated as empty text. Follow the dataset source's terms for attribution and redistribution.

## Project Structure

```text
.
|-- app.py                     # Streamlit interface
|-- recommender.py             # Data loading and cosine-similarity logic
|-- requirements.txt           # Python dependencies
|-- README.md
|-- .gitignore
|-- .streamlit/
|   `-- config.toml            # Dark theme settings
|-- tmdb_5000_movies.csv       # Movie metadata
`-- tmdb_5000_credits.csv      # Cast and crew metadata
```

## Run Locally

Use Python 3.10 or newer. Open a terminal in the project directory and create a virtual environment, install dependencies, and launch Streamlit.

### macOS or Linux

```bash
cd path/to/Recommendation_sys
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
streamlit run app.py
```

### Windows PowerShell

```powershell
cd path\to\Recommendation_sys
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
streamlit run app.py
```

Streamlit prints the local URL in the terminal, usually <http://localhost:8501>. Stop the server with `Ctrl+C`. If port 8501 is already in use, run `streamlit run app.py --server.port 8502` instead.

## Deploy to Streamlit Community Cloud

### 1. Push the project to GitHub

Create a GitHub repository and push the app, dependency file, Streamlit config, and both datasets. Keep the CSV files at the repository root because the app loads them relative to `recommender.py`. Do not commit the `.venv` directory; it is excluded by `.gitignore`.

From the project directory, stage the relevant files and push them:

```bash
git add app.py recommender.py requirements.txt README.md .gitignore .streamlit/config.toml
git add tmdb_5000_movies.csv tmdb_5000_credits.csv
git commit -m "Add Frame Finder movie recommender"
git push
```

The credits CSV is approximately 40 MB, so make sure your Git host accepts the dataset file. If your host rejects a file because of size or policy, keep the data in an approved external store and update the data-loading code to retrieve it there.

### 2. Create and deploy the Streamlit app

1. Sign in to [Streamlit Community Cloud](https://share.streamlit.io/) with a GitHub account that can access the repository.
2. Choose **Create app**, then select the repository and branch.
3. Set the app's main file path to `app.py`.
4. Deploy. Community Cloud installs the packages from `requirements.txt` and builds the app.

When deployment completes, Community Cloud provides a shareable app URL. No API keys or Streamlit secrets are needed. To publish updates, push commits to the branch connected to the app; Community Cloud will rebuild it.

## Troubleshooting

- **CSV file not found:** Confirm both CSVs are in the repository root and the filenames match the names listed above.
- **A Python package is missing:** Activate the project's virtual environment and run `python -m pip install -r requirements.txt`.
- **Port 8501 is busy:** Start Streamlit with `streamlit run app.py --server.port 8502`.
- **Community Cloud deployment fails:** Check the deploy logs, confirm both data files were pushed, and verify that every required package appears in `requirements.txt`.

<!-- //link recomasys-eeeakznykboirreeisfvm6 -->
