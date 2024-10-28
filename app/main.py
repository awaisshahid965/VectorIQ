from fastapi import FastAPI
from app.controllers.chat import router as chat_router

app = FastAPI()

@app.get('/')
def index():
    return "app is running..."

def create_app():

    app.include_router(chat_router)

    return app

app = create_app()
