import streamlit as st
import requests
import numpy as np
from scipy.stats import poisson

st.set_page_config(page_title="المحلل الرياضي الذكي", page_icon="⚽", layout="wide")

st.title("⚽ المحلل الرياضي التفاعلي لحساب الاحتمالات")
st.write("برنامج تحليلي يعتمد على توزيع بواسون الإحصائي لتوقع كافة خيارات المباريات.")

# الرمز الخاص بك جاهز ومدمج تلقائياً
API_KEY = "yldcCxtiEP"

@st.cache_data(ttl=3600)
def fetch_upcoming_matches():
    url = f"https://admin.soccersapi.com/v2.2/leagues/?action=list&secret={API_KEY}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"خطأ أثناء جلب البيانات: {e}")
    return {}

def calculate_predictions(home_xg, away_xg):
    goals = range(6)
    home_probs = [poisson.pmf(g, home_xg) for g in goals]
    away_probs = [poisson.pmf(g, away_xg) for g in goals]
    
    score_matrix = np.outer(home_probs, away_probs)
    
    home_win = np.sum(np.tril(score_matrix, -1)) * 100
    draw = np.sum(np.diag(score_matrix)) * 100
    away_win = np.sum(np.triu(score_matrix, 1)) * 100
    
    over_25 = np.sum([score_matrix[h, a] for h in goals for a in goals if h + a > 2.5]) * 100
    under_25 = 100 - over_25
    
    btts_yes = np.sum(score_matrix[1:, 1:]) * 100
    btts_no = 100 - btts_yes
    
    exact_scores = []
    for h in goals:
        for a in goals:
            exact_scores.append((f"{h} - {a}", score_matrix[h, a] * 100))
    exact_scores.sort(key=lambda x: x[1], reverse=True)
    
    return {
        "home_win": home_win, "draw": draw, "away_win": away_win,
        "over_25": over_25, "under_25": under_25,
        "btts_yes": btts_yes, "btts_no": btts_no,
        "top_scores": exact_scores[:5]
    }

st.subheader("📊 إدخال أرقام المباراة لحساب التوقع")
col_input1, col_input2 = st.columns(2)
with col_input1:
    home_xg = st.number_input("الأهداف المتوقعة للفريق المضيف (Home xG):", min_value=0.1, max_value=5.0, value=1.75, step=0.05)
with col_input2:
    away_xg = st.number_input("الأهداف المتوقعة للفريق الضيف (Away xG):", min_value=0.1, max_value=5.0, value=1.10, step=0.05)

res = calculate_predictions(home_xg, away_xg)

st.markdown("---")
c1, c2, c3 = st.columns(3)
c1.metric("فوز المضيف", f"{res['home_win']:.1f}%")
c2.metric("التعادل", f"{res['draw']:.1f}%")
c3.metric("فوز الضيف", f"{res['away_win']:.1f}%")

st.markdown("---")
col_a, col_b = st.columns(2)
with col_a:
    st.write("### ⚽ سوق الأهداف (Total Goals)")
    st.write(f"• **أكثر من 2.5 هدف (Over 2.5):** {res['over_25']:.1f}%")
    st.write(f"• **أقل من 2.5 هدف (Under 2.5):** {res['under_25']:.1f}%")
    
    st.write("### 🥅 كلا الفريقين يسجلان (BTTS)")
    st.write(f"• **نعم (Yes):** {res['btts_yes']:.1f}%")
    st.write(f"• **لا (No):** {res['btts_no']:.1f}%")

with col_b:
    st.write("### 🎯 أكثر 5 نتائج دقيقة احتمالية (Correct Score)")
    for score, prob in res['top_scores']:
        st.write(f"• النتيجة **({score})**: بنسبة **{prob:.1f}%**")
