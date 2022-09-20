from __future__ import annotations
from dataclasses import dataclass
from typing import Dict
from functools import partial

from ..exceptions.base import Forbidden
from ..serialization.interface import ISeralizable

from hou import Node

#TODO make a wrapper around Houdini native node

@dataclass
class LightNode(ISeralizable):
    name: str
    label: str
    path: str

    def IsValid(self):
        for val in self.__dict__.values():
            if not len(val):
                return False
        return True

    def Deserialize(self) -> str:
        return self.__dict__

    @staticmethod
    def Serialize(serializedObject: str) -> Node:
        raise NotImplemented()


class NativeNode(Node):

    def __new__(cls) -> None:
        raise Forbidden(f"{WrappedNode.__name__} instantion")

class WrappedNode(NativeNode):
    """Wrapping houdini native node for type hinting. The methods in this class are embedded into houdini node.
    This node raises Forbidden exception when instantiating.
    """

    def __new__(cls) -> None:
        raise Forbidden(f"{WrappedNode.__name__} instantion")

    def ToLightNode(self) -> LightNode:
        raise NotImplemented()

    def GetLabel(self) -> str:
        raise NotImplemented()

    def Deserialize(self) -> str:
        raise NotImplemented()

    @staticmethod
    def Serialize(serializedObject: str) -> Node:
        raise NotImplemented()

def NewWrappedNode(node: Node | NativeNode) -> WrappedNode:
    """Wraps the houdini native node into node used by this library. The new methods are embeded into this node instance."""
    def ToLightNode(self) -> Dict:
        name = self.name()
        label = self.type().name()
        path = self.path()
        return LightNode(name, label, path)

    def GetLabel(self) -> str:
        return self.type().name()

    setattr(node, ToLightNode.__name__, partial(ToLightNode, node))
    setattr(node, GetLabel.__name__, partial(GetLabel, node))
    return node