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
    " analyse mathématique de haute précision (Modèle Poisson & Détection de"
    " Value Bets)."
)

# شريط جانبى لإدخال أسماء الأندية والكوطات (Cotes)
st.sidebar.header("⚙️ Saisie des Clubs & Cotes")
home_team = st.sidebar.text_input("Équipe Domicile", "Real Madrid")
away_team = st.sidebar.text_input("Équipe Extérieur", "Manchester City")

st.sidebar.markdown("---")
st.sidebar.subheader("📊 Cotes du Bookmaker (1X2)")
cote_home = st.sidebar.number_input(
    f"Cote 1 ({home_team})", min_value=1.01, max_value=50.0, value=2.10, step=0.05
)
cote_draw = st.sidebar.number_input(
    "Cote X (Nul)", min_value=1.01, max_value=50.0, value=3.40, step=0.05
)
cote_away = st.sidebar.number_input(
    f"Cote 2 ({away_team})", min_value=1.01, max_value=50.0, value=3.20, step=0.05
)

st.sidebar.markdown("---")
st.sidebar.subheader("🚩 Paramètres Avancés")
avg_corners = st.sidebar.slider(
    "Moyenne Estimée des Corners", min_value=6.0, max_value=14.0, value=9.5, step=0.5
)

# 1. حساب الاحتمالات الضمنية من الكوطات (Implied Probabilities & Margin Removal)
imp_h = 1.0 / cote_home
imp_d = 1.0 / cote_draw
imp_a = 1.0 / cote_away
total_margin = imp_h + imp_d + imp_a

# الاحتمالات الحقيقية بعد إزالة هامش ربح الشركة (Fair Probabilities)
fair_h = imp_h / total_margin
fair_d = imp_d / total_margin
fair_a = imp_a / total_margin

# 2. استنتاج الأهداف المتوقعة (xG) بدقة عالية من الكوطات وتوزيع القوة
total_expected_goals = 2.75
h_xg = max(
    0.5,
    min(
        4.0,
        total_expected_goals
        * (fair_h + 0.5 * fair_d)
        / (fair_h + fair_d + fair_a),
    )
)
a_xg = max(
    0.5,
    min(
        4.0,
        total_expected_goals
        * (fair_a + 0.5 * fair_d)
        / (fair_h + fair_d + fair_a),
    )
)

# 3. محاكاة بواسون الرياضية المتقدمة
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

# العرض الرئيسي في الواجهة
st.subheader(
    f"📈 Analyse Statistique de Haute Précision : {home_team} vs {away_team}"
)

col1, col2, col3 = st.columns(3)
col1.metric(
    f"Modèle {home_team}",
    f"{model_hw * 100:.1f}%",
    delta=f"Cote: {cote_home}",
)
col2.metric("Modèle Nul (X)", f"{model_dr * 100:.1f}%", delta=f"Cote: {cote_draw}")
col3.metric(
    f"Modèle {away_team}",
    f"{model_aw * 100:.1f}%",
    delta=f"Cote: {cote_away}",
)

st.markdown("---")

# 4. نظام كشف القيم الرابحة (Value Bets Detection Engine)
st.subheader("💡 Détection des Value Bets (Analyse de Rentabilité)")
st.markdown(
    "Comparaison intelligente entre le modèle mathématique et les cotes du"
    " bookmaker :"
)


def check_value(model_prob, cote):
  implied = 1.0 / cote
  edge = (model_prob - implied) * 100
  if edge > 3.0:
    return (
        f"🔥 Value Bet Fort! (Edge: +{edge:.1f}%) - Opportunité Hautement"
        " Rentable"
    )
  elif edge > 0:
    return f"👍 Légère Valeur (Edge: +{edge:.1f}%)"
  else:
    return f"⚠️ Pas de Valeur (Edge: {edge:.1f}% - À Éviter)"


vb1 = check_value(model_hw, cote_home)
vb2 = check_value(model_dr, cote_draw)
vb3 = check_value(model_aw, cote_away)

st.info(
    f"**1️⃣ Victoire {home_team} :** {vb1}\n\n"
    f"**🟰 Match Nul (X) :** {vb2}\n\n"
    f"**2️⃣ Victoire {away_team} :** {vb3}"
)

st.markdown("---")

# 5. الأسواق المتقدمة (أهداف، شباك نظيفة، ركنيات)
m_col1, m_col2 = st.columns(2)
with m_col1:
  st.markdown("### 🥅 Marché des Buts & xG")
  st.write(f"xG Estimé ({home_team}) : **{h_xg:.2f} buts**")
  st.write(f"xG Estimé ({away_team}) : **{a_xg:.2f} buts**")
  st.write(f"Plus de 2.5 buts (Over 2.5) : **{o25 * 100:.1f}%**")
  st.write(f"Moins de 2.5 buts (Under 2.5) : **{u25 * 100:.1f}%**")
  st.write(f"Les deux équipes marquent (BTTS Oui) : **{btts_y * 100:.1f}%**")

with m_col2:
  st.markdown("### 🛡️ Défense & Corners")
  st.write(
      f"Clean Sheet {home_team} (Sans encaisser) :"
      f" **{cs_h * 100:.1f}%**"
  )
  st.write(
      f"Clean Sheet {away_team} (Sans encaisser) :"
      f" **{cs_a * 100:.1f}%**"
  )
  st.write(f"Moyenne Estimée des Corners : **{avg_corners}** corners")

st.markdown("---")

# 6. مصفوفة النتائج الدقيقة
st.subheader("🎯 Matrice des Scores Exacts (Top 6)")
scores = []
for h in range(4):
  for a in range(4):
    scores.append(
  
