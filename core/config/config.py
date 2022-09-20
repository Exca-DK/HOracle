
from __future__ import annotations
from asyncio.log import logger
from dataclasses import dataclass
from distutils.command.config import config
import json
import os
from typing import Dict, List

from ..events.types import HEvent, StringToHEvent
from ..logging.types import LoggingLevel


class Endpoint:
    def __init__(self, target: str, type: HEvent) -> None:
        self.endpoint = target
        self.type = type

@dataclass
class Config:
    Endpoints: List[Endpoint]
    User: str
    Url: str 
    Verbosity: LoggingLevel
    Contexts: List[str]
   

__defaultUrl__ = "http://localhost:2106/"
__defaultUser__ = "user"
__defaultEndpoints__ = ["ParmTupleChanged","NodeCreated","NodeDeleted","SceneSaved","RenderActivity", "ViewportActivity"]
__defaultContexts__ = ["obj","out"]
__defaultVerbosity__ = 21

__cfg__: Config = None

# {
#     "user": "exca",
#     "url": "http://localhost:2106/",
#     "endpoints": ["ParmTupleChanged","NodeCreated","NodeDeleted","SceneSaved","RenderActivity", "ViewportActivity"],
#     "verbosity": 21
# }

def resolvePath() -> str | None:
    path = os.environ.get('HORACLE_PATH', None)
    if path is None:
        return
    path = path.replace("\\", "/")
    return path

def LoadConfig():
    path = resolvePath()
   
    try:
        with open(f"{path}/config.json", "r") as f:
            data: Dict = json.load(f)
    except FileNotFoundError:

        data = {}

    user = data.get("user", __defaultUser__)
    url = data.get("url", __defaultUrl__)
    endpointsRaw = data.get("endpoints", __defaultEndpoints__)
    contextsRaw = data.get("contexts", __defaultContexts__)
    verbosity = data.get("verbosity", __defaultVerbosity__)
    lvl = LoggingLevel.ToLvl(verbosity)
    endpoints = []

    for ep in endpointsRaw:
        hevent = StringToHEvent(ep)
        if hevent is not None:

            endpoints.append(Endpoint(url+ep, hevent))

    contexts = []
    for context in contextsRaw:
        contexts.append("/"+context)

    global __cfg__
    __cfg__ = Config(endpoints, user, url, lvl, contexts)



def GetCurrentUser() -> str:
    global __cfg__
    return __cfg__.User

def GetCurrentUrl() -> str:
    global __cfg__
    return __cfg__.Url

def GetEndpoints() -> List[Endpoint]:
    global __cfg__
    return __cfg__.Endpoints

def GetVerbosity() -> LoggingLevel:
    global __cfg__
    return __cfg__.Verbosity

def GetContexts() -> List[str]:
    global __cfg__
    return __cfg__.Contexts
