from dotenv import load_dotenv; load_dotenv()
from app.config.app import App

if __name__ == "__main__":
    App.init_server()
