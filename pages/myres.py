import streamlit as st
from api import nav_page
from streamlit.components.v1 import html

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

st.title("내 예약 정보 찾기")
st.subheader("예약자 정보를 입력하세요")
col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)
col7, col8, col9 = st.columns(3)
col10, col11, col12 = st.columns([0.3,0.9,1])

with col1 : 
    res_name = st.text_input("이름")
with col4 :
    res_car_num = st.text_input("차량번호 (뒤 4자리)")
with col7 :
    res_ph_num = st.text_input("전화번호( - 없이 입력해주세요)")

if 'user_input7' not in st.session_state:
    st.session_state.user_input7 = ""

if 'user_input8' not in st.session_state:
    st.session_state.user_input8 = ""

if 'user_input9' not in st.session_state:
    st.session_state.user_input9= ""

with col10 :
    if st.button("예약 확인") :
        st.session_state.user_input7 = res_name
        st.session_state.user_input8 = res_car_num
        st.session_state.user_input9 = res_ph_num
        nav_page("myres_result")

with col11 :
    if st.button("처음으로") :
        nav_page("home")