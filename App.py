import numpy as np
import pandas as pd
import scipy.stats as stats
import streamlit as st

st.set_page_config(
    page_title="Analyseur Sportif Global", page_icon="⚽", layout="centered"
)

st.title("⚽ Analyseur Sportif Global des Matchs")
st.markdown(
    "Sélectionnez un match dans la barre latérale pour l'analyser"
    " instantanément."
)

# Liste des matchs globaux en français
global_matches = {
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
    "Arsenal vs Liverpool": {
        "home": "Arsenal",
        "away": "Liverpool",
        "h_xg": 1.75,
        "a_xg": 1.65,
        "h_c": 6.0,
        "a_c": 5.5,
    },
    "Barcelone vs Atletico Madrid": {
        "home": "Barcelone",
        "away": "Atletico Madrid",
        "h_xg": 1.70,
        "a_xg": 1.40,
        "h_c": 5.5,
        "a_c": 4.0,
    },
    "Al Ahly vs Espérance de Tunis": {
        "home": "Al Ahly",
        "away": "Espérance de Tunis",
        "h_xg": 1.60,
        "a_xg": 1.15,
        "h_c": 5.0,
        "a_c": 4.0,
    },
    "🛠️ Match personnalisé (Saisie manuelle)": {
        "home": "Domicile",
        "away": "Extérieur",
        "h_xg": 1.50,
        "a_xg": 1.20,
        "h_c": 5.0,
        "a_c": 4.0,
    },
}

st.sidebar.header("🌍 Liste des Matchs")
selected_match = st.sidebar.selectbox(
    "Sélectionnez un match :", list(global_matches.keys())
)

match_info = global_matches[selected_match]

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

st.subheader("🚩 Corners attendus")
col_c1, col_c2 = st.columns(2)
with col_c1:
  home_corners = st.number_input(
      "Corners Domicile",
      min_value=0.5,
      max_value=15.0,
      step=0.5,
      key="home_corners",
  )
with col_c2:
  away_corners = st.number_input(
      "Corners Extérieur",
      min_value=0.5,
      max_value=15.0,
      step=0.5,
      key="away_corners",
  )

# Calculs Poisson
max_goals = 7
home_probs = [stats.poisson.pmf(i, home_xg) for i in range(max_goals)]
away_probs = [stats.poisson.pmf(j, away_xg) for j in range(max_goals)]

matrix = np.outer(home_probs, away_probs)

home_win = float(np.sum(np.tril(matrix, -1)))
draw = float(np.sum(np.diag(matrix)))
away_win = float(np.sum(np.triu(matrix, 1)))

under_2_5 = 0.0
for i in range(max_goals):
  for j in range(max_goals):
    if i + j <= 2:
      under_2_5 += matrix[i, j]
over_2_5 = 1.0 - under_2_5

btts_yes = 0.0
for i in range(1, max_goals):
  for j in range(1, max_goals):
    btts_yes += matrix[i, j]
btts_no = 1.0 - btts_yes

st.divider()
st.subheader(f"📈 Analyse de la rencontre : {home_team} vs {away_team}")

res_col1, res_col2, res_col3 = st.columns(3)
res_col1.metric(f"Victoire {home_team}", f"{home_win * 100:.1f}%")
res_col2.metric("Match nul", f"{draw * 100:.1f}%")
res_col3.metric(f"Victoire {away_team}", f"{away_win * 100:.1f}%")

st.markdown("---")

market_col1, market_col2 = st.columns(2)
with market_col1:
  st.markdown("### 🥅 Buts du match (Over / Under 2.5)")
  st.write(f"Plus de 2.5 buts (Over) : **{over_2_5 * 100:.1f}%**")
  st.write(f"Moins de 2.5 buts (Under) : **{under_2_5 * 100:.1f}%**")

with market_col2:
  st.markdown("### ⚽ Les deux équipes marquent (GG / NG)")
  st.write(f"Les deux équipes marquent (Oui) : **{btts_yes * 100:.1f}%**")
  st.write(f"Non / Un seul marque (Non) : **{btts_no * 100:.1f}%**")

st.markdown("---")
st.subheader("🚩 Analyse des Corners")
total_corners = home_corners + away_corners
st.info(
    "Moyenne totale estimée des corners :"
    f" **{total_corners:.1f}** corners dans le match"
    f" ({home_team}: {home_corners} | {away_team}: {away_corners})"
)
