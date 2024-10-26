# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_restx import Api, Resource, fields
from groq import Groq
import os
app = Flask(__name__)

# 리액트와 통신 설정
CORS(app)

# groq api key
client = Groq(
    api_key = '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'
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

        try:
            # OpenAI API 호출
            response = client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content" : user_message
                        }
                    ],
                    model = 'llama3-8b-8192',
            )
            print(response)

            # GPT 응답 가져오기
            ai_response = response.choices[0].message.content
        except Exception as e:
            print("Error:", e)  # 서버 콘솔에 에러 출력
            ai_response = "죄송합니다, 서버에 문제가 발생했습니다."

        return jsonify({"response": ai_response})

if __name__ == "__main__":
    app.run(debug=True)
