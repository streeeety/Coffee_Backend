from fastapi import FastAPI
from database import Base, engine
from routers import router

app = FastAPI(title="Auth Service")

# создаём таблицы
Base.metadata.create_all(bind=engine)

# подключаем роутеры
app.include_router(router)