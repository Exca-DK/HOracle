
from ..events.types import HEvent
from ..hwrappers.node import NativeNode

from ..logging.logger import GetLogger
logger = GetLogger(__name__)

__PreRender__ = """from exca_pipeline import main
main.PreRender(hou.pwd(), hou.intFrame())"""

__PostRender__ = """from exca_pipeline import main 
main.PostRender(hou.pwd(), hou.intFrame())"""

__PreFrame__ = """from exca_pipeline import main
main.PreFrame(hou.pwd(), hou.intFrame())"""

__PostFrame__ = """from exca_pipeline import main 
main.PostFrame(hou.pwd(), hou.intFrame())"""

__types__ = {HEvent.RenderStart: __PreRender__,
HEvent.RenderEnd: __PostRender__,
HEvent.FrameStart: __PreFrame__,
HEvent.FrameEnd: __PostFrame__}

__params__ = {"prerender": HEvent.RenderStart, "postrender": HEvent.RenderEnd, "preframe": HEvent.FrameStart, "postframe": HEvent.FrameEnd}
__order__ = ["prerender", "postrender", "preframe", "postframe"]

def GetRenderCallback(hevent: HEvent):
    if hevent not in __types__:
        return None
    return __types__[hevent]

__options__ = [("t", True), ("l", "python"), ("", GetRenderCallback)]

def IsRenderNode(node: NativeNode) -> bool:
 
    result = node.parm(__order__[0])

    return result is not None

def ApplyRenderScriptMetrics(node: NativeNode):
   
    for ord in __order__:
        for prefix, tvalue in __options__:
            full = prefix+ord
            value = tvalue
            if full in __params__:
                value = tvalue(__params__[full])
                
            parm = node.parm(full)
            if parm is not None: 
                try:
                    parm.set(value)
                except Exception as e:
                    logger.warn(e)




