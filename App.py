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
        "Arsenal vs Real Madrid": {
            "home": "Arsenal",
            "away": "Real Madrid",
            "h_xg": 1.65,
            "a_xg": 1.70,
            "h_c": 5.8,
            "a_c": 5.2,
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
        "Aston Villa vs Newcastle United": {
            "home": "Aston Villa",
            "away": "Newcastle United",
            "h_xg": 1.55,
            "a_xg": 1.45,
            "h_c": 5.0,
            "a_c": 4.8,
        },
        "Brighton vs West Ham": {
            "home": "Brighton",
            "away": "West Ham",
            "h_xg": 1.65,
            "a_xg": 1.35,
            "h_c": 6.0,
            "a_c": 4.2,
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
        "Athletic Bilbao vs Villarreal": {
            "home": "Athletic Bilbao",
            "away": "Villarreal",
            "h_xg": 1.60,
            "a_xg": 1.30,
            "h_c": 5.5,
            "a_c": 4.5,
        },
        "Real Betis vs Valencia": {
            "home": "Real Betis",
            "away": "Valencia",
            "h_xg": 1.50,
            "a_xg": 1.20,
            "h_c": 4.8,
            "a_c": 4.2,
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
        "Napoli vs AS Roma": {
            "home": "Napoli",
            "away": "AS Roma",
            "h_xg": 1.75,
            "a_xg": 1.20,
            "h_c": 5.5,
            "a_c": 4.0,
        },
        "Inter Milan vs Lazio": {
            "home": "Inter Milan",
            "away": "Lazio",
            "h_xg": 1.90,
            "a_xg": 1.30,
            "h_c": 6.0,
            "a_c": 4.2,
        },
        "Atalanta vs Fiorentina": {
            "home": "Atalanta",
            "away": "Fiorentina",
            "h_xg": 1.80,
            "a_xg": 1.40,
            "h_c": 5.8,
            "a_c": 4.6,
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
        "VfB Stuttgart vs Eintracht Frankfurt": {
  
