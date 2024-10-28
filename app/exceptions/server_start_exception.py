class ServerStartError(Exception):
    """Custom exception for server start failures."""
    def __init__(self, message):
        super().__init__(message)
