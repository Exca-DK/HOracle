from __future__ import annotations
from email.header import Header

from typing import Tuple
import hou
from enum import Enum


class HEvent(Enum):
    """Wrapper around hou.nodeEventType."""
    Default = -1

    #Nodes
    BeingDeleted = hou.nodeEventType.BeingDeleted
    NameChanged = hou.nodeEventType.NameChanged
    FlagChanged = hou.nodeEventType.FlagChanged
    AppearanceChanged = hou.nodeEventType.AppearanceChanged
    PositionChanged = hou.nodeEventType.PositionChanged
    InputRewired = hou.nodeEventType.InputRewired
    InputDataChanged = hou.nodeEventType.InputDataChanged
    ParmTupleChanged = hou.nodeEventType.ParmTupleChanged
    ParmTupleAnimated = hou.nodeEventType.ParmTupleAnimated
    ParmTupleChannelChanged = hou.nodeEventType.ParmTupleChannelChanged
    ChildCreated = hou.nodeEventType.ChildCreated
    ChildSwitched = hou.nodeEventType.ChildSwitched
    ChildSelectionChanged = hou.nodeEventType.ChildSelectionChanged
    NetworkBoxCreated = hou.nodeEventType.NetworkBoxCreated
    NetworkBoxChanged = hou.nodeEventType.NetworkBoxChanged
    NetworkBoxDeleted = hou.nodeEventType.NetworkBoxDeleted
    StickyNoteCreated = hou.nodeEventType.StickyNoteCreated
    StickyNoteChanged = hou.nodeEventType.StickyNoteChanged
    StickyNoteDeleted = hou.nodeEventType.StickyNoteDeleted
    IndirectInputCreated = hou.nodeEventType.IndirectInputCreated
    IndirectInputDeleted = hou.nodeEventType.IndirectInputDeleted
    SpareParmTemplatesChanged = hou.nodeEventType.SpareParmTemplatesChanged
    SelectionChanged = hou.nodeEventType.SelectionChanged
    CustomDataChanged = hou.nodeEventType.CustomDataChanged
    WorkItemSelectionChanged = hou.nodeEventType.WorkItemSelectionChanged

    #Viewports
    SceneSaved = hou.hipFileEventType.AfterSave
    ViewportActivity = 9000

    #Renders
    RenderActivity = 9001
    RenderStart = 9002
    FrameStart = 9003
    FrameEnd = 9004
    RenderEnd = 9005

mapping = {
    HEvent.BeingDeleted: ["BeingDeleted", "NodeDeleted"],
    HEvent.NameChanged: ["NameChanged"],
    HEvent.FlagChanged: ["FlagChanged"],
    HEvent.AppearanceChanged: ["AppearanceChanged"],
    HEvent.PositionChanged: ["PositionChanged"],
    HEvent.InputRewired: ["InputRewired"],
    HEvent.InputDataChanged: ["InputDataChanged"],
    HEvent.ParmTupleChanged: ["ParmTupleChanged"],
    HEvent.ParmTupleAnimated: ["ParmTupleAnimated"],
    HEvent.ParmTupleChannelChanged: ["ParmTupleChannelChanged"],
    HEvent.ChildSwitched: ["ChildSwitched"],
    HEvent.ChildCreated: ["ChildCreated", "NodeCreated"],
    HEvent.ChildSelectionChanged: ["ChildSelectionChanged"],
    HEvent.NetworkBoxCreated: ["NetworkBoxCreated"],
    HEvent.NetworkBoxChanged: ["NetworkBoxChanged"],
    HEvent.NetworkBoxDeleted: ["NetworkBoxDeleted"],
    HEvent.StickyNoteCreated: ["StickyNoteCreated"],
    HEvent.StickyNoteChanged: ["StickyNoteChanged"],
    HEvent.StickyNoteDeleted: ["StickyNoteDeleted"],
    HEvent.IndirectInputCreated: ["IndirectInputCreated"],
    HEvent.IndirectInputDeleted: ["IndirectInputDeleted"],
    HEvent.SpareParmTemplatesChanged: ["SpareParmTemplatesChanged"],
    HEvent.SelectionChanged: ["SelectionChanged"],
    HEvent.CustomDataChanged: ["CustomDataChanged"],
    HEvent.WorkItemSelectionChanged: ["WorkItemSelectionChanged"],
    HEvent.SceneSaved: ["SceneSaved"],
    HEvent.RenderActivity: ["RenderActivity"],
    HEvent.ViewportActivity: ["ViewportActivity"],
}

def HEventToString(hevent: HEvent) -> str | None:
    if hevent in mapping:
        return mapping[hevent]
    return None

def StringToHEvent(hevent: str) -> HEvent | None:
    for key, values in mapping.items():
        for name in values:
            if name == hevent:
                return key
    return None





