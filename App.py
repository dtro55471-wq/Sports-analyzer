import numpy as np
import pandas as pd
import scipy.stats as stats
import streamlit as st

st.set_page_config(
    page_title="Analyseur Pro par Cotes & xG", page_icon="⚽", layout="centered"
)

st.title("⚽ Analyseur Sportif Pro (Par Noms & Cotes)")
st.markdown(
    "Entrez les noms des clubs et les cotes du bookmaker pour obtenir une"
    " analyse mathématique de haute précision."
)

st.sidebar.header("⚙️ Saisie des Clubs & Cotes")
home_team = st.sidebar.text_input("Équipe Domicile", "Real Madrid")
away_team = st.sidebar.text_input("Équipe Extérieur", "Manchester City")

st.sidebar.markdown("---")
st.sidebar.subheader("📊 Cotes du Bookmaker (1X2)")
cote_home = st.sidebar.number_input(
    "Cote 1 (Domicile)",
    min_value=1.01,
    max_value=50.0,
    value=2.10,
    step=0.05,
    format="%.2f",
)
cote_draw = st.sidebar.number_input(
    "Cote X (Nul)",
    min_value=1.01,
    max_value=50.0,
    value=3.40,
    step=0.05,
    format="%.2f",
)
cote_away = st.sidebar.number_input(
    "Cote 2 (Extérieur)",
    min_value=1.01,
    max_value=50.0,
    value=3.20,
    step=0.05,
    format="%.2f",
)

st.sidebar.markdown("---")
st.sidebar.subheader("🚩 Paramètres Avancés")
avg_
