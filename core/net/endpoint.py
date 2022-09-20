from enum import Enum
import json
from requests import post, get
from ..serialization import serializer, interface

from ..logging.logger import GetLogger
logger = GetLogger(__name__)


class EndpointType(Enum):
    Get = 0
    Post = 1
    Status = 2


class Endpoint:

    def __init__(self, url: str, type: EndpointType) -> None:
        self.Url = url
        self.Type = type
    def Send(self, data: interface.ISeralizable):
        headers = {"Content-Type": "application/json"}
        raw = serializer.Serializer.Deserialize(data)
        if isinstance(raw, dict):
            raw = json.dumps(raw)
        if raw is None:
            logger.warn(f"aborting sending {data} to {self.Url}")
            return None
        if self.Type.value == EndpointType.Get.value:
            logger.debug(f"Sending get to server. Target: {self.Url}\tData{raw}")
            return get(self.Url, data=raw, headers=headers)
        elif self.Type.value == EndpointType.Post.value:
            logger.debug(f"Sending post to server. Target: {self.Url}\tData{raw}")
            return post(self.Url, data=raw, headers=headers)
        else:
            raise Exception("???")

class EndpointSet:
    def __init__(self, post: Endpoint, get: Endpoint, status: Endpoint) -> None:
        self.Post = post
        self.Get = get
        self.Status = status
    

    def GetEndpointFromType(self, type: EndpointType) -> Endpoint:
        if type.value == 0:
            return self.Get
        elif type.value == 1:
            return self.Post
        elif type.value == 2:
            return self.Status
        else:
            raise Exception(f"{type} not supported")


# EndpointSet = namedtuple('EndpointSet', ['status', 'get', 'post'])

def CreatePostEndpoint(url: str) -> Endpoint:
    return Endpoint(url + "/post/", EndpointType.Post)

def CreateGetEndpoint(url: str) -> Endpoint:
    return Endpoint(url + "/get/", EndpointType.Get)

def CreateStatusEndpoint(url: str) -> Endpoint:
    return Endpoint(url + "/status/", EndpointType.Get)


def CreateEndpointSet(url: str) -> EndpointSet:
    post = CreatePostEndpoint(url)
    get = CreateGetEndpoint(url)
    status = CreateStatusEndpoint(url)

    return EndpointSet(post, get, status)


    