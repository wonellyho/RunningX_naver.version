from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()
client_id = os.getenv("Client_ID")
client_secret = os.getenv("Client_Secret")

app = Flask(__name__)
CORS(app)  # 모든 출처에서의 요청 허용

# 네이버 검색 API 호출 함수
def search_nearby(latitude, longitude, query="편의점", radius=1000):
    url = "https://openapi.naver.com/v1/search/local.json"
    headers = {
        'X-Naver-Client-Id': client_id,
        'X-Naver-Client-Secret': client_secret
    }
    params = {
        'query': query,
        'display': 5,
        'coordinate': f"{longitude},{latitude}",
        'radius': radius
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API 요청 실패: {response.status_code}, {response.text}")

# 기본 페이지 제공
@app.route("/", methods=["GET"])
def home():
    return send_file("now_location.html")

# POST 요청을 처리하여 검색 API 호출
@app.route("/search", methods=["POST"])
def search():
    data = request.get_json()
    latitude = data.get("latitude")
    longitude = data.get("longitude")

    try:
        results = search_nearby(latitude, longitude)
        for item in results.get("items", []):
            title = item.get("title", "").replace("<b>", "").replace("</b>", "")
            address = item.get("address", "주소 정보 없음")
            road_address = item.get("roadAddress", "도로명 주소 없음")
            print(f"이름: {title}, 주소: {address}, 도로명 주소: {road_address}")
        return jsonify(results.get("items", []))  # 브라우저로 결과 반환
    except Exception as e:
        print(f"오류 발생: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/favicon.ico")
def favicon():
    return send_file("favicon.ico")


if __name__ == "__main__":
    app.run(port=5000, debug=True)
