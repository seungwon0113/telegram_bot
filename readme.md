# 텔레그램 일정 관리 봇 🤖

<div align="center">
  
[![Python](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-blue.svg)](https://core.telegram.org/bots/api)
[![SQLite](https://img.shields.io/badge/SQLite-3-blue.svg)](https://www.sqlite.org/)

텔레그램을 통해 간편하게 일정을 관리할 수 있는 봇입니다.

</div>

## 📁 프로젝트 구조
```
├── bot.py          # 텔레그램 봇 실행 및 핸들러
├── service.py      # 비즈니스 로직
├── database.py     # 데이터베이스 관리
└── .env           # 환경 변수

```

## 🛠 기술 스택

### 언어 및 프레임워크
- [![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
- [![Telegram](https://img.shields.io/badge/Telegram-Bot_API-26A5E4?style=flat&logo=telegram&logoColor=white)](https://core.telegram.org/bots/api)

### 데이터베이스
- [![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite&logoColor=white)](https://www.sqlite.org/)

### 도구 및 라이브러리
- [![python-telegram-bot](https://img.shields.io/badge/python--telegram--bot-latest-blue)](https://python-telegram-bot.org/)
- [![python-dotenv](https://img.shields.io/badge/python--dotenv-latest-brightgreen)](https://pypi.org/project/python-dotenv/)
- [![nest-asyncio](https://img.shields.io/badge/nest--asyncio-latest-yellowgreen)](https://pypi.org/project/nest-asyncio/)

## ✨ 주요 기능

### 명령어
| 명령어 | 설명 |
|--------|------|
| `/start` | 봇 시작 및 도움말 |
| `/add [날짜] [내용]` | 새로운 일정 추가 |
| `/list` | 등록된 일정 목록 보기 |
| `/delete [번호]` | 일정 삭제 |


<div align="center">
<h3>데모 화면</h3>
  <img src="image/demobot.gif"  width="250"/>

</div>

## 🚀 시작하기

### 설치 방법

1. 가상환경 생성 및 활성화
```bash
python -m venv .venv
source .venv/bin/activate  # Mac/Linux
```

2. 필요한 패키지 설치
```bash
pip install python-telegram-bot python-dotenv nest-asyncio
```

3. 환경변수 설정
`.env` 파일 생성:
```bash
TELEGRAM_TOKEN=your_bot_token_here
CHAT_ID=chat_id
```

### 실행 방법
```bash
python bot.py
```
