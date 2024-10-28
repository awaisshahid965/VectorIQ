from dotenv import load_dotenv
from app.config.app import App

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    App.init_server()
