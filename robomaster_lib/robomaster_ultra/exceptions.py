# Exception Handling

__all__ = ['TimeOutError']


class SDKException(Exception):
    """Base class of all SDK exceptions."""


class TimeOutError(SDKException):
    """Remote Call Timeout."""


class OutOfRangeError(SDKException):
    """Params Values OutOfRange."""


class ConnectionError(SDKException):
    """Connection TimeOut."""
