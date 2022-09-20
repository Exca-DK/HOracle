from uuid import uuid4

from .listener import *
from ..exceptions.base import ListenerNotImplemented, ListenerAlreadyExists

from ..logging.logger import GetLogger
logger = GetLogger(__name__)


class ListenerFactory:

    @staticmethod
    def CreateAllListeners():
        for listener in __listeners__:
            ListenerFactory.CreateListener(listener)

    @staticmethod
    def CreateListener(hevent: HEvent, **kwargs) -> BaseListener:
        def inner():
            def cmpr(a: HEvent, b: HEvent):
                return a.name == b.name

        
            if hevent.name in __listeners_factory__:
                raise ListenerAlreadyExists(hevent.name)

            uuid = uuid4()
            listener = None
            #TODO Implement all of the cases of HEvent and switch to state machine
            if cmpr(hevent, hevent.ParmTupleChanged):
                size = kwargs.get("buffer_size", 5)
                listener = ParmTupleChangedListener(uuid, size)
            elif cmpr(hevent, HEvent.BeingDeleted):    
                size = kwargs.get("buffer_size", 5) 
                listener = BeingDeletedListener(uuid, size)
            elif cmpr(hevent, HEvent.ChildCreated):   
                size = kwargs.get("buffer_size", 5) 
                listener = ChildCreatedListener(uuid, size)
            elif cmpr(hevent, HEvent.SceneSaved):    
                listener = SceneSavedListener(uuid)
            elif cmpr(hevent, HEvent.RenderActivity):    
                listener = RenderActivityListener(uuid, 0)
            else:
                raise ListenerNotImplemented(hevent)

            __listeners_factory__[listener.GetTopic()] = listener
            return listener
        try:
            return inner()
        except ListenerAlreadyExists as e:
            print(__listeners_factory__)
            return __listeners_factory__[hevent.name]


__listeners_factory__: Dict[str, bool] = {}