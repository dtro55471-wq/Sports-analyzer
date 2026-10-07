import numpy as np
import pandas as pd
import scipy.stats as stats
import streamlit as st

st.set_page_config(
    page_title="Analyseur Sportif Global", page_icon="⚽", layout="centered"
)

st.title("⚽ Analyseur Sportif Global par Championnat")
st.markdown(
    "Sélectionnez d'abord le championnat, puis le match pour l'analyser"
    " instantanément."
)

# هيكل البطولات والدوريات الكبرى
leagues = {
    "UEFA Champions League": {
        "Real Madrid vs Manchester City": {
            "home": "Real Madrid",
            "away": "Manchester City",
            "h_xg": 1.85,
            "a_xg": 1.75,
            "h_c": 5.5,
            "a_c": 5.0,
        },
        "Bayern Munich vs Paris Saint-Germain": {
            "home": "Bayern Munich",
            "away": "Paris Saint-Germain",
            "h_xg": 1.95,
            "a_xg": 1.60,
            "h_c": 6.0,
            "a_c": 4.5,
        },
        "Barcelone vs Inter Milan": {
            "home": "Barcelone",
            "away": "Inter Milan",
            "h_xg": 1.70,
            "a_xg": 1.40,
            "h_c": 5.5,
            "a_c": 4.0,
        },
    },
    "Premier League (Angleterre)": {
        "Arsenal vs Liverpool": {
            "home": "Arsenal",
            "away": "Liverpool",
            "h_xg": 1.75,
            "a_xg": 1.65,
            "h_c": 6.0,
            "a_c": 5.5,
        },
        "Manchester United vs Chelsea": {
            "home": "Manchester United",
            "away": "Chelsea",
            "h_xg": 1.55,
            "a_xg": 1.50,
            "h_c": 5.0,
            "a_c": 5.0,
        },
        "Tottenham vs Newcastle United": {
            "home": "Tottenham",
            "away": "Newcastle United",
            "h_xg": 1.60,
            "a_xg": 1.55,
            "h_c": 6.5,
            "a_c": 5.0,
        },
    },
    "La Liga (Espagne)": {
        "Real Madrid vs Barcelone": {
            "home": "Real Madrid",
            "away": "Barcelone",
            "h_xg": 1.90,
            "a_xg": 1.80,
            "h_c": 6.0,
            "a_c": 5.0,
        },
        "Atletico Madrid vs Athletic Bilbao": {
            "home": "Atletico Madrid",
            "away": "Athletic Bilbao",
            "h_xg": 1.65,
            "a_xg": 1.10,
            "h_c": 5.0,
            "a_c": 4.0,
        },
    },
    "Serie A (Italie)": {
        "Juventus vs AC Milan": {
            "home": "Juventus",
            "away": "AC Milan",
            "h_xg": 1.45,
            "a_xg": 1.35,
            "h_c": 4.5,
            "a_c": 4.5,
        },
        "Napoli vs AS Roma": {
            "home": "Napoli",
            "away": "AS Roma",
            "h_xg": 1.75,
            "a_xg": 1.20,
            "h_c": 5.5,
            "a_c": 4.0,
        },
    },
    "Bundesliga (Allemagne)": {
        "Borussia Dortmund vs RB Leipzig": {
            "home": "Borussia Dortmund",
            "away": "RB Leipzig",
            "h_xg": 1.80,
            "a_xg": 1.50,
            "h_c": 6.0,
            "a_c": 5.0,
        },
    },
    "Ligue des Champions de la CAF": {
        "Al Ahly vs Espérance de Tunis": {
            "home": "Al Ahly",
            "away": "Espérance de Tunis",
            "h_xg": 1.60,
            "a_xg": 1.15,
            "h_c": 5.0,
            "a_c": 4.0,
        },
        "Wydad AC vs Mamelodi Sundowns": {
            "home": "Wydad AC",
            "away": "Mamelodi Sundowns",
            "h_xg": 1.50,
            "a_xg": 1.30,
            "h_c": 4.5,
            "a_c": 4.5,
        },
    },
    "🛠️ Personnalisé (Saisie manuelle)": {
        "Match personnalisé": {
            "home": "Domicile",
            "away": "Extérieur",
            "h_xg": 1.50,
            "a_xg": 1.20,
            "h_c": 5.0,
            "a_c": 4.0,
        }
    },
}

st.sidebar.header("🌍 Navigation par Championnat")
selected_league = st.sidebar.selectbox(
    "Sélectionnez un championnat :", list(leagues.keys())
)

match_dict = leagues[selected_league]
selected_match = st.sidebar.selectbox(
    "Sélectionnez un match :", list(match_dict.keys())
)

match_info = match_dict[selected_match]

if (
    "current_match" not in st.session_state
    or st.session_state.current_match != selected_match
):
  st.session_state.current_match = selected_match
  st.session_state.home_team = match_info["home"]
  st.session_state.away_team = match_info["away"]
  st.session_state.home_xg = match_info["h_xg"]
  st.session_state.away_xg = match_info["a_xg"]
  st.session_state.home_corners = match_info["h_c"]
  st.session_state.away_corners = match_info["a_c"]

st.divider()

col1, col2 = st.columns(2)
with col1:
  home_team = st.text_input("Équipe à domicile", key="home_team")
  home_xg = st.number_input(
      "xG Domicile", min_value=0.1, max_value=5.0, step=0.05, key="home_xg"
  )
with col2:
  away_team = st.text_input("Équipe à l'extérieur", key="away_team")
  away_xg = st.number_input(
      "xG Extérieur", min_value=0.1, max_value=5.0, step=0.05, key="away_xg"
  )
