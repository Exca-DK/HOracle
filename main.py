from .core.config import config
from .core.worker import ViewportWorker, HTTPworker
from .core.listeners.factory import ListenerFactory
from .core.handler import EventHandler, HEvent, HandlerRegistry, IsHandlerCreated
from .core.logging.logger import SetLoggingLevel, GetLogger
from .core.logging.types import LoggingLevel
from .core.net.endpoint import CreateEndpointSet
from .core.hwrappers.hip import GetCurrentHip

from .core.events.types import HEvent
from .core.handler import GetCachedHandler, NewWrappedNode
from .core.hwrappers.node import NativeNode


logger = GetLogger(__name__)

from hou import node


def RenderMetrics(node: NativeNode, eventType: HEvent, frame: int = None):
    handler = GetCachedHandler()
    if handler is None:
        logger.critical("Handler null", exc_info=1)
    handler.Notify(HEvent.RenderActivity, NewWrappedNode(node), _type=eventType, _frame=frame)

def PreRender(node: NativeNode, frame: int):
    RenderMetrics(node, HEvent.RenderStart, frame)

def PostRender(node: NativeNode, frame: int):
    RenderMetrics(node, HEvent.RenderEnd, frame)

def PreFrame(node: NativeNode, frame: int):
    RenderMetrics(node, HEvent.FrameStart, frame)

def PostFrame(node: NativeNode, frame: int):
    RenderMetrics(node, HEvent.FrameEnd, frame)

def main():
    
    if IsHandlerCreated():
        logger.debug("handler already exists")
        return

    config.LoadConfig()
    SetLoggingLevel(config.GetVerbosity())
   
    httpWorker = HTTPworker()
    registry = HandlerRegistry(httpWorker.GetChannel())
    for ep in config.GetEndpoints():
        endpoint = CreateEndpointSet(ep.endpoint)
        logger.debug(f"creating epset {ep.endpoint} for {ep.type}")
        httpWorker.AddEndpointSet(endpoint, ep.type)
        try:
            listener = ListenerFactory.CreateListener(ep.type)
            registry.RegisterListener(listener)
        except Exception as e:
            logger.debug(e.args)
        
    httpWorker.Start()

    viewportWorker = ViewportWorker(5)
    viewportWorker.SetEventChannel(httpWorker.GetChannel())
    viewportWorker.Start()

    handler = EventHandler(registry)

    for context in config.GetContexts():
        n = node(context)
        if n is None:
            continue
        handler.RegisterNodeEvent(n, HEvent.ChildCreated)

    handler.RegisteSceneEvents(GetCurrentHip())




    