from fastapi import FastAPI
from routers import router
from database import Base, engine

app = FastAPI(title="Order Service")

Base.metadata.create_all(bind=engine)

app.include_router(router)