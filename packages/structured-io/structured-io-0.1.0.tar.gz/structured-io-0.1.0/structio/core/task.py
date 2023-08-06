from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Coroutine, Any, Callable


class TaskState(Enum):
    INIT: int = auto()
    RUNNING: int = auto()
    PAUSED: int = auto()
    FINISHED: int = auto()
    CRASHED: int = auto()
    CANCELLED: int = auto()
    IO: int = auto()


_joiner: Callable[[Any, Any], Coroutine[Any, Any, Any]] | None = None


@dataclass
class Task:
    """
    An asynchronous task wrapper
    """

    # The task's name
    name: str
    # The underlying coroutine of this
    # task
    coroutine: Coroutine = field(repr=False)
    # The task's pool
    pool: "TaskPool" = field(repr=False)
    # The state of the task
    state: TaskState = field(default=TaskState.INIT)
    # What error did the task raise, if any?
    exc: BaseException | None = None
    # The task's return value, if any
    result: Any | None = None
    # When did the task pause last time?
    paused_when: Any = -1
    # When is the task's next deadline?
    next_deadline: Any = -1
    # Is cancellation pending?
    pending_cancellation: bool = False
    # Any task explicitly joining us?
    waiters: set["Task"] = field(default_factory=set)

    def done(self):
        """
        Returns whether the task is running
        """

        return self.state in [
            TaskState.CRASHED,
            TaskState.FINISHED,
            TaskState.CANCELLED,
        ]

    def __hash__(self):
        """
        Implements hash(self)
        """

        return self.coroutine.__hash__()

    # These are patched later at import time!
    def __await__(self):
        """
        Wait for the task to complete and return/raise appropriately (returns when cancelled)
        """

        return _joiner(self).__await__()

    def cancel(self):
        """
        Cancels the given task
        """

        return NotImplemented
