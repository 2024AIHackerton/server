# app.py
from flask import Flask
from flask_cors import CORS
from flask_restx import Api, Resource

app = Flask(__name__)

# 리액트와 통신 설정
CORS(app)

# flask swagger UI 설정
api = Api(app, version='1.0', title='API 문서', description='Swagger 문서', doc="/api-docs")

# namespace 설정
get_test_api = api.namespace('test', description='GET Test API')

@get_test_api.route('/')
class Test(Resource):
    def get(self):
        return 'Hello World!'

# namespace 설정
json_test_api = api.namespace('JSON', description='GET JSON Test API')

@json_test_api.route("/data")
class JSONTest(Resource):
    def get(self):
        data = {"message": "Hello from Flask!"}
        return data  # jsonify 사용하지 않음

if __name__ == "__main__":
    app.run(debug=True)
