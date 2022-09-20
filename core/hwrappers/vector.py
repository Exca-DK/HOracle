from __future__ import annotations

from ..exceptions.base import Forbidden

import hou


class Vector3(hou.Vector3):

    def __new__(cls: type):
        raise Forbidden(Vector3.__name__)

def MergeVectorCoords(vector: Vector3) -> float:
    x = vector.x
    y = vector.y
    z = vector.z

    return x + y + z
    
def CompareVectors(vectorA: Vector3, vectorB: Vector3) -> float:
    a = MergeVectorCoords(vectorA)
    b = MergeVectorCoords(vectorB)
    return a - b

def IsCopy(source: Vector3, target: Vector3) -> bool:
    diff = CompareVectors(source, target)
    if abs(diff) < 0.01:
        return True
    return False
