class BaseDecodeException(Exception):
    def __init__(self, error: str):
        self._error = error

    @property
    def message(self):
        return self._error
