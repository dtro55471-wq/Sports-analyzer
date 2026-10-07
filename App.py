import numpy as np
import pandas as pd
import scipy.stats as stats
import streamlit as st

st.set_page_config(
    page_title="المحلل الرياضي الشامل - عالمي", page_icon="⚽", layout="centered"
)

st.title("⚽ المحلل الرياضي الشامل لمباريات العالم")
st.markdown("اختر أي مباراة من مختلف دوريات وبطولات العالم لتحليلها فوراً.")

# قائمة موسعة تضم أبرز مباريات وبطولات العالم الكبرى
global_matches = {
    # دوري أبطال أوروبا
    "دوري أبطال أوروبا: ريال مدريد ضد مانشستر سيتي": {
        "home": "ريال مدريد",
        "away": "مانشستر سيتي",
        "h_xg": 1.85,
        "a_xg": 1.75,
        "h_c": 5.5,
        "a_c": 5.0,
    },
    "دوري أبطال أوروبا: بايرن ميونخ ضد باريس سان جيرمان": {
        "home": "بايرن ميونخ",
        "away": "باريس سان جيرمان",
        "h_xg": 1.95,
        "a_xg": 1.60,
        "h_c": 6.0,
        "a_c": 4.5,
    },
    "دوري أبطال أوروبا: برشلونة ضد إنتر ميلان": {
        "home": "برشلونة",
        "away": "إنتر ميلان",
        "h_xg": 1.70,
        "a_xg": 1.40,
        "h_c": 5.5,
        "a_c": 4.0,
    },
    # الدوري الإنجليزي الممتاز
    "الدوري الإنجليزي: أرسنال ضد ليفربول": {
        "home": "أرسنال",
        "away": "ليفربول",
        "h_xg": 1.75,
        "a_xg": 1.65,
        "h_c": 6.0,
        "a_c": 5.5,
    },
    "الدوري الإنجليزي: مانشستر يونايتد ضد تشيلسي": {
        "home": "مانشستر يونايتد",
        "away": "تشيلسي",
        "h_xg": 1.55,
        "a_xg": 1.50,
        "h_c": 5.0,
        "a_c": 5.0,
    },
    "الدوري الإنجليزي: توتنهام ضد نيوكاسل يونايتد": {
        "home": "توتنهام",
        "away": "نيوكاسل يونايتد",
        "h_xg": 1.60,
        "a_xg": 1.55,
        "h_c": 6.5,
        "a_c": 5.0,
    },
    # الدوري الإسباني
    "الدوري الإسباني: أتلتيكو مدريد ضد أتلتيك بلباو": {
        "home": "أتلتيكو مدريد",
        "away": "أتلتيك بلباو",
        "h_xg": 1.65,
        "a_xg": 1.10,
        "h_c": 5.0,
        "a_c": 4.0,
    },
    # الدوري الإيطالي
    "الدوري الإيطالي: يوفنتوس ضد ميلان": {
        "home": "يوفنتوس",
        "away": "ميلان",
        "h_xg": 1.45,
        "a_xg": 1.35,
        "h_c": 4.5,
        "a_c": 4.5,
    },
    "الدوري الإيطالي: نابولي ضد روما": {
        "home": "نابولي",
        "away": "روما",
        "h_xg": 1.75,
        "a_xg": 1.20,
        "h_c": 5.5,
        "a_c": 4.0,
    },
    # الدوري الألماني
    "الدوري الألماني: بوروسيا دورتموند ضد لايبزيغ": {
        "home": "بوروسيا دورتموند",
        "away": "لايبزيغ",
        "h_xg": 1.80,
        "a_xg": 1.50,
        "h_c": 6.0,
        "a_c": 5.0,
    },
    # دوري أبطال إفريقيا / العرب
    "دوري أبطال إفريقيا: الأهلي ضد الترجي التونسي": {
        "home": "الأهلي",
        "away": "الترجي التونسي",
        "h_xg": 1.60,
        "a_xg": 1.15,
        "h_c": 5.0,
        "a_c": 4.0,
    },
    "دوري أبطال إفريقيا: الوداد الرياضي ضد ماميلودي صنداونز": {
        "home": "الوداد الرياضي",
        "away": "ماميلودي صنداونز",
        "h_xg": 1.50,
        "a_xg": 1.30,
        "h_c": 4.5,
        "a_c": 4.5,
    },
    # مباراة مخصصة
    "🛠️ مباراة مخصصة (أدخل الفرق والأرقام يدوياً)": {
        "home": "المضيف",
        "away": "الضيف",
        "h_xg": 1.50,
        "a_xg": 1.20,
        "h_c": 5.0,
        "a_c": 4.0,
    },
}

st.sidebar.header("🌍 بطولات ودوريات العالم")
selected_match = st.sidebar.selectbox(
    "اختر المباراة للتحليل:", list(global_matches.keys())
)

match_info = global_matches[selected_match]

# تحديث الذاكرة المؤقتة للتطبيق
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

st.subheader("📊 إعدادات الأهداف المتوقعة (xG) والركنيات")
col1, col2 = st.columns(2)

with col1:
  home_team = st.text_input("الفريق المضيف", key="home_team")
  home_xg = st.number_input(
      "xG للمضيف",
      min_value=0.1,
      max_value=5.0,
      step=0.05,
      key="home_xg",
  )

with col2:
  away_team = st.text_input("الفريق الضيف", key="away_team")
  away_xg = st.number_input(
      "xG للضيف",
      min_value=0.1,
      max_value=5.0,
      step=0.05,
      key="away_xg",
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

# حساب احتمالات بواسون الإحصائية
max_goals = 7
home_probs = [stats.poisson.pmf(i, home_xg) for i in range(max_goals)]
away_probs = [stats.poisson.pmf(j, away_xg) for j in range(max_goals)]

matrix = np.outer)
