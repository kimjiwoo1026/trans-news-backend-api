# trans-news-backend-api
키워드 기반 뉴스 검색과 기사 본문 크롤링/요약, 한↔영 번역을 하나의 FastAPI 앱으로 통합한 프로젝트

## tech
-Python <br>
-FastAPI <br>
-Web Crawling <br>
-AI summarization



## 프로젝트 기능
뉴스 기사 크롤링 <br>
AI 기반 기사 요약 <br>
키워드 기반 뉴스 모니터링 <br>
PR/ 마케팅 팀을 위한 기사 분석 데이터 제공 <br>



## 구조

```
TransNews
│
├─ app
│   ├─ main.py
│   │
│   ├─ routers
│   │   ├─ article_router.py
│   │   ├─ summary_router.py
│   │   └─ search_router.py
│   │
│   ├─ services
│   │   ├─ crawler_service.py
│   │   ├─ summarizer_service.py
│   │   ├─ translate_service.py
│   │   ├─ rss_service.py
│   │   └─ search_service.py
│   │
│   ├─ schemas
│   │   └─ models.py
│   │
│   └─ config.py
│
├─ requirements.txt
├─ README.md
└─ .gitignore
```

## 설치
python -m venv .venv <br>
.venv\Scripts\activate <br>
pip install -r requirements.txt <br>


## 실행
vicorn app.main:app --reload --port 8000


## 접속
http://localhost:8000/docs
