import os
import uvicorn
from ..exceptions.server_start_exception import ServerStartError

from ..main import app

class App:
    
    @staticmethod
    def init_server():
        host = os.getenv('HOST', '')
        port = os.getenv('PORT', '')
        env = os.getenv('ENV', 'dev')

        try:
            port = int(port)  # Ensure port is an integer
        except ValueError:
            raise ServerStartError("Port must be an integer.")

        if not host or not port:
            raise ServerStartError("Failed to start server, either port or host is missing!\n")
        
        is_dev_mode = env == 'dev'

        uvicorn.run(
            app="app.main:app" if is_dev_mode else app,
            host=host,
            port=port,
            reload=is_dev_mode,
        )
        
        print(f"Server is running at {App._get_server_url(host, port)}")

    @staticmethod
    def _get_server_url(host, port):
        if port in [443, 80]:
            return f"http://{host}"
        return f"http://{host}:{port}"
