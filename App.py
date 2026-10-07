import numpy as np
import pandas as pd
import scipy.stats as stats
import streamlit as st

st.set_page_config(
    page_title="المحلل الرياضي الشامل", page_icon="⚽", layout="centered"
)

st.title("⚽ المحلل الرياضي الشامل لمباريات العالم")
st.markdown("اختر أي مباراة من القائمة الجانبية لتحليلها فوراً.")

# قائمة المباريات الشاملة
global_matches = {
    "ريال مدريد ضد مانشستر سيتي": {
        "home": "ريال مدريد",
        "away": "مانشستر سيتي",
        "h_xg": 1.85,
        "a_xg": 1.75,
        "h_c": 5.5,
        "a_c": 5.0,
    },
    "بايرن ميونخ ضد باريس سان جيرمان": {
        "home": "بايرن ميونخ",
        "away": "باريس سان جيرمان",
        "h_xg": 1.95,
        "a_xg": 1.60,
        "h_c": 6.0,
        "a_c": 4.5,
    },
    "أرسنال ضد ليفربول": {
        "home": "أرسنال",
        "away": "ليفربول",
        "h_xg": 1.75,
        "a_xg": 1.65,
        "h_c": 6.0,
        "a_c": 5.5,
    },
    "برشلونة ضد أتلتيكو مدريد": {
        "home": "برشلونة",
        "away": "أتلتيكو مدريد",
        "h_xg": 1.70,
        "a_xg": 1.40,
        "h_c": 5.5,
        "a_c": 4.0,
    },
    "الأهلي ضد الترجي التونسي": {
        "home": "الأهلي",
        "away": "الترجي التونسي",
        "h_xg": 1.60,
        "a_xg": 1.15,
        "h_c": 5.0,
        "a_c": 4.0,
    },
    "🛠️ مباراة مخصصة (إدخال يدوي)": {
        "home": "المضيف",
        "away": "الضيف",
        "h_xg": 1.50,
        "a_xg": 1.20,
        "h_c": 5.0,
        "a_c": 4.0,
    },
}

st.sidebar.header("🌍 جدول المباريات")
selected_match = st.sidebar.selectbox(
    "اختر المباراة:", list(global_matches.keys())
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
  home_team = st.text_input("الفريق المضيف", key="home_team")
  home_xg = st.number_input(
      "xG للمضيف", min_value=0.1, max_value=5.0, step=0.05, key="home_xg"
  )
with col2:
  away_team = st.text_input("الفريق الضيف", key="away_team")
  away_xg = st.number_input(
      "xG للضيف", min_value=0.1, max_value=5.0, step=0.05, key="away_xg"
  )

st.subheader("🚩 الركنيات المتوقعة")
col_c1, col_c2 = st.columns(2)
with col_c1:
  home_corners = st.number_input(
      "ركنيات المضيف",
      min_value=0.5,
      max_value=15.0,
      step=0.5,
      key="home_corners",
  )
with col_c2:
  away_corners = st.number_input(
      "ركنيات الضيف",
      min_value=0.5,
      max_value=15.0,
      step=0.5,
      key="away_corners",
  )

# حساب احتمالات بواسون
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
st.subheader(f"📈 تحليل لقاء: {home_team} ضد {away_team}")

res_col1, res_col2, res_col3 = st.columns(3)
res_col1.metric(f"فوز {home_team}", f"{home_win * 100:.1f}%")
res_col2.metric("تعادل", f"{draw * 100:.1f}%")
res_col3.metric(f"فوز {away_team}", f"{away_win * 100:.1f}%")

st.markdown("---")

market_col1, market_col2 = st.columns(2)
with market_col1:
  st.markdown("### 🥅 أهداف المباراة (Over / Under 2.5)")
  st.write(f"أكثر من 2.5 هدف (Over): **{over_2_5 * 100:.1f}%**")
  st.write(f"أقل من 2.5 هدف (Under): **{under_2_5 * 100:.1f}%**")

with market_col2:
  st.markdown("### ⚽ تسجيل الفريقين (GG / NG)")
  st.write(f"كلا الفريقين يسجلان (GG): **{btts_yes * 100:.1f}%**")
  st.write(f"لا يسجل الفريقان أو أحدهما (NG): **{btts_no * 100:.1f}%**")

st.markdown("---")
st.subheader("🚩 تحليل الركنيات (Corners)")
total_corners = home_corners + away_corners
st.info(
    f"المعدل الإجمالي المتوقع للركنيات: **{total_corners:.1f}** ركنية في اللقاء"
    f" ({home_team}: {home_corners} | {away_team}: {away_corners})"
)
