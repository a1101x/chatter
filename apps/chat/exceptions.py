class ClientError(Exception):
    """
    Custom exception for the websocket receive().
    """
    def __init__(self, code):
        super().__init__(code)
        self.code = code
