# import requests
# from dotenv import load_dotenv
# import os

# # .env 파일의 환경변수 로드

# load_dotenv()
# client_id=os.getenv("Client_ID")
# client_secret=os.getenv("Client_Secret")

# #api url
# url="https://openapi.naver.com/v1/search/local.json"

# query='화장실'


# #검색키워드


# headers={
#     'X-Naver-Client-Id': client_id,
#     'X-Naver-Client-Secret': client_secret
# }


# response=requests.get(url, headers=headers, 
#                       params={'query':query}
#                       )


# if response.status_code==200:
#     data=response.json()
#     print(data)


# import requests
# from dotenv import load_dotenv
# import os

# # .env 파일의 환경변수 로드
# load_dotenv()
# client_id = os.getenv("Client_ID")
# client_secret = os.getenv("Client_Secret")

# # 네이버 검색 API URL
# url = "https://openapi.naver.com/v1/search/local.json"

# # 검색 키워드 및 위치 기반 검색 매개변수
# query = "화장실"  # 검색 키워드
# latitude = 37.5665  # 중심 위도 (예: 서울 시청)
# longitude = 126.9780  # 중심 경도
# radius = 500  # 검색 반경 (미터 단위, 최대 10,000m)

# # 요청 헤더
# headers = {
#     'X-Naver-Client-Id': client_id,
#     'X-Naver-Client-Secret': client_secret
# }

# # 요청 매개변수
# params = {
#     'query': query,
#     'display': 5,  # 최대 5개 결과
#     'start': 1,  # 결과 시작점
#     'sort': 'random',  # 정렬 방식 (random: 랜덤, comment: 리뷰 순)
#     'coordinate': f"{longitude},{latitude}",  # 위경도 입력 (경도,위도 순서)
#     'radius': radius  # 반경 설정 (미터 단위)
# }

# # API 요청
# response = requests.get(url, headers=headers, params=params)

# # 결과 확인
# if response.status_code == 200:
#     data = response.json()
#     for item in data.get('items', []):
#         print(f"제목: {item['title']}")
#         print(f"주소: {item['address']}")
#         print(f"도로명 주소: {item['roadAddress']}")
#         print(f"카테고리: {item['category']}")
#         print(f"위도: {item['mapy']}, 경도: {item['mapx']}")
#         print('-' * 50)
# else:
#     print(f"API 요청 실패: {response.status_code}")
#     print(response.text)




#터미널창에 정보뜨는거 확인 but 내기준이 아님, 시청기준으로가져오게됨
#gpt모듈로 내 주변 화장실 검색어로 가져오기

import requests
from dotenv import load_dotenv
import os

# .env 파일 로드
load_dotenv()
client_id = os.getenv("Client_ID")
client_secret = os.getenv("Client_Secret")

import gps

#gps모듈은 하드웨어가 필요하다

def get_gps_location():
    # GPS 연결
    session = gps.gps(mode=gps.WATCH_ENABLE)
    while True:
        report = session.next()
        if report['class'] == 'TPV':
            return report.lat, report.lon
 
try:
    latitude, longitude = get_gps_location()  #gps는 못가져오지
    print(f"현재 위치: 위도={latitude}, 경도={longitude}")
except Exception as e:
    print("GPS 데이터를 가져오는 중 오류 발생:", e)


# 네트워크 기반 현재 위치 가져오기 #ip기반으로 가져오기
def get_current_location():
    response = requests.get("https://ipinfo.io")
    if response.status_code == 200:
        data = response.json()
        location = data["loc"].split(",")  # "37.5665,126.9780"
        latitude, longitude = float(location[0]), float(location[1])
        return latitude, longitude
    else:
        raise Exception("현재 위치를 가져올 수 없습니다.")

# 네이버 검색 API 호출
def search_nearby(latitude, longitude, query="화장실", radius=1000):
    url = "https://openapi.naver.com/v1/search/local.json"
    headers = {
        'X-Naver-Client-Id': client_id,
        'X-Naver-Client-Secret': client_secret
    }
    params = {
        'query': query,
        'display': 5,
        'sort': 'random',
        'coordinate': f"{longitude},{latitude}",
        'radius': radius
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API 요청 실패: {response.status_code}, {response.text}")


# 실행
try:
    # 현재 위치 가져오기
    latitude, longitude = get_current_location()
    print(f"현재 위치: 위도={latitude}, 경도={longitude}")

    # 네이버 API로 검색
    results = search_nearby(latitude, longitude)
    for item in results.get('items', []):
        title = item.get('title', '').replace('<b>', '').replace('</b>', '')
        address = item.get('address', '주소 정보 없음')
        road_address = item.get('roadAddress', '도로명 주소 없음')
        print(f"이름: {title}, 주소: {address}, 도로명 주소: {road_address}")
except Exception as e:
    print(e)




# #컴퓨터 ip주소로 현재위치 특정하기
# #
# import requests

# def get_location_by_ip():
#     try:
#         response = requests.get("https://ipinfo.io")
#         if response.status_code == 200:
#             data = response.json()
#             location = data["loc"].split(",")  # "위도,경도" 형식
#             latitude = float(location[0])
#             longitude = float(location[1])
#             return latitude, longitude
#         else:
#             raise Exception(f"IP 기반 위치 요청 실패: {response.status_code}")
#     except Exception as e:
#         print(f"위치 가져오기 오류: {e}")
#         return None, None

# # 실행 예제
# latitude, longitude = get_location_by_ip()
# if latitude and longitude:
#     print(f"현재 위치: 위도={latitude}, 경도={longitude}")
# else:
#     print("현재 위치를 가져올 수 없습니다.")