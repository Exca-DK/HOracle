from __future__ import annotations
from typing import Tuple

from ..exceptions.base import Forbidden

import hou

def GetCurrentSceneViewers() -> Tuple[SceneViewer]:
    sceneViews = [item for item in hou.ui.curDesktop().currentPaneTabs() if item.type() == hou.paneTabType.SceneViewer]
    return sceneViews

def GetSceneViews(scene: hou.SceneViewer) -> Tuple[GeometryViewer]:
    views = scene.viewports()
    return views
        
class SceneViewer(hou.SceneViewer):

    def __new__(cls):
        raise Forbidden(SceneViewer.__name__)

class GeometryViewer(hou.GeometryViewport):

    def __new__(cls):
        raise Forbidden(GeometryViewer.__name__)


