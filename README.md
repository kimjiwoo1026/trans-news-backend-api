# trans-news-backend-api
키워드 기반 뉴스 검색과 기사 본문 크롤링/요약, 한↔영 번역을 하나의 FastAPI 앱으로 통합한 프로젝트

# 구조

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
