import streamlit as st
import streamlit_folium
from streamlit.components.v1 import html
from folium import Map, Marker, Popup, Icon
from pyparsing import empty
import pandas as pd
import re

# 클라이언트 통신에서 받아와야하는 정보
from api import get_res, get_point, get_able_book, nav_page

# 페이지 Layout 설정
st.set_page_config(layout="wide")

empty1,con1,empty2 = st.columns([0.1,0.7,0.1])

# 시군구 카테고리 선언
area0 = ["시/도 선택","서울","인천","대전","광주","대구","울산","부산","경기","강원특별자치도","충북","충남","전북","전남","경북","경남","제주특별자치도"]
area1 = ["시/군/구 선택", "강남구","강동구","강북구","강서구","관악구","광진구","구로구","금천구","노원구","도봉구","동대문구","동작구","마포구","서대문구","서초구","성동구","성북구","송파구","양천구","영등포구","용산구","은평구","종로구","중구","중랑구"]
area2 = ["시/군/구 선택", "계양구","남구","남동구","동구","부평구","서구","연수구","중구","강화군","옹진군"]
area3 = ["시/군/구 선택", "대덕구","동구","서구","유성구","중구"]
area4 = ["시/군/구 선택", "광산구","남구","동구", "북구","서구"]
area5 = ["시/군/구 선택", "남구","달서구","동구","북구","서구","수성구","중구","달성군"]
area6 = ["시/군/구 선택", "남구","동구","북구","중구","울주군"]
area7 = ["시/군/구 선택", "강서구","금정구","남구","동구","동래구","부산진구","북구","사상구","사하구","서구","수영구","연제구","영도구","중구","해운대구","기장군"]
area8 = ["시/군/구 선택", "고양시","과천시","광명시","광주시","구리시","군포시","김포시","남양주시","동두천시","부천시","성남시","수원시","시흥시","안산시","안성시","안양시","양주시","오산시","용인시","의왕시","의정부시","이천시","파주시","평택시","포천시","하남시","화성시","가평군","양평군","여주군","연천군"]
area9 = ["시/군/구 선택", '강릉시', '동해시', '삼척시', '속초시', '원주시', '춘천시', '태백시', '고성군', '양구군', '양양군', '영월군', '인제군', '정선군', '철원군', '평창군', '홍천군', '화천군', '횡성군']
area10 = ["시/군/구 선택", "제천시","청주시","충주시","괴산군","단양군","보은군","영동군","옥천군","음성군","증평군","진천군","청원군"]
area11 = ["시/군/구 선택", "계룡시","공주시","논산시","보령시","서산시","아산시","천안시","금산군","당진군","부여군","서천군","연기군","예산군","청양군","태안군","홍성군"]
area12 = ["시/군/구 선택", "군산시","김제시","남원시","익산시","전주시","정읍시","고창군","무주군","부안군","순창군","완주군","임실군","장수군","진안군"]
area13 = ["시/군/구 선택", "광양시","나주시","목포시","순천시","여수시","강진군","고흥군","곡성군","구례군","담양군","무안군","보성군","신안군","영광군","영암군","완도군","장성군","장흥군","진도군","함평군","해남군","화순군"]
area14 = ["시/군/구 선택", "경산시","경주시","구미시","김천시","문경시","상주시","안동시","영주시","영천시","포항시","고령군","군위군","봉화군","성주군","영덕군","영양군","예천군","울릉군","울진군","의성군","청도군","청송군","칠곡군"]
area15 = ["시/군/구 선택", "거제시","김해시","마산시","밀양시","사천시","양산시","진주시","진해시","창원시","통영시","거창군","고성군","남해군","산청군","의령군","창녕군","하동군","함안군","함양군","합천군"]
area16 = ["시/군/구 선택", "서귀포시","제주시"]

# 충전소 위치 정보 불러오기
df1 = pd.DataFrame(get_point()) # 위도, 경도, 주소 데이터 가져오기
df2 = pd.DataFrame(get_res(1))  # API 값 가져오기
df = pd.merge(df1, df2, on='chrstn_mno')

