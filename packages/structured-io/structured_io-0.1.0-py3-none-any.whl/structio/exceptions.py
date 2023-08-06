class StructIOException(Exception):
    """
    A generic StructIO error
    """


class Cancelled(BaseException):
    # We inherit from BaseException
    # so that users don't accidentally
    # ignore cancellations
    """
    A cancellation exception
    """

    scope: "TaskScope"


class TimedOut(StructIOException):
    """
    Raised when a task scope times out.
    The scope attribute can be used to
    know which scope originally timed
    out
    """

    scope: "TaskScope"


class ResourceClosed(StructIOException):
    """
    Raised when an asynchronous resource is
    closed and no longer usable
    """


class ResourceBusy(StructIOException):
    """
    Raised when an attempt is made to use an
    asynchronous resource that is currently busy
    """


class ResourceBroken(StructIOException):
    """
    Raised when an asynchronous resource gets
    corrupted and is no longer usable
    """

