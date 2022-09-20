from __future__ import annotations
from datetime import datetime
import json
from typing import Dict

from ..serialization.serializer import Serializer
from ..serialization.interface import ISeralizable
from ..exceptions.base import NotSerializable, ParseExeception


class Event(ISeralizable):

    def __init__(self, data: ISeralizable, timestamp=None) -> None:
        if not Serializer.IsDeserializable(data):
            raise NotSerializable(data)
        self.Data = data
        if timestamp is None:
            self.Timestamp = datetime.utcnow()
        else:
            self.Timestamp = timestamp


    def Deserialize(self):
        return {"timestamp": self.Timestamp.isoformat(), "data": self.Data.Deserialize()}


    @classmethod
    def __FromDict(cls, dictObj: Dict):
        """No safety-checks. Only for internal"""
        tmp = []
        annotations = Event.__annotations__
        for name in annotations.keys():
            tmp.append(dictObj[name])

        return cls(*tmp)

    @staticmethod
    def Serialize(eventLikeness: str) -> Event:
        """Serializes event object from string. Checks if all required fields exist and are of specific type.

        Raises:
            ParseExeception: Missing or invalid type of field
        """
        js: Dict = json.loads(eventLikeness)
        

        annotations = Event.__annotations__
        for name, _type in annotations.items():
            field = js.get(name, None)
            if field is None:
                raise ParseExeception(
                    f"Could not find field: {name}", Event)
            if not isinstance(field, _type):
                try:
                    field = _type(field)
                except:
                    raise ParseExeception(
                        f"Field of name: {name} with value {field} is not of type: {_type.__name__}", Event)

        return Event.__FromDict(js)

        

        
