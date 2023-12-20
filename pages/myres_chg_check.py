import streamlit as st
from api import nav_page, send_res_val
from streamlit.components.v1 import html
import json 

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

chr_name = st.session_state.user_input15
car_num = st.session_state.user_input16
name = st.session_state.user_input17
ph_num = st.session_state.user_input18
old_res_date = st.session_state.user_input19
new_res_date = st.session_state.user_input20

# 예약자 정보 출력
st.header("예약 정보 변경 확인")
st.write("충전소 : " + chr_name)
st.write("차량번호 : " + car_num)
st.write("성함 : " + name)
st.write("전화번호 : " + ph_num)
st.write("변경 전 예약 시간 : " + old_res_date)
st.write("변경 된 예약 시간 : " + new_res_date)

res_info = {
    "chr_name" : chr_name,
    "car_num" : car_num,
    "name" : name,
    "ph_num" : ph_num,
    "old_res_time" : old_res_date,
    "new_res_time" : new_res_date
}

col1, col2, col3 = st.columns([0.4,0.9,1])

with col1 :
    if st.button("예약 변경 확정") :
        if(send_res_val(res_info) == '1') :
            try :
                nav_page("sucsess_chg")
            except :
                pass
        else :
            try :
                my_js = """
                    alert("예약 변경을 할 수 없습니다. 해당 시간에 이미 예약이 있습니다.");
                    """
                my_html = f"<script>{my_js}</script>"
                html(my_html)
                nav_page("myres_chg")
            except :
                pass

        

with col2 :
    if st.button("처음으로") :
        nav_page("home")