from fastapi import FastAPI
from database import engine, Base
from routers import router
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Menu Service")

Base.metadata.create_all(bind=engine)

logger.info("Menu Service started")

app.include_router(router)