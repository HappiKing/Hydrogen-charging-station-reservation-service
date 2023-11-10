import streamlit as st
from api import nav_page

hide_navi = """
<style>
    /* Hide the sidebar navigation */
    [data-testid="stSidebar"] {
        display: none;
    }
    </style>
"""

st.markdown(hide_navi, unsafe_allow_html=True)

st.header("예약이 완료되었습니다")

if st.button("돌아가기") :
    nav_page("home")