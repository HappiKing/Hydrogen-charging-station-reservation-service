import socket
import requests
import pandas as pd
import json
import base64
import pymysql

def check_availability(cursor, chr_name, res_time, name):
    # 충전소 이름과 예약 시간이 동시에 중복인지 확인
    cursor.execute('SELECT * FROM reservation_info WHERE chr_name = %s AND res_time = %s', (chr_name, res_time))
    result = cursor.fetchone()
    if result is not None:
        # 중복된 예약이 있으면 예약 불가능
        return False

    # 같은 이름과 같은 시간 중복인지 확인
    cursor.execute('SELECT * FROM reservation_info WHERE name = %s AND res_time = %s', (name, res_time))
    result_name = cursor.fetchone()
    if result_name is not None:
        # 중복된 이름이 있으면 예약 불가능
        return False

    # 중복된 예약이 없으면 예약 가능
    return True

def find_reservation(cursor, car_num, name, ph_num):
    cursor.execute('SELECT * FROM reservation_info WHERE car_num = %s AND name = %s AND ph_num = %s', (car_num, name, ph_num))
    result = cursor.fetchall()
    return result

def delete_reservation(cursor, chr_name, name, res_time):
    cursor.execute('DELETE FROM reservation_info WHERE chr_name = %s AND name = %s AND res_time = %s', (chr_name, name, res_time))

def change_reservation(cursor, new_res_time, name, res_time, chr_name):
    cursor.execute('update reservation_info set res_time =%s where name = %s AND res_time = %s AND chr_name = %s', (new_res_time, name, res_time, chr_name))
    result = cursor.fetchone()
    if result is not None:
        # 중복된 예약이 있으면 예약 불가능
        return False
    # 중복된 예약이 없으면 예약 가능
    return True

# 서버 설정 및 소켓 초기화
PORT = 2500
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(("localhost", PORT))
serverSocket.listen(5)

while True :
    # 클라이언트 연결 대기 및 수락
    clientSocket, addr = serverSocket.accept()
    # print(f"Connection from {addr}")

    # 클라이언트로부터 요청 받기
    request_code = clientSocket.recv(1024).decode('utf-8').strip()
    print(f"클라이언트로부터 받은 데이터: {request_code}")


    # API 전체 값(json) 반환
    def get_res():
        api_url = "http://el.h2nbiz.or.kr/api/chrstnList/currentInfo"
        key = "SX5s864WGPvPk7u18GZ227L4wKvn2zkAdZi6D1M6DpmYGDHg2pSm6rbY9YCqQOAx"

        headers = {
            "Accept": "application/json",
            "Authorization": key
        }
        
        res = requests.get(api_url, headers=headers)
        res = res.json()

        return res

    # 1~3번 요청에 대한 응답 처리
    if request_code == '1':
        temp = get_res()
        # JSON 형식의 데이터를 문자열로 변환
        json_data_str = json.dumps(temp)

        # 문자열을 바이트로 인코딩
        json_data_bytes = json_data_str.encode('utf-8')
        clientSocket.send(json_data_bytes)

        
    elif request_code == '2':
        excel_file_path = '/Users/hb/Desktop/Team_project/code/data.xlsx'

        # 엑셀 파일 읽기
        data = pd.read_excel(excel_file_path)
        json_data = data.to_json(orient='records', force_ascii=False)
        json_data_str = json.dumps(json_data)
        # 문자열을 바이트로 인코딩
        json_data_bytes = json_data_str.encode('utf-8')
        clientSocket.send(json_data_bytes)

    
    else :
        # base64 디코딩디코딩
        decoded_data = base64.b64decode(request_code)

        # 디코딩된 데이터를 JSON 문자열로 변환
        json_str = decoded_data.decode('utf-8')

        # 작은따옴표를 큰따옴표로 변경
        json_str_fixed = json_str.replace("'", '"')

        # JSON 문자열을 파이썬 딕셔너리로 로드
        json_data = json.loads(json_str_fixed)

        # print(json_data)
        if json_data :
            print("입력되었습니다")

        if 'chr_name' in json_data :
            if 'ph_num' in json_data :
                if 'old_res_time' in json_data :
                    print("예약 변경")

                    try:
                        db = pymysql.connect(host="localhost", user="root", password="rhtn1720", charset="utf8")
                        cursor = db.cursor(pymysql.cursors.DictCursor)

                        cursor.execute('USE reservation;')

                        chr_name = json_data['chr_name']
                        name = json_data['name']
                        res_time = json_data['old_res_time']
                        new_res_time = json_data['new_res_time']
                        
                        if change_reservation(cursor, new_res_time, name, res_time, chr_name):
                            
                            clientSocket.send(b'1')
                        else:
                            clientSocket.send(b'0')

                        cursor.execute('SELECT * FROM reservation_info;')

                        db.commit()
                    finally:
                        db.close()




                    
                else :
                    print("예약하기")
                    chr_name = json_data['chr_name']
                    car_num = json_data['car_num']
                    name = json_data['name']
                    ph_num = json_data['ph_num']
                    res_time = json_data['res_time']

                    try:
                        db = pymysql.connect(host="localhost", user="root", password="rhtn1720", charset="utf8")
                        cursor = db.cursor(pymysql.cursors.DictCursor)

                        cursor.execute('USE reservation;')


                        if check_availability(cursor, chr_name, res_time, name):
                            cursor.execute('INSERT INTO reservation_info (chr_name, car_num, name, ph_num, res_time) VALUES (%s, %s, %s, %s, %s)',
                                        (chr_name, car_num, name, ph_num, res_time))
                            clientSocket.send(b'1')
                        else:
                            clientSocket.send(b'0')

                        cursor.execute('SELECT * FROM reservation_info;')
                        value = cursor.fetchall()
                        print(value)

                        db.commit()
                    finally:
                        db.close()
            
            else :
                print("삭제하기")
                try:
                    db = pymysql.connect(host="localhost", user="root", password="rhtn1720", charset="utf8")
                    cursor = db.cursor(pymysql.cursors.DictCursor)

                    cursor.execute('USE reservation;')

                    chr_name = json_data['chr_name']
                    car_num = json_data['car_num']
                    res_time = json_data['res_time']
                    
                    print("삭제 전 예약 정보 조회:")
                    select_query = 'SELECT * FROM reservation_info WHERE chr_name = %s AND name = %s AND res_time = %s'
                    cursor.execute(select_query, (chr_name, name, res_time))
                    before_delete_reservations = cursor.fetchall()
                    print(before_delete_reservations)

                    # 예약 정보 삭제
                    delete_reservation(cursor, chr_name, name, res_time)
                    print("예약 정보를 삭제했습니다.")

                    db.commit()
                finally:
                    db.close()

        else :
            car_num = json_data['car_num']
            name = json_data['name']
            ph_num = json_data['ph_num']

            print("예약 정보 확인")

            try:
                db = pymysql.connect(host="localhost", user="root", password="rhtn1720", charset="utf8")
                cursor = db.cursor(pymysql.cursors.DictCursor)

                cursor.execute('USE reservation;')


                cursor.execute('SELECT * FROM reservation_info;')

                # 예약 정보 확인
                found_reservations = find_reservation(cursor, car_num, name, ph_num)
                
                data = str(found_reservations)
                # [를 "로, ]를 "로 변환
                data = data.replace('[', '"').replace(']', '"')
                binary_data = data.encode('unicode-escape')
                clientSocket.send(binary_data)

                db.commit()
            finally:
                db.close()


    # 소켓 닫기
    clientSocket.close()
