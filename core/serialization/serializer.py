from __future__ import annotations
from typing import Any, Dict

from .interface import ISeralizable
from ..exceptions.base import DeserializationError, ParseExeception, SerializationError


from ..logging.logger import GetLogger
logger = GetLogger(__name__)


class Serializer:

    @staticmethod
    def TryDeserialize(item: Any) -> str | Dict[str, str]:
        if item is None:
            return "none"
        elif isinstance(item, ISeralizable):
                return item.Deserialize()
        elif isinstance(item, Dict):
            d = {}
            for key, value in item.items():
                k = Serializer.TryDeserialize(key)
                v = Serializer.TryDeserialize(value)
                d[k] = v
            return d
        else:
            try:
                return str(item)
            except:
                raise DeserializationError(dict)


    @staticmethod
    def Deserialize(serializableObject: ISeralizable) -> str | Dict[str, str] | None:
        try:
            logger.debug(f"deserializing: {serializableObject}")
            deserialized = Serializer.TryDeserialize(serializableObject)
            return deserialized
        except DeserializationError as e:
            logger.warn(e)
        except Exception as e:
            logger.error(e)

    @staticmethod
    def Serialize(deserializableObject: str, type: ISeralizable) -> ISeralizable | None:
        try:
            serialized = type.Serialize(deserializableObject)
            if not Serializer.IsDeserializable(serialized):
                raise SerializationError(deserializableObject)
            return serialized
        except SerializationError as e:
            logger.warn(e)
        except ParseExeception as e:
            logger.warn(e)
        except Exception as e:
            logger.error(e)

    @staticmethod
    def IsDeserializable(item: Any) -> bool:
        """Checks if an item is either ISerizable instance or str instance"""
        if isinstance(item, ISeralizable):
            return True
        elif item is None:
            return True
        elif isinstance(item, dict):
            for key, value in item.items():
                t = Serializer.IsDeserializable(key)
                if not t:
                    return False
                t = Serializer.IsDeserializable(value)
                if not t:
                    return False
            return True
        try:
            str(item)
        except Exception:
            return False
        return True





