import streamlit as st
from api import nav_page, send_res_val

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

# 세션 저장 값 호출
# 1. 충전소 명
# 2. 차량번호 (뒤 4자리)
# 3. 예약자 성함
# 4. 전화번호
# 5. 예약시간

chr = st.session_state.user_input1
car_num = st.session_state.user_input2
name = st.session_state.user_input3
ph_num = st.session_state.user_input4
res_time = st.session_state.user_input5

# 예약자 정보 출력
st.header("예약 정보 확인")
st.write("충전소 : " + chr)
st.write("차량번호 : " + car_num)
st.write("성함 : " + name)
st.write("전화번호 : " + ph_num)
st.write("예약 시간 : " + res_time)

col1, col2, col3 = st.columns([0.3,0.9,1])
with col1 :
    if st.button("예약 확정") :
        nav_page("sucsess")
        send_res_val(chr , car_num, name, ph_num, res_time)

with col2 :
    if st.button("돌아가기") :
        nav_page("reservation")