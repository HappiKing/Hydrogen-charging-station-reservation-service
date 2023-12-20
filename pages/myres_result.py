import streamlit as st
from api import nav_page, send_res_val
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

st.title("내 예약 정보 찾기")


res_name = st.session_state.user_input7
res_car_num = st.session_state.user_input8
res_ph_num = st.session_state.user_input9

res_info = {
    "car_num" : res_car_num,
    "name" : res_name,
    "ph_num" : res_ph_num,
}

data = send_res_val(res_info)
print(type(data))
print("\n\n\n\n")
print(data)
data = data.replace('"', '')
list_of_dicts = eval('[' + data + ']')
df = pd.DataFrame(list_of_dicts)

print(list_of_dicts)
# 현재 날짜와 시간 얻기
today = datetime.datetime.now()

# 현재 날짜를 원하는 형식으로 포맷팅
formatted_today = today.strftime('%Y-%m-%d')

st.markdown("### 이전 예약")
filtered_df_old = df[df['res_time'] < formatted_today]
st.write(filtered_df_old)

st.markdown("### 예약 현황")
filtered_df_now = df[df['res_time'] >= formatted_today]
st.write(filtered_df_now)

col1, col2, col3= st.columns([0.7,0.3,0.8])
col4, col5, col6, col7 = st.columns([0.2, 0.2 ,0.2, 1])

with col1 :
    data = []
    for i in range(len(df)):
        str_d = f"{df.iloc[i][0]}, {df.iloc[i][1]}, {df.iloc[i][4]}, {df.iloc[i][2]}, {df.iloc[i][3]}"
        if df.iloc[i][4] > datetime.datetime.now() :
            data.append(str_d)
    
    # 선택한 값을 출력
    sel_res = st.selectbox("취소할 예약을 선택하세요",data)
    
    res = str(sel_res)
    # ','를 기준으로 문자열을 분할하여 배열로 저장
    res = res.split(', ')
    print(res)

with col4 :
    if st.button("예약 취소"):
        res_info = {
        "chr_name" : res[0],
        "car_num" : res[1],
        "res_time" : res[2],
        }
        send_res_val(res_info)

        nav_page("myres_result")


with col5 :
    if st.button("예약 변경"):
        if 'user_input10' not in st.session_state:
            st.session_state.user_input10 = ""

        if 'user_input11' not in st.session_state:
            st.session_state.user_input11 = ""

        if 'user_input12' not in st.session_state:
            st.session_state.user_input12 = ""

        if 'user_input13' not in st.session_state:
            st.session_state.user_input13 = ""

        if 'user_input14' not in st.session_state:
            st.session_state.user_input14 = ""

        st.session_state.user_input10 = res[0] # chr_name
        st.session_state.user_input11 = res[1] # car_num
        st.session_state.user_input12 = res[4] # name
        st.session_state.user_input13 = res[3] # ph_num
        st.session_state.user_input14 = res[2] # res_time
        
        nav_page("myres_chg")
with col6 :
    if st.button("처음으로") :
        nav_page("home")