# 지역 선택
def sidebar_option() :
    # 시/도 입력
    sido = st.sidebar.selectbox('지역을 선택하세요.', (area0))
    
    # 시/군/구 입력
    if sido == "서울" :
        center = [37.5642135, 127.0016985]; m = Map(location=center, zoom_start=10) # 초기 지도 설정
        sigungu = st.sidebar.selectbox(' ', (area1))

    elif sido == "인천" :
        center = [37.45639, 126.70528]; m = Map(location=center, zoom_start=10) # 초기 지도 설정
        sigungu = st.sidebar.selectbox(' ', (area2))

    elif sido == "대전" :
        center = [36.35111, 127.38500]; m = Map(location=center, zoom_start=11) # 초기 지도 설정
        sigungu = st.sidebar.selectbox(' ', (area3))

    elif sido == "광주" :
        center = [35.15972, 126.85306]; m = Map(location=center, zoom_start=11) # 초기 지도 설정
        sigungu = st.sidebar.selectbox(' ', (area4))

    elif sido == "대구" :
        center = [35.87222, 128.60250]; m = Map(location=center, zoom_start=11) # 초기 지도 설정
        sigungu = st.sidebar.selectbox(' ', (area5))

    elif sido == "울산" :
        center = [35.53889, 129.31667]; m = Map(location=center, zoom_start=11) # 초기 지도 설정
        sigungu = st.sidebar.selectbox(' ', (area6))

    elif sido == "부산" :
        center = [35.17944, 129.07556]; m = Map(location=center, zoom_start=11) # 초기 지도 설정
        sigungu = st.sidebar.selectbox(' ', (area7))

    elif sido == "경기" :
        center = [37.42637222, 126.9898]; m = Map(location=center, zoom_start=10) # 초기 지도 설정
        sigungu = st.sidebar.selectbox(' ', (area8))

    elif sido == "강원특별자치도" :
        center = [37.541991, 128.543688]; m = Map(location=center, zoom_start=8) # 초기 지도 설정
        sigungu = st.sidebar.selectbox(' ', (area9))

    elif sido == "충북" :
        center = [36.628503, 127.929344]; m = Map(location=center, zoom_start=9) # 초기 지도 설정
        sigungu = st.sidebar.selectbox(' ', (area10))

    elif sido == "충남" :
        center = [36.557229, 126.779757]; m = Map(location=center, zoom_start=10) # 초기 지도 설정
        sigungu = st.sidebar.selectbox(' ', (area11))

    elif sido == "전북" :
        center = [35.716705, 127.144185]; m = Map(location=center, zoom_start=10) # 초기 지도 설정
        sigungu = st.sidebar.selectbox(' ', (area12))

    elif sido == "전남" :
        center = [34.819400, 126.893113]; m = Map(location=center, zoom_start=10) # 초기 지도 설정
        sigungu = st.sidebar.selectbox(' ', (area13))

    elif sido == "경북" :
        center = [36.248647, 128.664734]; m = Map(location=center, zoom_start=10) # 초기 지도 설정
        sigungu = st.sidebar.selectbox(' ', (area14))

    elif sido == "경남" :
        center = [35.259787, 128.664734]; m = Map(location=center, zoom_start=10) # 초기 지도 설정
        sigungu = st.sidebar.selectbox(' ', (area15))

    elif sido == "제주특별자치도" :
        center = [33.364805, 126.542671]; m = Map(location=center, zoom_start=10) # 초기 지도 설정
        sigungu = st.sidebar.selectbox(' ', (area16))

    else :
        # 중심 좌표 설정
        sigungu = None
        center = [36.34, 127.77] # 초기 중심 좌표
        m = Map(location=center, zoom_start=7) # 초기 지도 설정

    return center, m, sido, sigungu

# 충전소 위치 조회    
def search_chr(sido, sigungu, df) :
    if sido == '시/도 선택' and sigungu == '':
        pass
    elif sigungu =='시/군/구 선택' :
        pass
    elif sigungu == None :
        pass

    else :
        keyword = sido + " " + sigungu # 여기에 원하는 키워드를 입력하세요.
        filtered_df = df[df['address'].str.contains(keyword, case=False, na=False)]
        name_df = []
        for i in filtered_df["chrstn_nm_x"] :
            name_df.append(i)

        if (sigungu == "") or (sigungu == "시/군/구 선택") :
            pass
        
        else :   
            chr_sel = st.sidebar.selectbox('충전소 선택', (name_df))
            # chr_sel = st.sidebar.selectbox('충전소 선택', (filtered_df["chrstn_nm_x"]))
            return chr_sel

# sidebar에서 정보를 입력하고, 버튼을 클릭했을 때 페이지를 이동하기 위해
# 변수들을 전역 변수로 선언한다.

# 조회 할 시군구 정보 값 가져오기
center, m, sido, sigungu = sidebar_option()

# 예약 가능 시간 불러오기
time_term = get_able_book()

# 선택한 충전소 이름 가져오기
chr_sel = search_chr(sido, sigungu, df)

hide_navi = """
<style>
    /* Hide the sidebar navigation */
    [data-testid="stSidebarNav"] {
        display: none;
    }
    </style>
"""


