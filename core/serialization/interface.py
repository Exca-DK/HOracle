from __future__ import annotations
from abc import ABC, abstractmethod, abstractstaticmethod

from ..logging.logger import GetLogger
logger = GetLogger(__name__)


class ISeralizable(ABC):

    @abstractmethod
    def Deserialize(self) -> str:
        pass

    @abstractstaticmethod
    def Serialize(serializedObject: str) -> ISeralizable:
        pass

