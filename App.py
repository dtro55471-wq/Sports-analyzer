import numpy as np
import pandas as pd
import scipy.stats as stats
import streamlit as st

st.set_page_config(
    page_title="Analyseur Sportif Pro", page_icon="⚽", layout="centered"
)

st.title("⚽ Analyseur Sportif Pro & Avancé")
st.markdown(
    "Sélectionnez un championnat et un match pour l'analyser instantanément."
)

leagues = {
    "🏆 Match Personnalisé (Saisie Libre)": {
        "Saisir les équipes et xG": {
            "home": "Domicile",
            "away": "Extérieur",
            "h_xg": 1.6,
            "a_xg": 1.3,
            "h_c": 5.5,
            "a_c": 4.5,
        }
    },
    "🇪🇺 UEFA Champions League": {
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
            "a_xg": 1.6,
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
    "🇬🇧 Premier League": {
        "Arsenal vs Liverpool": {
            "home": "Arsenal",
            "away": "Liverpool",
            "h_xg": 1.75,
            "a_xg": 1.65,
            "h_c": 6.0,
            "a_c": 5.5,
        },
        "Manchester City vs Chelsea": {
            "home": "Manchester City",
            "away": "Chelsea",
            "h_xg": 2.1,
            "a_xg": 1.3,
            "h_c": 6.5,
            "a_c": 4.0,
        },
        "Manchester United vs Tottenham": {
            "home": "Manchester United",
            "away": "Tottenham",
            "h_xg": 1.60,
            "a_xg": 1.55,
            "h_c": 5.5,
            "a_c": 5.0,
        },
    },
    "🇪🇸 La Liga": {
        "Real Madrid vs Barcelone": {
            "home": "Real Madrid",
            "away": "Barcelone",
            "h_xg": 1.9,
            "a_xg": 1.8,
            "h_c": 6.0,
            "a_c": 5.0,
        },
        "Atletico Madrid vs Real Sociedad": {
            "home": "Atletico Madrid",
            "away": "Real Sociedad",
            "h_xg": 1.65,
            "a_xg": 1.10,
            "h_c": 5.0,
            "a_c": 4.0,
        },
    },
    "🇮🇹 Serie A": {
        "Juventus vs AC Milan": {
            "home": "Juventus",
            "away": "AC Milan",
            "h_xg": 1.45,
            "a_xg": 1.35,
            "h_c": 4.5,
            "a_c": 4.5,
        },
        "Inter Milan vs Lazio": {
            "home": "Inter Milan",
            "away": "Lazio",
            "h_xg": 1.90,
            "a_xg": 1.30,
            "h_c": 6.0,
            "a_c": 4.2,
        },
    },
    "🇩🇪 Bundesliga": {
        "Borussia Dortmund vs RB Leipzig": {
            "home": "Borussia Dortmund",
            "away": "RB Leipzig",
            "h_xg": 1.80,
            "a_xg": 1.50,
            "h_c": 6.0,
            "a_c": 5.0,
        },
        "Bayern Munich vs Bayer Leverkusen": {
            "home": "Bayern Munich",
            "away": "Bayer Leverkusen",
            "h_xg": 2.10,
            "a_xg": 1.80,
            "h_c": 6.5,
            "a_c": 5.5,
        },
    },
    "🇫🇷 Ligue 1": {
        "Paris Saint-Germain vs Marseille": {
            "home": "Paris Saint-Germain",
            "away": "Marseille",
            "h_xg": 2.10,
            "a_xg": 1.20,
            "h_c": 6.5,
            "a_c": 4.0,
        },
        "AS Monaco vs Lyon": {
            "home": "AS Monaco",
            "away": "Lyon",
            "h_xg": 1.75,
            "a_xg": 1.55,
            "h_c": 5.5,
            "a_c": 5.0,
        },
    },
    "🌍 Compétitions Africaines & Arabes": {
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
        "Al Hilal vs Al Nassr": {
            "home": "Al Hilal",
            "away": "Al Nassr",
            "h_xg": 2.00,
            "a_xg": 1.90,
            "h_c": 6.0,
            "a_c": 5.8,
        },
    },
}

st.sidebar.header("🌍 Navigation")
sel_league = st.sidebar.selectbox("Championnat:", list(leagues.keys()))
match_dict = leagues[sel_league]
sel_match = st.sidebar.selectbox("Match:", list(match_dict.keys()))

info = match_dict[sel_match]

if "cur" not in st.session_state or st.session_state.cur != sel_match:
  st.session_state.cur = sel_match
  st.session_state.h_team 
