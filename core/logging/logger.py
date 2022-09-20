import logging
from .types import LoggingLevel
LOGGING_LEVEL = logging.INFO
loggers = set()
stream_handler = logging.StreamHandler()
standard_formatter = logging.Formatter("[%(levelname)s] - %(asctime)s - %(name)s - : %(message)s  - line:%(lineno)d")
stream_handler.setFormatter(standard_formatter)



def SetLoggingLevel(level: LoggingLevel):
    """Set minimum level for logging messages."""
    for logger in loggers:
        logger.setLevel(level.value)

def GetLogger(name=None) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(LOGGING_LEVEL)
    logger.addHandler(stream_handler)
    loggers.add(logger)
    return logger