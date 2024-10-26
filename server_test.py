import requests

# Flask 서버 IP와 포트를 설정 (예: 210.121.241.202:5000)
url = "http://172.31.99.234:5001/run"

try:
    # GET 요청 보내기
    response = requests.get(url)

    # 응답 코드 확인 및 데이터 출력
    if response.status_code == 200:
        print("응답 데이터:", response.json())  # JSON 응답 출력
    else:
        print(f"Error: 응답 코드 {response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"요청 실패: {e}")
