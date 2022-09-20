from datetime import datetime


class Limiter:

    def __init__(self, limit: int, time: int) -> None:
        self._limit = limit
        self._time = time
        self._tokens = limit
        self._last = datetime.utcnow()

    def WaitN(self, n: int):
        if n > self._limit:
            raise Exception("...")
        
        if self._tokens < n:
            self.Reserve(n)

    def Reserve(self, n):
        pass