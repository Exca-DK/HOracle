

from __future__ import annotations
from abc import abstractmethod
from enum import Enum
from typing import Dict

from .worker import Worker
from ..buffer import Buffer
from ..events.event import Event
from ..serialization.interface import ISeralizable
from ..net.endpoint import EndpointSet, EndpointType


from ..logging.logger import GetLogger
logger = GetLogger(__name__)


class NetWorker(Worker):


    def __init__(self) -> None:
        super().__init__()
        self.__Endpoints: Dict[Enum, EndpointSet] = {}
        self.buffer = Buffer(0)

    def AddEndpointSet(self, set: EndpointSet, under: Enum):
        lock = self.GetLock()
        with lock:
            self.__Endpoints[under] = set

    def GetEndpointSet(self, under: Enum) -> EndpointSet | None:
        if under not in self.__Endpoints:
            return None
        return self.__Endpoints[under]

    def OnStart(self):
        while True:
            if self.ShouldStop():
                break
            ev = self.GetEvent()
            serializable, under, etype = self.OnEvent(ev)
            self.buffer.Append((serializable, under, etype))
            
            #TODO Make a schedular instead of instantly sending
            self.SendAvaiable()

    def Cleanup(self):
        pass
    

    @abstractmethod
    def OnEvent(self, item: Event) -> ISeralizable & Enum & EndpointType:
        pass

    @abstractmethod
    def SendAvaiable(self):
        pass