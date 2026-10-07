import numpy as np
import pandas as pd
import requests
import scipy.stats as stats
import streamlit as st

st.set_page_config(
    page_title="المحلل الرياضي الذكي (مباريات حية)",
    page_icon="⚽",
    layout="centered",
)

st.title("⚽ المحلل الرياضي الذكي - جلب المباريات تلقائياً")
st.markdown(
    "يقوم هذا الإصدار بالبحث عن المباريات المتاحة وعرض تحليلات بواسون"
    " الإحصائية فوراً."
)


# دالة لجلب المباريات من مصدر رياضي مجاني متاح عاماً
@st.cache_data(ttl=600)  # تحديث البيانات كل 10 دقائق
def fetch_live_matches():
  try:
    # استخدام واجهة بيانات مجانية عامة للمباريات الحية واليومية
    url = "https://www.thesportsdb.com/api/v1/json/3/eventsday.php?d=2026-10-07"
    response = requests.get(url, timeout=5)
    data = response.json()
    if data and "events" in data and data["events"]:
      return data["events"]
  except:
    pass
  return None


# محاولة جلب المباريات الحية
live_events = fetch_live_matches()

matches_dict = {}

if live_events:
  for event in live_events:
    home = event.get("strHomeTeam", "مضيف")
    away = event.get("strAwayTeam", "ضيف")
    league = event.get("strLeague", "دوري عام")
    match_name = f"{home} ضد {away} ({league})"
    # تعيين قيم افتراضية للأهداف المتوقعة والركنيات بناءً على قوة فرق البث إن وجدت أو قيم تقديرية
    matches_dict[match_name] = {
        "home": home,
        "away": away,
        "h_xg": 1.65,
        "a_xg": 1.25,
        "h_c": 5.5,
        "a_c": 4.5,
    }

# إذا لم تتوفر مباريات حية عبر الشبكة في هذه اللحظة، نضيف قائمة مباريات بديلة لضمان عمل التطبيق بسلاسة
if not matches_dict:
  matches_dict = {
      "ريال مدريد ضد برشلونة (مباراة افتراضية)": {
          "home": "ريال مدريد",
          "away": "برشلونة",
          "h_xg": 1.90,
          "a_xg": 1.65,
          "h_c": 6.0,
          "a_c": 5.0,
      },
      "مانشستر سيتي ضد أرسنال (مباراة افتراضية)": {
          "home": "مانشستر سيتي",
          "away": "أرسنال",
          "h_xg": 2.10,
          "a_xg": 1.50,
          "h_c": 6.5,
          "a_c": 4.0,
      },
  }

st.sidebar.header("🗓️ جدول المباريات المتاحة")
selected_match = st.sidebar.selectbox(
    "اختر مباراة للتحليل:", list(matches_dict.keys())
)

match_info = matches_dict[selected_match]

st.divider()

st.subheader("📊 إعدادات الأهداف المتوقعة (xG) والركنيات")
col1, col2 = st.columns(2)

with col1:
  home_team = st.text_input("الفريق المضيف", value=match_info["home"])
  home_xg = st.number_input(
      f"xG لـ {home_team}",
      min_value=0.1,
      max_value=5.0,
      value=match_info["h_xg"],
      step=0.05,
  )

with col2:
  away_team = st.text_input("الفريق الضيف", value=match_info["away"])
  away_xg = st.number_input(
      f"xG لـ {away_team}",
      min_value=0.1,
      max_value=5.0,
      value=match_info["a_xg"],
      step=0.05,
  )

st.subheader("🚩 الركنيات المتوقعة")
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

# حساب احتمالات بواسون
max_goals = 7
home_probs = [stats.poisson.pmf(i, home_xg) for i in range(max_goals)]
away_probs = [stats.poisson.pmf(j, away_xg) for j in range(max_goals)]

matrix = np.outer(home_probs, away_probs)

home_win = np.sum(np.tril(matrix, -1))
draw = np.sum(np.diag(matrix))
away_win = np.sum(np.triu(matrix, 1))

under_2_5 = sum(
    matrix[i, j] for i in range(max_goals) for j in range(max_goals) if i + j <= 2
)
over_2_5 = 1.0 - under_2_5

btts_yes = sum(
    matrix[i, j]
    for i in range(1, max_goals)
    for j in range(1, max_goals)
)
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
