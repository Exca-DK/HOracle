from enum import Enum
from typing import Tuple

from .netWorker import NetWorker
from ..exceptions.base import EndpointSetNotFound
from ..events.event import Event
from ..events.types import HEvent
from ..config.config import GetCurrentUser
from ..net.endpoint import EndpointType
from ..serialization.interface import ISeralizable


from ..logging.logger import GetLogger
logger = GetLogger(__name__)


class HTTPworker(NetWorker):

    def SendAvaiable(self):
        while not self.buffer.IsEmpty():
            serializable, under, etype = self.buffer.GetOldest()
            eset = self.GetEndpointSet(under)
            if eset is None:
                raise EndpointSetNotFound(under)
            ep = eset.GetEndpointFromType(etype)
            try:
                logger.debug(f"sending: {serializable} to {ep.Url}")
                response = ep.Send(serializable)
                logger.debug(f"status: {response.status_code}, data: {response.text}")
            except Exception as e:
                logger.warn(e)
                return
            if response is None:
                continue

    def OnEvent(self, item: Tuple[Event, Enum]) -> Tuple[ISeralizable, Enum, EndpointType]:
        #TODO Refactor into state machine later
        serializable = item[0].Data
        source = item[1]
        user = GetCurrentUser()
        if source.name == HEvent.ParmTupleChanged.name:
            serializable["user"] = user
            return serializable, source, EndpointType.Post
        elif source.name == HEvent.ChildCreated.name:
            serializable["user"] = user
            return serializable, source, EndpointType.Post
        elif source.name == HEvent.BeingDeleted.name:
            serializable["user"] = user
            return serializable, source, EndpointType.Post
        elif source.name == HEvent.ViewportActivity.name:
            return {"user": user}, source, EndpointType.Post
        elif source.name == HEvent.SceneSaved.name:
            serializable["user"] = user
            return serializable, source, EndpointType.Post
        elif source.name == HEvent.RenderActivity.name:
            serializable["user"] = user
            return serializable, source, EndpointType.Post
        else:
            raise NotImplementedError(f"http worker does not support {source.name}")