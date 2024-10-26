# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_restx import Api, Resource, fields
from groq import Groq
import yaml, requests
import urllib.request
import json
import re


from pyexpat.errors import messages

app = Flask(__name__)

# 리액트와 통신 설정
CORS(app)

# YAML 파일 읽기
yml_file = 'configuration.yaml'
with open(yml_file, 'r') as file:
    credentials = yaml.safe_load(file)

# 읽은 내용에서 각 항목을 변수로 추출
groq_secret_key = credentials['groq']['secret-key']
papago_client_id = credentials['papago']['client-id']
papago_client_secret = credentials['papago']['client-secret']

# groq api key
client = Groq(
    api_key = groq_secret_key
)
# flask swagger UI 설정
api = Api(app, version='1.0', title='API 문서', description='Swagger 문서', doc="/api-docs")

# namespace 설정

# 채팅 전달 api
chat_test_api = api.namespace('chat', description='CHAT API')

# Swagger 모델 정의 (사용자 입력을 위한)
chat_model = api.model('ChatModel', {
    'message': fields.String(required=True, description='사용자 입력 메시지')
})

@chat_test_api.route("/")
class ChatTest(Resource):
    @chat_test_api.expect(chat_model)  # 입력 모델 추가
    def post(self):
        # 사용자 메시지를 JSON 형식에서 추출
        user_message = api.payload.get('message')

        user_keyword = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content" : f'다음의 질문에서 키워드를 배열로 표현해줘 : {user_message}'
                }
            ],
            model = 'llama3-8b-8192'
        )
        
        
        user_text = user_keyword.choices[0].message.content

        # 배열 값 받고서
        # 키워드 => 날짜 값을 받고, ai model에 집어넣어서 예측값 df 받기
        # 받은 df json으로 변화하여, 라마에게 전달
        # 라마는 여기서 제일 높은 값이나 추천 가능한 품목들을 말하도록 조정
        keywords = get_keyword(user_text)
        can_translate = ['4월', 'April', 'april']
        if any(keyword in can_translate for keyword in keywords):
            try:
                date_param = '2020-04-30'
                params = {'date' : date_param}
                url = "http://172.31.99.234:5001/run"

                response = requests.get(url, params=params)

                ai_data = response.json()
                print(ai_data)

                # OpenAI API 호출
                response = client.chat.completions.create(
                        messages=[
                            {
                                "role": "user",
                                "content" : json.dumps(ai_data, ensure_ascii=False) +
                                            "다음 데이터를 보고 mean_current가 제일 높은 작물을 말해주고"
                                            + "그리고 작물 이름은 코드가 아닌 item_name으로 말해줘야 하고"
                                            + "mean_current는 price라 얘기해줘, 또 나온 item_name이 좋은 이유도 알려줘"
                            }
                        ],
                        model = 'llama3-8b-8192',
                )
                # GPT 응답 가져오기
                print(response.choices[0].message.content)
                ai_response = translate_to_kor(response.choices[0].message.content)
            except Exception as e:
                print("Error:", e)  # 서버 콘솔에 에러 출력
                ai_response = "서버에 문제 발생"
        else:
            ai_response = "다시 시도해 주세요"
        return jsonify({"response": ai_response})

def get_keyword(user_text):
    matches = re.findall(r'\[(.*?)\]', user_text)
    print(matches)

    if matches:
        keywords = [item.strip().strip('"').lower() for item in matches[0].split(',')]
        print(keywords)  # 결과: ['next month', 'crop prices']
        return keywords


def translate_to_kor(text):
    url = "https://naveropenapi.apigw.ntruss.com/nmt/v1/translation"

    encText = text
    data = f"source=en&target=ko&text={encText}"
    request = urllib.request.Request(url)
    request.add_header("X-NCP-APIGW-API-KEY-ID", papago_client_id)
    request.add_header("X-NCP-APIGW-API-KEY", papago_client_secret)

    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    response_body = response.read().decode('utf-8')

    rescode = response.getcode()
    print(response_body, rescode)
    if rescode == 200:
        # UTF-8로 디코딩하여 JSON 파싱

        parsed_data = json.loads(response_body)

        # translatedText 추출 (이스케이프 문자 그대로 유지)
        translated_text = parsed_data['message']['result']['translatedText']
        return translated_text
    else:
        print("Error Code:", rescode)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
