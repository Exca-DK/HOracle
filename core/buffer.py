from collections import deque
from datetime import  datetime, timedelta
from typing import Any, Callable

from .logging.logger import GetLogger
logger = GetLogger(__name__)

import hou

class Buffer:

    def __init__(self, size: int) -> None:
        if size == 0:
            self._storage = deque()
        else:
            self._storage = deque(maxlen=size)

        self._size = size

    def GetNewest(self) -> Any:
        if not len(self._storage):
            raise Exception("empty")
        return self._storage.pop()

    def GetOldest(self) -> Any:
        if not len(self._storage):
            raise Exception("empty")
        return self._storage.popleft()

    def IsEmpty(self):
        return len(self._storage) == 0

    def Append(self, item: any):
        self._storage.append(item)

    def Print(self):
        return f"{self._storage}"

class DeltaBuffer(Buffer):

    __deltaZero = datetime.utcnow() - datetime.utcnow()
    __deltaStart = datetime.utcnow()

    def __init__(self, size: int) -> None:
        if int == 0:
            self._storage = deque()
        else:
            self._storage = deque(maxlen=size)
        self._size = size

    def Append(self, item: any):
        super().Append((item, datetime.utcnow()))

    def GetDelta(self, filter: Callable) -> timedelta:
        stamps = []
        for item, timestamp in reversed(self._storage):
            try:
                if filter(item):
                    stamps.append(timestamp)
                    if len(stamps) > 1:
                        break
            except hou.ObjectWasDeleted:
                pass
            except Exception as e:
                logger.error(f"Error when filtering. Error: {e}")

        if len(stamps) > 1:
            return stamps[0] - stamps[1]
        return datetime.utcnow() - DeltaBuffer.__deltaStart




