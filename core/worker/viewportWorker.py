

from __future__ import annotations
from time import sleep
from typing import List

from .worker import Worker
from ..events.types import HEvent
from ..events.event import Event
from ..hwrappers.scene import GetCurrentSceneViewers, GetSceneViews, GeometryViewer
from ..hwrappers.matrix import FlattenMatrix, Matrix4
from ..utils.utils import Timer, IsClose


from ..logging.logger import GetLogger
logger = GetLogger(__name__)


class ViewportWorker(Worker):


    def __init__(self, viewportFrequency: int) -> None:
        super().__init__()
        self.counter = 0
        self.viewports: List[GeometryViewer] = []
        self.__timer = Timer()
        self.__pivots = []
        self.ViewportFrequency = viewportFrequency
        self.__eventChannel = None

    def SetEventChannel(self, channel):
        self.__eventChannel = channel

    def GetEventChannel(self):
        return self.__eventChannel

    def FetchViewports(self):
        t = Timer()
        t.Start()
        self.viewports = []
        scenes = GetCurrentSceneViewers()
        for scene in scenes:
            viewports = GetSceneViews(scene)
            for viewport in viewports:
                self.viewports.append(viewport)
        elapsed = t.Elapsed()
        logger.debug(f"Fetching viewports took: {elapsed} seconds")


    def AwaitViewports(self):
        counter = 0
        while True:
            if counter > 10:
                logger.error("Failed fetching viewports")
                raise Exception()
            try:
                self.FetchViewports()
            except:
                sleep(15)
                counter += 1
                continue
            break

    def ShouldFetchViewports(self) -> bool:
        if self.__timer.Elapsed() > 60:
            return True
        return False

    def ResetTimer(self):
        self.__timer = Timer()

    def FetchCoords(self):
        t = Timer()
        pivots = []
        for view in self.viewports:
            trans: Matrix4 = view.viewTransform()
            pivots.append(FlattenMatrix(trans))
        elapsed = t.Elapsed()
        logger.debug(f"Fetching coords took: {elapsed} seconds")
        return pivots

    def PivotsChanged(self, pivots):
        if len(pivots) != len(self.__pivots):
            return True
        
        for pivot in pivots:
            same = False
            for pivotB in self.__pivots:
                if IsClose(pivot, pivotB, 0.01):
                    same = True
                    break
            if same is False:
                return True
        return False


    def OnStart(self):
        sleep(5)
        self.AwaitViewports()
        self.ResetTimer()
        while True:
            if self.ShouldStop():
                break
            if self.ShouldFetchViewports():
                    self.AwaitViewports()
                    self.ResetTimer()
            try:
                pivots = self.FetchCoords()
            except Exception:
                self.AwaitViewports()
                self.ResetTimer()
                continue
            if self.PivotsChanged(pivots):
                self.__pivots = pivots
                channel = self.GetEventChannel()
                channel.put((Event(None), HEvent.ViewportActivity))
            sleep(self.ViewportFrequency)
            self.counter += 1

    def Cleanup(self):
        logger.debug(f"{self.__class__.__name__} | ID: {self.GetId()} has made {self.counter} iterations")
    
