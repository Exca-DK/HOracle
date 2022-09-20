
from abc import ABC, abstractmethod
from threading import Thread, Event as TEvent, Lock
from queue import Queue
from uuid import uuid4

from ..events.event import Event

from ..logging.logger import GetLogger
logger = GetLogger(__name__)


class Worker(ABC):

    def __init__(self) -> None:
        self.__mu = Lock()
        self.__running = False
        self.__started = TEvent()
        self.__canceled = TEvent()
        self.__queue = Queue()
        self.__id = uuid4()
        self.__th = None

    def Start(self):
        th = Thread(target=self.__Entry)
        self.__th = th
        th.start()
        self.__started.wait()

    def GetChannel(self) -> Queue:
        return self.__queue

    def GetEvent(self) -> Event:
        return self.__queue.get()

    def GetId(self) -> Queue:
        return self.__id

    def GetLock(self) -> Lock:
        return self.__mu

    def IsRunning(self) -> bool:
        self.__mu.acquire()
        running = self.__running
        self.__mu.release()
        return running

    def Stop(self):
        if self.IsRunning():
            logger.warn(f"Thread: {self.__id} is not running")
            return
        self.__canceled.set()
        self.__th.join()

    def ShouldStop(self) -> bool:
        return self.__canceled.isSet()
            
    def __Entry(self):
        self.__started.set()
        self.__running = True
        prefix = f"Worker: {self.GetId()}"
        logger.debug(f"{prefix} started")
        self.OnStart()
        logger.debug(f"{prefix} cleaning up")
        self.Cleanup()
        logger.debug(f"{prefix} stopped")

    @abstractmethod
    def OnStart(self):
        pass
    
    @abstractmethod
    def Cleanup(self):
        pass