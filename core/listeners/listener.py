from __future__ import annotations
from abc import ABC, abstractmethod
from ctypes import Union
from dataclasses import dataclass
from datetime import datetime
from queue import Queue
from typing import Any, Dict, List, Tuple
from uuid import UUID

from ..serialization.interface import ISeralizable


from ..buffer import DeltaBuffer
from ..exceptions.base import ParamNotFound
from ..events.event import Event
from ..events.types import HEvent
from ..hwrappers.param import HParameter, Parameter
from ..hwrappers.node import WrappedNode
from ..hwrappers.hip import GetCurrentHipPath


from hou import Parm

from ..logging.logger import GetLogger
logger = GetLogger(__name__)

@dataclass
class ListenerError:
    error: str

@dataclass
class ListenerResult:
    Data: Dict
    Error: ListenerError = None


class BaseListener(ABC):

    Topic: HEvent

    def __init__(self, id: UUID) -> None:
        self._ID = id
        self._channel: Queue = None

    def SetChannel(self, channel: Queue):
        self._channel = channel

    def Send(self, result: ListenerResult, topic: HEvent):
        if self._channel is None:
            logger.warn(f"Can't send data: {result} to channel. Reason: Channel not specified")
            return
        
        if result.Error is None:
            self._channel.put_nowait((Event(result.Data), topic))
        else:
            self._channel.put_nowait((Event(result.Error), topic))

    def Recv(self, *args, **kwargs):
        handle = self.BeforeHandle(*args, **kwargs)
        if handle:
            logger.debug(f"{self.__class__.__name__} handles topic: {self.Topic}. Args: {args}, Kwargs: {kwargs}")
            result = self.Handle(*args, **kwargs)
            self.PostHandle(result)

    @abstractmethod
    def BeforeHandle(self, *args, **kwargs) -> bool:
        """Ran at the beginning of every event."""
        pass

    @abstractmethod
    def Handle(self, *args, **kwargs) -> List[ListenerResult]:
        pass

    @abstractmethod
    def PostHandle(self, results: List[ListenerResult]):
        pass

    def GetTopic(self):
        return self.Topic.name

    def GetId(self):
        return self._ID


class DeltaBufferedListener(BaseListener):

    def __init__(self, id: UUID, bufferSize: int) -> None:
         super().__init__(id)
         self._Buffer = DeltaBuffer(bufferSize)

    def AddToBuffer(self, value: Any):
        self._Buffer.Append(value)

    def GetAllOccurencies(self, stop: callable) -> List[Any]:
        stack = []
        while True:
            newest = self._Buffer.GetNewest()
            stack.append(newest)
            if stop(newest):
                logger.info(f"stack: {stack}")
                break
        return stack

    def _ShowBuffer(self):
        return f"{self._Buffer.Print()}"

    def GetDelta(self, filter: callable):
        return self._Buffer.GetDelta(filter)

class ChildCreatedListener(DeltaBufferedListener):

    Topic = HEvent.ChildCreated
    Threshold = 1000 #Ratelimiter in ms

    def __init__(self, id: UUID, bufferSize: int) -> None:
        super().__init__(id, bufferSize)      

    def BeforeHandle(self, node: WrappedNode, *args, **kwargs) -> bool:
        # pathFull: str = node.path()       
        # path: str = pathFull.rsplit("/")[0]
        # delta = self.GetDelta(lambda x: x in path)
        delta = self.GetDelta(lambda l: 1 == 1)
        self.AddToBuffer(None)
        total = (delta.seconds * 1000 + delta.microseconds/1000)

        if total < ParmTupleChangedListener.Threshold: 
            return False
        return True

    def Handle(self, node: WrappedNode, *args, **kwargs) -> ListenerResult:  
        lightNode = None
        try:
            lightNode = node.ToLightNode()
            if not lightNode.IsValid():
                return
        except Exception as e:
            return

        return ListenerResult({"node": lightNode})


    def PostHandle(self, result: ListenerResult):
        if not isinstance(result, ListenerResult):
            return
        if result is None:
            return

        self.Send(result, self.Topic) 

