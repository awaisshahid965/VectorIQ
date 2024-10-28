from fastapi import FastAPI
from app.controllers.chat import router as chat_router

app = FastAPI()

@app.get('/')
def index():
    return "app is running..."

app.include_router(chat_router)
