from email import message
from typing import Type


class Error(Exception):
    """Base class for other exceptions"""
    pass

class ListenerNotImplemented(Error):

    def __init__(self, event) -> None:
        message = f"Listener for {event} has not been implemented."
        super().__init__(message)

class ListenerAlreadyExists(Error):

    def __init__(self, event) -> None:
        message = f"Listener for {event} already exists."
        super().__init__(message)

class EmptyListeners(Error):

    def __init__(self, event) -> None:
        message = f"Event: {event} has no active listeners."
        super().__init__(message)

class ParamNotFound(Error):

    def __init__(self, paramName) -> None:
        message = f"Parameter: {paramName} has not been found."
        super().__init__(message)

class ErrorWhenEvalParam(Error):

    def __init__(self, source) -> None:
        message = f"Encountered error when evaluating parameter. Source: {source}"
        super().__init__(message)


class SerializationError(Error):

    def __init__(self, source: str, type: Type) -> None:
        message = f"Encountered error when serializing object. Source: {source}, Wants: {type}"
        super().__init__(message)


class DeserializationError(Error):

    def __init__(self, source) -> None:
        message = f"Encountered error when deserializing object. Object: {source}"
        super().__init__(message)


class NotSerializable(Error):

    def __init__(self, source) -> None:
        message = f"Object {source} is not serializable"
        super().__init__(message)

class ParseExeception(Exception):
    message = "Could not parse due to missing one or more field"
    def __init__(self, error, objectReference):            

        super().__init__(ParseExeception.message)
        self.errors = f"ParseException: {error} when creating {objectReference.__name__} object"
    
class Forbidden(Exception):
    message = "Operation forbidden"
    def __init__(self, operation):            

        super().__init__(operation)
        self.errors = f"Operation: {operation} is forbidden"
    
    
class EndpointSetNotFound(Exception):
    message = "Endpoint set has not been found"
    def __init__(self, under):            

        super().__init__(under)
        self.errors = f"{message} under {under}"