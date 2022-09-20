from __future__ import annotations
from enum import Enum

class LoggingLevel(Enum):
    CRITICAL = 50
    ERROR = 40
    WARNING = 30
    INFO = 20
    DEBUG = 10
    NOTSET = 0


    @staticmethod
    def ToLvl(i: int) -> LoggingLevel:
        if i < LoggingLevel.DEBUG.value:
            return LoggingLevel.NOTSET
        elif i < LoggingLevel.INFO.value:
            return LoggingLevel.DEBUG
        elif i < LoggingLevel.WARNING.value:
            return LoggingLevel.INFO
        elif i < LoggingLevel.ERROR.value:
            return LoggingLevel.WARNING
        elif i < LoggingLevel.CRITICAL.value:
            return LoggingLevel.ERROR
        return LoggingLevel.CRITICAL