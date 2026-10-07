import numpy as np
import pandas as pd
import scipy.stats as stats
import streamlit as st

st.set_page_config(
    page_title="المحلل الرياضي المتقدم", page_icon="⚽", layout="centered"
)

st.title("⚽ المحلل الرياضي التفاعلي المتقدم")
st.markdown(
    "برنامج تحليلي متطور يعتمد على توزيع بواسون الإحصائي لتوقع كافة خيارات"
    " المباريات (النتيجة، الأهداف، والركنيات)."
)

st.sidebar.header("إعدادات البيانات")
input_mode = st.sidebar.radio(
    "طريقة إدخال البيانات:", ("إدخال يدوي (xG)", "جلب تلقائي (عبر API قريباً)")
)

st.divider()

st.subheader("📊 إدخال أرقام المباراة والأهداف المتوقعة")
col1, col2 = st.columns(2)

with col1:
  home_xg = st.number_input(
      "الأهداف المتوقعة للمضيف (Home xG)",
      min_value=0.1,
      max_value=5.0,
      value=1.75,
      step=0.05,
  )

with col2:
  away_xg = st.number_input(
      "الأهداف المتوقعة للضيف (Away xG)",
      min_value=0.1,
      max_value=5.0,
      value=1.10,
      step=0.05,
  )

st.subheader("🚩 الركنيات المتوقعة للمباراة")
col_c1, col_c2 = st.columns(2)
with col_c1:
  home_corners = st.number_input(
      "ركنيات المضيف", min_value=0.5, max_value=15.0, value=5.5, step=0.5
  )
with col_c2:
  away_corners = st.number_input(
      "ركنيات الضيف", min_value=0.5, max_value=15.0, value=4.5, step=0.5
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
st.subheader("📈 نتائج وتحليلات الاحتمالات الشاملة")

# نتائج النتيجة الرئيسية (1X2)
res_col1, res_col2, res_col3 = st.columns(3)
res_col1.metric("فوز المضيف", f"{home_win * 100:.1f}%")
res_col2.metric("تعادل", f"{draw * 100:.1f}%")
res_col3.metric("فوز الضيف", f"{away_win * 100:.1f}%")

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
    f" (المضيف: {home_corners} | الضيف: {away_corners})"
)
