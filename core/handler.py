from __future__ import annotations
from ast import Param
from queue import Queue
from typing import Dict, List, Tuple
from uuid import UUID

from .hwrappers.hip import Hip

from .hwrappers.node import NativeNode, NewWrappedNode
from .events.types import HEvent
from .exceptions.base import EmptyListeners
from .listeners.listener import BaseListener
from .render.render import IsRenderNode, ApplyRenderScriptMetrics


from .logging.logger import GetLogger
logger = GetLogger(__name__)

__callbacks__: Dict[HEvent, List[HEvent]] = {}
__callbacks__[HEvent.ChildCreated] = [HEvent.ChildCreated, HEvent.ParmTupleChanged, HEvent.BeingDeleted]


def HEventNodeConverter(foo):

    """Wraps the native houdini callbacks into EventHandler callback method"""
    def wrapper(*args, **kwargs):
        etype = kwargs.pop("event_type", HEvent.Default)
        node = kwargs.pop("node", None)
        if len(args) > 1:
            _self, _args = args
            foo(_self, HEvent(etype), node, *_args, **kwargs)
        else:
            foo(*args, HEvent(etype), node, **kwargs)

    return wrapper


class HandlerRegistry:
    def __init__(self, channel: Queue) -> None:
        self.__registry__: Dict[HEvent, Dict[UUID, BaseListener]] = {}
        self.channel = channel

    def RegisterListener(self, listener: BaseListener):      
        topic = listener.GetTopic()
        lid = listener.GetId()
        if topic not in self.__registry__:
            self.__registry__[topic] = {}
        if lid in self.__registry__[topic]:
            logger.warning(f"Listener: Id-{lid}, Type: {listener.__class__.__name__} already active under {topic}")
            return
        
        self.__registry__[topic][lid] = listener
        listener.SetChannel(self.channel)
        logger.debug(f"Registered Listener: Id-{lid}, type: {listener.__class__.__name__} under {topic}")


    def RemoveListener(self, topic: HEvent, ListenerId: UUID):
        if topic not in self.__registry__:
            return
        if ListenerId not in self.__registry__[topic]:
            return
        self.__registry__[topic].pop(ListenerId)

    def NotifyListeners(self, event: HEvent, *args, **kwargs):
        if event.name not in self.__registry__:
            logger.debug(EmptyListeners(event))
            return False

        for listener in self.__registry__[event.name].values():
            listener.Recv(*args, **kwargs)



class EventHandler(object):

    def __init__(self, registry: HandlerRegistry) -> None:
        self.__reg = registry
        global __handler__
        __handler__ = self

    def Notify(self, hevent: HEvent, *args, **kwargs):
        self.__reg.NotifyListeners(hevent, *args, **kwargs)

    @HEventNodeConverter
    def OnNodeEvent(self, etype: HEvent, node: NativeNode, *args, **kwargs):
        
        child: NativeNode = kwargs.get("child_node", None)
        if child is None and node is not None:
            wnode = NewWrappedNode(node)
        else:
            wnode = NewWrappedNode(child)
        self.Notify(etype, wnode, *args, **kwargs)
        
        if child is not None:  
            if IsRenderNode(child):
                ApplyRenderScriptMetrics(child)


            # preparam = child.parm("prerender")
            # tppreparam = child.parm("tprerender")
            # lppreparam = child.parm("lprerender")

            # postparam = child.parm("postrender")
            # tppostparam = child.parm("tpostrender")
            # lppostparam = child.parm("lpostrender")
            # if preparam is not None:
            #     try:
            #         tppreparam.set(True)
            #         lppreparam.set("python")
            #         preparam.set(GetRenderCallback(HEvent.RenderStart))

            #         tppostparam.set(True)
            #         lppostparam.set("python")
            #         postparam.set(GetRenderCallback(HEvent.RenderEnd))

            #     except Exception as e:
            #         print(e)


        if etype in __callbacks__:
            for event in __callbacks__[etype]:      
                self.RegisterNodeEvent(child, event)



    def RegisterNodeEvent(self, node: NativeNode, event: HEvent):
        node.addEventCallback((event.value,), self.OnNodeEvent)

    def RegisteSceneEvents(self, hip: Hip):
        def inner(event_type):
            ev = HEvent.Default
            try:
                ev = HEvent(event_type)
            except:
                pass
            self.Notify(ev)

        hip.addEventCallback(inner)

        


def IsHandlerCreated() -> bool:
    global __handler__
    return __handler__ is not None

def GetCachedHandler():
    global __handler__
    return __handler__


__handler__ = None