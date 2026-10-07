import numpy as np
import pandas as pd
import scipy.stats as stats
import streamlit as st

st.set_page_config(
    page_title="Analyseur Sportif Pro", page_icon="⚽", layout="centered"
)

st.title("⚽ Analyseur Sportif Professionnel & Avancé")
st.markdown(
    "Analysez n'importe quel match dans le monde avec des statistiques"
    " approfondies (xG, Corners, Scores Exacts et Clean Sheets)."
)

# قائمة واسعة وشاملة لأبرز الدوريات العالمية مع إمكانية التعديل الكامل
leagues = {
    "🏆 Match Personnalisé / En Direct (Saisie Libre)": {
        "Saisir les équipes et xG du match du jour": {
            "home": "Équipe Domicile",
            "away": "Équipe Extérieur",
            "h_xg": 1.60,
            "a_xg": 1.30,
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
    "🇬🇧 Premier League (Angleterre)": {
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
            "h_xg": 2.10,
            "a_xg": 1.30,
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
    "🇪🇸 La Liga (Espagne)": {
        "Real Madrid vs Barcelone": {
            "home": "Real Madrid",
            "away": "Barcelone",
            "h_xg": 1.90,
            "a_xg": 1.80,
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
        "Raja CA vs FAR Rabat": {
            "home": "Raja CA",
            "away": "FAR Rabat",
            "h_xg": 1.55,
            "a_xg": 1.35,
            "h_c": 5.0,
            "a_c": 4.5,
        },
    },
}

st.sidebar.header("🌍 Sélection de la Compétition")
selected_league = st.sidebar.selectbox(
    "Choisissez le championnat :", list(leagues.keys())
)

match_dict = leagues[selected_league]
selected_match = st.sidebar.selectbox(
    "Choisissez le match :", list(match_dict.keys())
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

st.subheader("⚙️ Paramètres & Statistiques du Match")
col1, col2 = st.columns(2)
with col1:
  home_team = st.text_input("Équipe à Domicile", key="home_team")
  home_xg = st.number_input(
      "xG Domicile (Buts attendus)",
      min_value=0.1,
      max_value=6.0,
      step=0.05,
      key="home_xg",
  )
with col2:
  away_team = st.text_input("Équipe à l'Extérieur", key="away_team")
  away_xg = st.number_input(
      "xG Extérieur (Buts attendus)",
      min_value=0.1,
      max_value=6.0,
      step=0.05,
      key="away_xg",
  )

st.subheader("🚩 Analyse des Corners")
col_c1, col_c2 = st.columns(2)
with col_c1:
  home_corners = st.number_input(
      "Corners Domicile",
      min_value=0.5,
      max_value=15.0,
      step=0.5,
      key="home_corners",
 