class BeingDeletedListener(DeltaBufferedListener):

    Topic = HEvent.BeingDeleted
    Threshold = 1000 #Ratelimiter in ms

    def __init__(self, id: UUID, bufferSize: int) -> None:
        super().__init__(id, bufferSize)         

    def BeforeHandle(self, *args, **kwargs) -> bool:
        delta = self.GetDelta(lambda l: 1 == 1)
        self.AddToBuffer(None)
        total = (delta.seconds * 1000 + delta.microseconds/1000)

        if total < ParmTupleChangedListener.Threshold: 
            return False
        return True

    def Handle(self, node: WrappedNode, *args, **kwargs) -> ListenerResult:  
        lightNode = None
        try:
            lightNode = node.ToLightNode()
            if not lightNode.IsValid():
                return
        except Exception as e:
            logger.warn(e)
            return

        return ListenerResult({"node": lightNode})


    def PostHandle(self, result: ListenerResult):
        if not isinstance(result, ListenerResult):
            return
        if result is None:
            return

        
        self.Send(result, self.Topic) 


class SceneSavedListener(BaseListener):

    Topic = HEvent.SceneSaved

    def __init__(self, id: UUID) -> None:
        super().__init__(id)      

    def BeforeHandle(self, *args, **kwargs) -> bool:
        return True

    def Handle(self) -> ListenerResult:
        path = GetCurrentHipPath()
  

        #No absolute path, too much of privacy issue
        file = path.rsplit("/")[-1]
        return ListenerResult({"file": file})


    def PostHandle(self, result: ListenerResult):
        if not isinstance(result, ListenerResult):
            return
        if result is None:
            return
        
        self.Send(result, self.Topic) 

class RenderFrame(ISeralizable):

    __slots__ = ("start", "end", "number", "marked")

    def __init__(self, number: int) -> None:
        self.number = number
        self.start: float = int(datetime.utcnow().timestamp())
        self.end: float = None
        self.marked = False
        

    def Finalize(self):
        self.end = int(datetime.utcnow().timestamp())

    def Deserialize(self) -> str:
        return {"number": self.number, "start": self.start, "end": self.end}

    @staticmethod
    def Serialize(serializedObject: str) -> ISeralizable:
        raise NotImplementedError(RenderFrame.__name__)


class RenderActivityParams(ISeralizable):
    __slots__ = ("start", "frames", "end")

    def __init__(self) -> None:  
        self.start: float = int(datetime.utcnow().timestamp())
        self.frames: Dict[str,RenderFrame] = {}
        self.end: float = None
        self.marked = False
        self.tframes = 0

    def AddFrame(self, frame: RenderFrame):
        self.frames[frame.number] = frame

    def Finalize(self):
        self.end = int(datetime.utcnow().timestamp())
        self.marked = True

    def MarkFrame(self, frame):
        if frame not in self.frames:
            return
        self.frames[frame].marked = True

    def PopMarked(self) -> RenderFrame | None:
        for key, frame in self.frames.items():
            if frame.marked:
                self.tframes += 1
                return self.frames.pop(key)


    def Deserialize(self) -> str:
        # frames = []
        # #TODO I imagine it not being sorted when running filecache in top network.
        # for frame in self.frames.values():
        #     frames.append(frame.Deserialize())

        return {"start": self.start, "frames": self.tframes, "end": self.end}

    @staticmethod
    def Serialize(serializedObject: str) -> ISeralizable:
        raise NotImplementedError(RenderActivityParams.__name__)
    

