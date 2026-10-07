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
    },
    "🇪🇸 La Liga": {
        "Real Madrid vs Barcelone": {
            "home": "Real Madrid",
            "away": "Barcelone",
            "h_xg": 1.9,
            "a_xg": 1.8,
            "h_c": 6.0,
            "a_c": 5.0,
        }
    },
}

st.sidebar.header("🌍 Navigation")
sel_league = st.sidebar.selectbox("Championnat:", list(leagues.keys()))
match_dict = leagues[sel_league]
sel_match = st.sidebar.selectbox("Match:", list(match_dict.keys()))

info = match_dict[sel_match]

if "cur" not in st.session_state or st.session_state.cur != sel_match:
  st.session_state.cur = sel_match
  st.session_state.h_team = info["home"]
  st.session_state.a_team = info["away"]
  st.session_state.h_xg = info["h_xg"]
  st.session_state.a_xg = info["a_xg"]
  st.session_state.h_c = info["h_c"]
  st.session_state.a_c = info["a_c"]

st.divider()

col1, col2 = st.columns(2)
with col1:
  home_team = st.text_input("Équipe Domicile", key="h_team")
  home_xg = st.number_input(
      "xG Domicile", 0.1, 6.0, 0.05, key="h_xg", format="%.2f"
  )
with col2:
  away_team = st.text_input("Équipe Extérieur", key="a_team")
  away_xg = st.number_input(
      "xG Extérieur", 0.1, 6.0, 0.05, key="a_xg", format="%.2f"
  )

st.subheader("🚩 Corners")
col_c1, col_c2 = st.columns(2)
with col_c1:
  home_corners = st.number_input("Corners Domicile", 0.5, 15.0, 0.5, key="h_c")
with col_c2:
  away_corners = st.number_input("Corners Extérieur", 0.5, 15.0, 0.5, key="a_c")

max_g = 6
h_probs = [stats.poisson.pmf(i, home_xg) for i in range(max_g)]
a_probs = [stats.poisson.pmf(j, away_xg) for j in range(max_g)]
mat = np.outer(h_probs, a_probs)

hw = float(np.sum(np.tril(mat, -1)))
dr = float(np.sum(np.diag(mat)))
aw = float(np.sum(np.triu(mat, 1)))

u25 = float(sum(mat[i, j] for i in range(max_g) for j in range(max_g) if i + j <= 2))
o25 = 1.0 - u25

btts_y = float(
    sum(mat[i, j] for i in range(1, max_g) for j in range(1, max_g))
)
btts_n = 1.0 - btts_y

cs_h = float(a_probs[0])
cs_a = float(h_probs[0])

st.divider()
st.subheader(f"📈 Analyse : {home_team} vs {away_team}")

r1, r2, r3 = st.columns(3)
r1.metric(f"Victoire {home_team}", f"{hw * 100:.1f}%")
r2.metric("Nul", f"{dr * 100:.1f}%")
r3.metric(f"Victoire {away_team}", f"{aw * 100:.1f}%")

st.markdown("---")
m1, m2 = st.columns(2)
with m1:
  st.markdown("### 🥅 Buts")
  st.write(f"Over 2.5 : **{o25 * 100:.1f}%**")
  st.write(f"Under 2.5 : **{u25 * 100:.1f}%**")
  st.write(f"BTTS (Oui) : **{btts_y * 100:.1f}%**")
  st.write(f"BTTS (Non) : **{btts_n * 100:.1f}%**")

with m2:
  st.markdown("### 🛡️ Clean Sheets & Corners")
  st.write(f"Clean Sheet {home_team} : **{cs_h * 100:.1f}%**")
  st.write(f"Clean Sheet {away_team} : **{cs_a * 100:.1f}%**")
  st.write(f"Total Corners : **{home_corners + away_corners:.1f}**")

st.markdown("---")
st.subheader("🎯 Scores Exacts")
scores = []
for h in range(4):
  for a in range(4):
    scores.append(
        {
            "Score": f"{h} - {a}",
            "Probabilité (%)": round(mat[h, a] * 100, 2),
        }
    )

df = pd.DataFrame(scores).sort_values(by="Probabilité (%)", ascending=False)
st.dataframe(df.head(6), use_container_width=True)
