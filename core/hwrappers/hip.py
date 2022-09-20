from __future__ import annotations
from ..exceptions.base import Forbidden

import hou

class Hip:

    def path() -> str:
        pass

    def __new__(cls):
        raise Forbidden(Hip.__name__)

def GetCurrentHip() -> hou.hipFile:
    return hou.hipFile

def GetCurrentHipPath(hip: hou.hipFile = None) -> str:
    if hip is None:
        return GetCurrentHip().path()
    return hip.path()