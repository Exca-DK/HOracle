import json
from typing import List, Tuple
from dataclasses import dataclass

from .node import LightNode
from ..serialization.interface import ISeralizable


@dataclass
class HParameter:
    Name: str
    Value: str

@dataclass
class ParamField(ISeralizable):
    name: str
    value: str

    def Deserialize(self) -> str:
        return json.dumps(self.__dict__)

    @staticmethod
    def Serialize(serializedObject: str) -> ISeralizable:
        raise NotImplemented()

@dataclass
class Parameter(ISeralizable):
    name: str
    fields: Tuple[ParamField]
    value: str
    source: LightNode

    @classmethod
    def FromHParams(cls, params: List[HParameter], source: LightNode):
    
        def common_start(*args):
            def _iter():
                for iter in zip(*args):
                    first = iter[0]
                    for value in iter:
                        if value != first:
                            return
                    yield first

            return ''.join(_iter())
        names = []
        for param in params:
            names.append(param.Name)

        prefix = common_start(*names)
        fields = []
        for param in params:
            fields.append(ParamField(param.Name[len(prefix):], param.Value))

        return cls(prefix, tuple(fields), None, source)
    
    def Deserialize(self) -> str:
        d = self.__dict__
        fields = []
        if d["fields"] is not None:
            for field in d["fields"]:

                fields.append({"name": str(field.name), "value": str(field.value)})
        

        d["fields"] = fields
        d["value"] = str(self.value)
        d["source"] = self.source.Deserialize()
        return d

    @staticmethod
    def Serialize(serializedObject: str) -> ISeralizable:
        raise NotImplemented()
        



        