# 메인 화면
def main_page() :

    st.markdown(hide_navi, unsafe_allow_html=True)

    # 왼쪽 여백
    with empty1 :
        empty()

    # 메인 화면
    with con1 :
        st.title("수소 충전소 예약 서비스")

        # 충전소 마커 옵션
        chr_view = st.sidebar.radio(
            "충전소 보기 옵션",
            ["전체 보기", "영업 중만 보기"],
            captions = ["전체 수소 충전소를 봅니다.", "현재 영업 중인 충전소만 봅니다."])

        # 가게 정보를 리스트로 저장 (위치, 가게명)
        stores = []
        for item in df[["chrstn_nm_x","latitude","longitude", "oper_sttus_nm", "oper_sttus_cd", "address"]].values.tolist() : # 충전소 명, 위도, 경도, 운영 정보(숫자), 운영정보(문자)
            stores.append({'location' : item[1:3], 'name' : item[0], 'oper_sttus_nm' : item[3], "oper_sttus_cd" : item[4], "address" : item[5]})


        # 마커와 팝업 생성
        if chr_view == '전체 보기':
            for store in stores:
                if (store['oper_sttus_cd'] == '30') : # 영업 중
                    icon = Icon(color='blue')  # 색상을 여기서 'blue'로 변경하세요.
                    marker = Marker(location=store['location'], icon=icon)
                    popup = Popup(store['name']+f"<br>주소 : {store['address']}<br>운영 상태 : {store['oper_sttus_nm']}",min_width=100, max_width=300,)
                    popup.add_to(marker)
                    marker.add_to(m)

                elif (store['oper_sttus_cd'] == '20') : # 영업 마감
                    icon = Icon(color='red')  # 색상을 여기서 'red'로 변경하세요.
                    marker = Marker(location=store['location'], icon=icon)
                    popup = Popup(store['name']+f"<br>주소 : {store['address']}<br>운영 상태 : {store['oper_sttus_nm']}",min_width=100, max_width=300,)
                    popup.add_to(marker)
                    marker.add_to(m)

                elif (store['oper_sttus_cd'] == '10') : # 영업 중지
                    icon = Icon(color='gray')  # 색상을 여기서 'gray'로 변경하세요.
                    marker = Marker(location=store['location'], icon=icon)
                    popup = Popup(store['name']+f"<br>주소 : {store['address']}<br>운영 상태 : {store['oper_sttus_nm']}",min_width=100, max_width=300,)
                    popup.add_to(marker)
                    marker.add_to(m)

        else:
            for store in stores:
                if (store['oper_sttus_cd'] == '30') : # 영업 중
                    icon = Icon(color='blue')  # 색상을 여기서 'blue'로 변경하세요.
                    marker = Marker(location=store['location'], icon=icon)
                    popup = Popup(store['name']+f"<br>주소 : {store['address']}<br>운영 상태 : {store['oper_sttus_nm']}",min_width=100, max_width=300,)
                    popup.add_to(marker)
                    marker.add_to(m)

        if sido == "시/도 선택" :
            st.sidebar.button("예약", disabled=True)

        elif sigungu == "시/군/구 선택" :
            st.sidebar.button("예약", disabled=True)

        else :
            # 필터링 된 충전소 목록 출력
            try : 
                keyword = re.escape(chr_sel)  # 여기에 원하는 키워드를 입력하세요.

                filtered_df_sttus = df[df['chrstn_nm_x'].str.contains(keyword, case=False, na=False)]
                status = int(filtered_df_sttus["oper_sttus_cd"])

                

                if status == 20 :
                    st.sidebar.button("예약", disabled=True)
                elif status == 30 :
                    if st.sidebar.button("예약", disabled=False):
                        # 예약 페이지에 선택한 충전소 값 전달
                        st.session_state.user_input = chr_sel
                        nav_page("reservation")
        
                else :
                    st.sidebar.button("예약", disabled=True)
                    
            except :
                pass
                
        # Streamlit에 지도 표시
        st_folium = streamlit_folium.st_folium(m, use_container_width=True, width=50, height=500)

        if sido == "시/도 선택" :
            pass

        elif sigungu == "시/군/구 선택" :
            pass
        else :
            filtered_df_chr = df[df['address'].str.contains(sido + " " + sigungu, case=False, na=False)]
            st.dataframe(filtered_df_chr[["chrstn_nm_x", "address", "oper_sttus_nm", "cnf_sttus_nm"]])
            
    # 오른쪽 여백
    with empty2 :
	    empty()


page_names_to_funcs = {
    "Main page": main_page,
}

# if st.button("예약", disabled=True) :
#     nav_page("book")

page_names_to_funcs["Main page"]()

