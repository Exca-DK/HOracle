from __future__ import annotations
from ..exceptions.base import Forbidden

import hou


class Matrix4(hou.Matrix4):
    
    def __new__(cls: type):
        raise Forbidden(Matrix4.__name__)


def FlattenMatrix(matrix4: Matrix4) -> float:
    values = matrix4.asTuple()

    return sum(values)
