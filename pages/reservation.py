import streamlit as st
from api import get_able_book, nav_page

from datetime import datetime

chr_sel = (st.session_state.user_input)

hide_navi = """
<style>
    /* Hide the sidebar navigation */
    [data-testid="stSidebar"] {
        display: none;
    }
    </style>
"""

st.markdown(hide_navi, unsafe_allow_html=True)

time_term = get_able_book()

st.title("예약 정보")
col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)
col7, col8, col9 = st.columns(3)
col10, col11, col12 = st.columns([0.3,0.9,1])

with col1 : 
    chr = st.text_input("방문 충전소", chr_sel)
with col2 :
    car_num = st.text_input("차량번호 (뒤 4자리)")

with col4 :
    name = st.text_input("이름")
with col5 :
    ph_num = st.text_input("전화번호( - 없이 입력해주세요)")

with col7 :
    # 오늘 날짜 계산
    today = datetime.today()

    # 날짜 입력 받기 (오늘부터 선택 가능)
    d = st.date_input("예약 날짜", today, min_value=today)

with col8 :
    t = st.selectbox('충전 예약 시간', (time_term))

# SessionState에 사용자 입력값 저장
if 'user_input1' not in st.session_state:
    st.session_state.user_input1 = ""

if 'user_input2' not in st.session_state:
    st.session_state.user_input2 = ""

if 'user_input3' not in st.session_state:
    st.session_state.user_input3 = ""

if 'user_input4' not in st.session_state:
    st.session_state.user_input4 = ""

if 'user_input5' not in st.session_state:
    st.session_state.user_input5 = ""

if 'user_input6' not in st.session_state:
    st.session_state.user_input6= ""

with col10 :
    if st.button("예약하기") :
        st.session_state.user_input1 = chr_sel
        st.session_state.user_input2 = car_num
        st.session_state.user_input3 = name
        st.session_state.user_input4 = ph_num
        st.session_state.user_input5 = str(d)
        st.session_state.user_input6 = t
        
        nav_page("reservation_check")

with col11 :
    if st.button("취소하기") :
        nav_page("home")