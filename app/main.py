from fastapi import FastAPI
from routers.news_router import router as news_router
from routers.summary_router import router as summary_router
from routers.pipeline_router import router as pipeline_router

app = FastAPI(title="TransNews Backend API")

app.include_router(news_router, prefix="/api")
app.include_router(summary_router, prefix="/api")
app.include_router(pipeline_router, prefix="/api")