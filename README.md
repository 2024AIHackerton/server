# 🚀 Flask Server

![GitHub repo size](https://img.shields.io/github/repo-size/chyun7114/server)
![GitHub contributors](https://img.shields.io/github/contributors/chyun7114/server)
![GitHub stars](https://img.shields.io/github/stars/chyun7114/server?style=social)
![GitHub forks](https://img.shields.io/github/forks/chyun7114/server?style=social)

## 📌 프로젝트 개요
이 레포지토리는 Flask와 OpenAI를 활용한 간단한 챗봇 애플리케이션 개발을 다룹니다. 주된 기능은 아래와 같습니다:
- **Papago API** 연동
- Flask 기반 **챗봇 REST API**

## 🛠️ 주요 파일 구조
```plaintext
server/
├── .gitignore         # Git에 포함되지 않을 파일 정의
├── README.md          # 프로젝트 설명 파일
├── flask_init.py      # Flask 서버 코드
├── server_test.py     # 서버 테스트 코드
└── .idea/             # IDE 관련 설정 파일
```

## 🚀 사용 방법

### 1. 환경 설정
1. Python 3.8+ 설치
2. 프로젝트 디렉토리로 이동 후, 의존성 설치:
 ```bash
 pip install -r requirements.txt
 ```
   
### 2. 서버 실행
```bash
python flask_init.py
```
서버가 정상적으로 실행되면, 브라우저에서 [http://127.0.0.1:5000](http://127.0.0.1:5000)로 접속하세요.

## 📚 기술 스택
- **Backend:** Flask
- **사용 API:** Papago Translate API, OpenAI gpt 4.0

## 📂 향후 계획
- gpt 호출 속도 최적화
- 추가적인 프롬프트 엔지니어링
- Docker 컨테이너화 with this repository https://github.com/2024AIHackerton/chatbot

## 🧑‍💻 작성자
**윤창현**  
[GitHub Profile](https://github.com/chyun7114)
