import streamlit as st
from api import nav_page, get_able_book
from streamlit.components.v1 import html
import pandas as pd
import datetime

# 슬라이드바 제거
hide_navi = """
<style>
    /* Hide the sidebar navigation */
    [data-testid="stSidebar"] {
        display: none;
    }
    </style>
"""

st.markdown(hide_navi, unsafe_allow_html=True)

st.title("예약 변경")
time_term = get_able_book()

col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)
col7, col8, col9 = st.columns(3)
col13, col14, col15 = st.columns(3)
col10, col11, col12 = st.columns([0.3,0.9,1])

chr_sel = st.session_state.user_input10
car_num = st.session_state.user_input11
ph_num = st.session_state.user_input12
name = st.session_state.user_input13
old_res_time = st.session_state.user_input14

with col1 : 
    chr = st.text_input("방문 충전소", chr_sel)
with col2 :
    car_num = st.text_input("차량번호 (뒤 4자리)", car_num)

with col4 :
    name = st.text_input("이름", name)
with col5 :
    ph_num = st.text_input("전화번호( - 없이 입력해주세요)", ph_num)

with col7 :
    # 오늘 날짜 계산
    today = datetime.datetime.today()

    # 날짜 입력 받기 (오늘부터 선택 가능)
    d = st.date_input("예약 날짜", today, min_value=today)

with col8 :
    t = st.selectbox('충전 예약 시간', (time_term))

# SessionState에 사용자 입력값 저장
if 'user_input15' not in st.session_state:
    st.session_state.user_input15 = ""

if 'user_input16' not in st.session_state:
    st.session_state.user_input16= ""

if 'user_input17' not in st.session_state:
    st.session_state.user_input17 = ""

if 'user_input18' not in st.session_state:
    st.session_state.user_input18 = ""

if 'user_input19' not in st.session_state:
    st.session_state.user_input19 = ""

if 'user_input20' not in st.session_state:
    st.session_state.user_input20 = ""

with col10 :
    if st.button("예약 변경") :
        st.session_state.user_input15 = chr_sel
        st.session_state.user_input16 = car_num
        st.session_state.user_input17 = name
        st.session_state.user_input18 = ph_num
        st.session_state.user_input19 = old_res_time
        st.session_state.user_input20 = f"{d} {t}"
        
        nav_page("myres_chg_check")

with col11 :
    if st.button("취소하기") :
        nav_page("home")