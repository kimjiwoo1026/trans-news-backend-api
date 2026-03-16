import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import news_router, summary_router, pipeline_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

app = FastAPI(title="TransNews API Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(news_router.router, prefix="/api/v1")
app.include_router(summary_router.router, prefix="/api/v1")
app.include_router(pipeline_router.router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    logger.info("TransNews Backend Server Started Successfully")