import json

import streamlit as st

from recommender import load_recommender, recommend


st.set_page_config(page_title="Frame Finder", layout="wide")
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');
    :root { --ink: #f0eee7; --muted: #a6aaa0; --paper: #171a17; --accent: #e07a5f; --line: #394139; }
    .stApp { background-color: var(--paper); background-image: repeating-linear-gradient(135deg, transparent 0 22px, rgba(240,238,231,.018) 22px 23px); color: var(--ink); }
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
    h1, h2, h3 { color: var(--ink); font-family: 'Playfair Display', Georgia, serif; }
    h1 { font-size: 2.8rem !important; margin-bottom: 0 !important; }
    .eyebrow { color: var(--accent); font-size: .72rem; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; }
    .lede { color: var(--muted); font-size: 1rem; margin-top: .25rem; }
    [data-testid="stMetric"] { background: rgba(34,39,34,.82); border: 1px solid var(--line); border-radius: 6px; padding: .8rem 1rem; }
    [data-testid="stMetricLabel"] { color: var(--muted); }
    [data-testid="stVerticalBlockBorderWrapper"] { background: rgba(34,39,34,.88); border-color: var(--line); border-radius: 6px; }
    [data-testid="stSelectbox"] label { color: var(--muted); font-weight: 600; }
    hr { border-color: var(--line); }
    </style>
    """,
    unsafe_allow_html=True,
)

movies, vectors = load_recommender()
titles = sorted(movies["title"].dropna().unique().tolist())

st.markdown('<p class="eyebrow">A little less scrolling, a little more cinema</p>', unsafe_allow_html=True)
st.title("Frame Finder")
st.markdown('<p class="lede">Pick a film. Find what to watch next.</p>', unsafe_allow_html=True)

left, right = st.columns([3, 1])
with left:
    selected_title = st.selectbox("Choose a movie", titles, index=titles.index("Avatar") if "Avatar" in titles else 0)
with right:
    st.metric("Films in the collection", f"{len(movies):,}")

selected = movies.loc[movies["title"] == selected_title].iloc[0]
try:
    selected_genres = ", ".join(item["name"] for item in json.loads(selected["genres"]))
except (json.JSONDecodeError, TypeError):
    selected_genres = ""

st.caption(f"{selected_genres}  ·  {str(selected.get('release_date', ''))[:4]}  ·  TMDB rating {selected.get('vote_average', 0):.1f}")
st.write(selected.get("overview") or "No synopsis is available for this film.")
st.divider()
st.subheader("Films with a similar pulse")

recommendations = recommend(selected_title, movies, vectors)
for row_start in range(0, len(recommendations), 3):
    columns = st.columns(3)
    for column, (_, movie) in zip(columns, recommendations.iloc[row_start:row_start + 3].iterrows()):
        with column:
            with st.container(border=True):
                st.markdown(f"### {movie['title']}")
                try:
                    genres = ", ".join(item["name"] for item in json.loads(movie["genres"]))
                except (json.JSONDecodeError, TypeError):
                    genres = ""
                st.caption(genres)
                overview = str(movie.get("overview") or "No synopsis available.")
                st.write(overview if len(overview) <= 220 else overview[:217].rsplit(" ", 1)[0] + "...")
                rating = movie.get("vote_average", 0)
                st.caption(f"TMDB {rating:.1f}  ·  {movie['similarity']:.0%} match")