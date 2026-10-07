import numpy as np
import pandas as pd
import scipy.stats as stats
import streamlit as st

st.set_page_config(
    page_title="المحلل الرياضي الذكي للمباريات", page_icon="⚽", layout="centered"
)

st.title("⚽ المحلل الرياضي التفاعلي للمباريات")
st.markdown(
    "اختر مباراة مباشرة من القائمة الجانبية أو أدخل أرقامها لتحليل كافة"
    " الاحتمالات بشكل فوري."
)

# قائمة المباريات النموذجية التي يتم تحديثها
matches_data = {
    "اختر مباراة مخصصة (إدخال يدوي)": {
        "home": "المضيف",
        "away": "الضيف",
        "h_xg": 1.75,
        "a_xg": 1.10,
        "h_c": 5.5,
        "a_c": 4.5,
    },
    "ريال مدريد ضد برشلونة": {
        "home": "ريال مدريد",
        "away": "برشلونة",
        "h_xg": 1.90,
        "a_xg": 1.65,
        "h_c": 6.0,
        "a_c": 5.0,
    },
    "مانشستر سيتي ضد أرسنال": {
        "home": "مانشستر سيتي",
        "away": "أرسنال",
        "h_xg": 2.10,
        "a_xg": 1.50,
        "h_c": 6.5,
        "a_c": 4.0,
    },
    "بايرن ميونخ ضد بوروسيا دورتموند": {
        "home": "بايرن ميونخ",
        "away": "بوروسيا دورتموند",
        "h_xg": 2.20,
        "a_xg": 1.40,
        "h_c": 7.0,
        "a_c": 4.5,
    },
    "باريس سان جيرمان ضد مارسيليا": {
        "home": "باريس سان جيرمان",
        "away": "مارسيليا",
        "h_xg": 1.85,
        "a_xg": 1.15,
        "h_c": 5.5,
        "a_c": 3.5,
    },
}

st.sidebar.header("🗓️ قائمة المباريات المتاحة")
selected_match = st.sidebar.selectbox(
    "اختر المباراة للتحليل:", list(matches_data.keys())
)

match_info = matches_data[selected_match]

st.divider()

st.subheader("📊 بيانات الفريقين والأهداف المتوقعة (xG)")
col1, col2 = st.columns(2)

with col1:
  home_team = st.text_input("اسم الفريق المضيف", value=match_info["home"])
  home_xg = st.number_input(
      f"الأهداف المتوقعة لـ {home_team} (Home xG)",
      min_value=0.1,
      max_value=5.0,
      value=match_info["h_xg"],
      step=0.05,
  )

with col2:
  away_team = st.text_input("اسم الفريق الضيف", value=match_info["away"])
  away_xg = st.number_input(
      f"الأهداف المتوقعة لـ {home_team} (Away xG)"
      if False
      else f"الأهداف المتوقعة لـ {away_team} (Away xG)",
      min_value=0.1,
      max_value=5.0,
      value=match_info["a_xg"],
      step=0.05,
  )

st.subheader("🚩 الركنيات المتوقعة للمباراة")
col_c1, col_c2 = st.columns(2)
with col_c1:
  home_corners = st.number_input(
      f"ركنيات {home_team}",
      min_value=0.5,
      max_value=15.0,
      value=match_info["h_c"],
      step=0.5,
  )
with col_c2:
  away_corners = st.number_input(
      f"ركنيات {away_team}",
      min_value=0.5,
      max_value=15.0,
      value=match_info["a_c"],
      step=0.5,
  )

# حساب احتمالات الأهداف والنتيجة عبر توزيع بواسون
max_goals = 7
home_probs = [stats.poisson.pmf(i, home_xg) for i in range(max_goals)]
away_probs = [stats.poisson.pmf(j, away_xg) for j in range(max_goals)]

# مصفوفة احتمالات النتائج
matrix = np.outer(home_probs, away_probs)

home_win = np.sum(np.tril(matrix, -1))
draw = np.sum(np.diag(matrix))
away_win = np.sum(np.triu(matrix, 1))

# حساب Over / Under 2.5
under_2_5 = 0
over_2_5 = 0
for i in range(max_goals):
  for j in range(max_goals):
    if i + j <= 2:
      under_2_5 += matrix[i, j]
    else:
      over_2_5 += matrix[i, j]

# حساب GG / NG (تسجيل الفريقين)
btts_yes = 0
for i in range(1, max_goals):
  for j in range(1, max_goals):
    btts_yes += matrix[i, j]
btts_no = 1.0 - btts_yes

st.divider()
st.subheader(f"📈 نتائج وتحليلات لقاء: {home_team} ضد {away_team}")

# نتائج النتيجة الرئيسية (1X2)
res_col1, res_col2, res_col3 = st.columns(3)
res_col1.metric(f"فوز {home_team}", f"{home_win * 100:.1f}%")
res_col2.metric("تعادل", f"{draw * 100:.1f}%")
res_col3.metric(f"فوز {away_team}", f"{away_win * 100:.1f}%")

st.markdown("---")

# أسواق الأهداف و GG/NG
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
