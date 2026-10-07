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
avg_corners = st.sidebar.slider(
    "Moyenne Estimée des Corners", min_value=6.0, max_value=14.0, value=9.5, step=0.5
)

# حساب الاحتمالات الضمنية وإزالة هامش الربح
imp_h = 1.0 / cote_home
imp_d = 1.0 / cote_draw
imp_a = 1.0 / cote_away
total_margin = imp_h + imp_d + imp_a

fair_h = imp_h / total_margin
fair_d = imp_d / total_margin
fair_a = imp_a / total_margin

# استنتاج الأهداف المتوقعة (xG) بدقة عالية من الكوطات
total_xg = 2.75
h_xg = max(
    0.5, min(4.0, total_xg * (fair_h + 0.5 * fair_d) / (fair_h + fair_d + fair_a))
)
a_xg = max(
    0.5, min(4.0, total_xg * (fair_a + 0.5 * fair_d) / (fair_h + fair_d + fair_a))
)

# محاكاة بواسون الرياضية المتقدمة
max_g = 6
h_probs = [stats.poisson.pmf(i, h_xg) for i in range(max_g)]
a_probs = [stats.poisson.pmf(j, away_xg) for j in range(max_g)]
mat = np.outer(h_probs, a_probs)

model_hw = float(np.sum(np.tril(mat, -1)))
model_dr = float(np.sum(np.diag(mat)))
model_aw = float(np.sum(np.triu(mat, 1)))

u25 = float(
    sum(mat[i, j] for i in range(max_g) for j in range(max_g) if i + j <= 2)
)
o25 = 1.0 - u25

btts_y = float(
    sum(mat[i, j] for i in range(1, max_g) for j in range(1, max_g))
)
btts_n = 1.0 - btts_y

cs_h = float(a_probs[0])
cs_a = float(h_probs[0])

# الواجهة الرئيسية
st.subheader(
    f"📈 Analyse Statistique de Haute Précision : {home_team} vs {away_team}"
)

col1, col2, col3 = st.columns(3)
col1.metric(
    f"Victoire {home_team}",
    f"{model_hw * 100:.1f}%",
    delta=f"Cote: {cote_home}",
)
col2.metric("Match Nul (X)", f"{model_dr * 100:.1f}%", delta=f"Cote: {cote_draw}")
col3.metric(
    f"Victoire {away_team}",
    f"{model_aw * 100:.1f}%",
    delta=f"Cote: {cote_away}",
)

st.markdown("---")

st.subheader("💡 Détection des Value Bets (Opportunités de Paris)")


def check_value(model_prob, cote):
  implied = 1.0 / cote
  edge = (model_prob - implied) * 100
  if edge > 3.0:
    return f"🔥 Value Bet Fort! (Edge: +{edge:.1f}%)"
  elif edge > 0:
    return f"👍 Légère Valeur (Edge: +{edge:.1f}%)"
  else:
    return f"⚠️ Pas de Valeur (Edge: {edge:.1f}%)"


st.info(
    f"**1️⃣ {home_team} :** {check_value(model_hw, cote_home)}\n\n"
    f"**🟰 Match Nul (X) :** {check_value(model_dr, cote_draw)}\n\n"
    f"**2️⃣ {away_team} :** {check_value(model_aw, cote_away)}"
)

st.markdown("---")

m1, m2 = st.columns(2)
with m1:
  st.markdown("### 🥅 Buts & xG")
  st.write(f"xG Domicile : **{h_xg:.2f}**")
  st.write(f"xG Extérieur : **{a_xg:.2f}**")
  st.write(f"Over 2.5 : **{o25 * 100:.1f}%**")
  st.write(f"Under 2.5 : **{u25 * 100:.1f}%**")
  st.write(f"BTTS (Oui) : **{btts_y * 100:.1f}%**")

with m2:
  st.markdown("### 🛡️ Défense & Corners")
  st.write(f"Clean Sheet {home_team} : **{cs_h * 100:.1f}%**")
  st.write(f"Clean Sheet {away_team} : **{cs_a * 100:.1f}%**")
  st.write(f"Corners Estimés : **{avg_corners}**")

st.markdown("---")
st.subheader("🎯 Matrice des Scores Exacts")

scores_list = []
for h in range(4):
  for a in range(4):
    p = float(mat[h, a] * 100)
    scores_list.append(
        {
            "Score": f"{h} - {a}",
            "Probabilité (%)": round(p, 2),
        }
    )

df_scores = pd.DataFrame(scores_list).sort_values(
    by="Probabilité (%)", ascending=False
)
st.dataframe(df_scores.head(6), use_container_width=True)