class RenderActivityListener(BaseListener):

    Topic = HEvent.RenderActivity

    def __init__(self, id: UUID, size: int) -> None:
        super().__init__(id)      
        self._Elem: Dict[str, RenderActivityParams] = {}

    def BeforeHandle(self, node: WrappedNode, *args, **kwargs) -> bool:
        pathFull: str = node.path()
        _type = kwargs.get("_type", None)
        frame = kwargs.get("_frame", 0)
        if _type == HEvent.RenderStart:
            self._Elem[pathFull] = RenderActivityParams()
        elif _type == HEvent.RenderEnd:
            self._Elem[pathFull].Finalize()
            self._Elem[pathFull].marked = True
            return True
        elif _type == HEvent.FrameStart:
            frames = self._Elem[pathFull].frames
            frames[frame] = RenderFrame(frame)
        elif _type == HEvent.FrameEnd:
            frames = self._Elem[pathFull].frames
            frames[frame].Finalize()
            self._Elem[pathFull].MarkFrame(frame)
            return True
        else:
            logger.warn(f"Unsupported render type. Type: {_type}. node: {node.ToLightNode()}")

        return False

    def Handle(self, node: WrappedNode, *args, **kwargs) -> ListenerResult:
        light = node.ToLightNode()
        params = self._Elem.get(light.path)   
        light = node.ToLightNode() 
        _type = 2
        if light.label != "rop_geometry":
            _type = 1
       
        if params.marked:
            self._Elem.pop(light.path)
        path = GetCurrentHipPath()
        file = path.rsplit("/")[-1]
        frame = params.PopMarked()
        if frame is None:
            return ListenerResult({"render": params,"t": _type, "scene": file})
        return ListenerResult({"frame": frame, "t": _type, "scene": file})
 

    def PostHandle(self, result: ListenerResult):
        if not isinstance(result, ListenerResult):
            return
        if result is None:
            return
        #TODO Render currently is used as file-cache interpreter. It might actually include render context too. 
        self.Send(result, self.Topic) 


class ParmTupleChangedListener(DeltaBufferedListener):

    Topic = HEvent.ParmTupleChanged
    Threshold = 1000 #Ratelimiter in ms


    def __init__(self, id: UUID, bufferSize: int) -> None:
        super().__init__(id, bufferSize)    

    def BeforeHandle(self, node: WrappedNode, *args, **kwargs) -> bool:
        pathFull: str = node.path()       
        path: str = pathFull.rsplit("/")[0]
        delta = self.GetDelta(lambda x: x in path)
        self.AddToBuffer(path)
        total = (delta.seconds * 1000 + delta.microseconds/1000)

        if total < ParmTupleChangedListener.Threshold: 
            return False
        return True
        

    def Handle(self, node: WrappedNode, *args, **kwargs) -> List[ListenerResult]:
        #When user creates an complex asset for example DOP network houdini will send many events instead of one creation event.
        #We ignore most of them because they weren't made by user in such case.
        results: List[ListenerResult] = []
        
        lightNode = None
        try:
            lightNode = node.ToLightNode()
            if not lightNode.IsValid():
                return
            if lightNode.name == "load_a_field":
                return
        except Exception as e:
            return

        try:
            params: Tuple[Parm] = kwargs.get("parm_tuple", None)
            if params is None:
                raise ParamNotFound(f"parm_tuple, Node: {lightNode}")
        except ParamNotFound as e:
            return

        hparms: List[HParameter] = []
        for param in params:
            try:
                name: str = param.name()
                # if name == "snippet":
                #     val = "....."
                # else:
                val: Union[str, int, float] = param.eval()
                
            except Exception as e:
                logger.error(f"Encountered error when evaluating param. Error: {e}")
            finally:
                if val is None or name is None:
                    results.append(ListenerResult(None, ListenerError(f"node: {lightNode} had invalid parameter")))
                else:
                    hparms.append(HParameter(name, val))

        d = {}
        if len(hparms) > 1:
            parameter = Parameter.FromHParams(hparms, lightNode)
            d["param"] =  parameter
        elif len(hparms):
            parameter = Parameter(hparms[0].Name, None, hparms[0].Value, lightNode)
            d["param"] =  parameter
        if len(d):
            results.append(ListenerResult(d, None))

        
        return results
        
    def PostHandle(self, results: List[ListenerResult]):
        if not isinstance(results, list):
            return

        
        for result in results:
            self.Send(result, self.Topic)  
        
__listeners__: Tuple[BaseListener] = (ParmTupleChangedListener, BeingDeletedListener, ChildCreatedListener)