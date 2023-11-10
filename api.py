import requests
import pandas as pd
from streamlit.components.v1 import html

# 페이지 이동 함수
def nav_page(page_name="book", timeout_secs=3):
    nav_script = """
        <script type="text/javascript">
            function attempt_nav_page(page_name, start_time, timeout_secs) {
                var links = window.parent.document.getElementsByTagName("a");
                for (var i = 0; i < links.length; i++) {
                    if (links[i].href.toLowerCase().endsWith("/" + page_name.toLowerCase())) {
                        links[i].click();
                        return;
                    }
                }
                var elasped = new Date() - start_time;
                if (elasped < timeout_secs * 1000) {
                    setTimeout(attempt_nav_page, 100, page_name, start_time, timeout_secs);
                } else {
                    alert("Unable to navigate to page '" + page_name + "' after " + timeout_secs + " second(s).");
                }
            }
            window.addEventListener("load", function() {
                attempt_nav_page("%s", new Date(), %d);
            });
        </script>
    """ % (page_name, timeout_secs)
    html(nav_script)



"""








여기다가 C언어 코드 삽입 예정








"""



# api 정보 받기
"""
<데이터 형식>
"chrstn_mno": "4311420121HS2020002",
"chrstn_nm": "충북 청주 도원수소충전소",
"tt_pressr": 600,
"prfect_elctc_posbl_alge" : 1
"wait_vhcle_alge": 1,
"cnf_sttus_cd" : "1" ,
"cnf_sttus_nm" : "여유"
"oper_sttus_cd": "30",
"oper_sttus_nm","운영중",
"pos_sttus_cd" : "0",
"pos_sttus_nm" : "영업중",
"last_mdfcn_dt": "20211214091233",
"send_dt": "2022-01-18"

-> 서버 측에서 api 호출 값(json)을 받아 올 예정
"""
def get_res(chrstn) : 

    api_url = "http://el.h2nbiz.or.kr/api/chrstnList/currentInfo"  # 대상 API 엔드포인트 URL을 입력
    key ="SX5s864WGPvPk7u18GZ227L4wKvn2zkAdZi6D1M6DpmYGDHg2pSm6rbY9YCqQOAx"

    headers = {
        "Accept" : "Application/json",
        "Authorization" : key
    }

    res = requests.get(api_url, headers=headers)
    res_temp = res.json()

    

    return res_temp

# 위치 정보 받기
"""
<데이터 형식>
chrstn_mno  	            chrstn_nm	                    latitude	        longitude	        address
1132020121HS2023024	        도봉수소충전소  	                37.69279146	        127.0443039	        서울 도봉구 도봉동 377
1150020121HS2022025	        E1 오곡 수소충전소	                37.55583165         126.7681832	        서울 강서구 오곡동 699-14
1150020121HS2022031	        서울 강서 공영차고지 버스 수소충전소     37.57778148	     126.7972008	     서울 강서구 개화동 663
1156020121HS2019014	        H국회수소충전소	                    37.5282036	        126.9151282	        서울 영등포구 여의도동 1

-> 서버 측에서 다음과 같은 형식으로 받아 올 예정
"""
def get_point() :
    df = pd.read_excel("/Users/hb/Desktop/Team project/code/data.xlsx")
    return df

# 예약 가능 정보 받기
"""
예약 가능 시간 데이터
-> 서버 측에서 예약 가능 시간을 받아 올 예정
"""
def get_able_book() :
    time_term = ["08:00", "08:20", "08:40", "09:00", "09:20", "09:40", "10:00", "10:20", "10:40", "11:00", "11:20", "11:40", "12:00", "12:20", "12:40", "13:00", "13:20", "13:40", "14:00", "14:20", "14:40", "15:00", "15:20", "15:40", "16:00", "16:20", "16:40", "17:00", "17:20", "17:40", "18:00"]

    return time_term

def send_res_val(chr , car_num, name, ph_num, res_time) :
    print(chr , car_num, name, ph_num, res_time)