from structio.core import run as _run
from typing import Coroutine, Any, Callable
from structio.core.kernels.fifo import FIFOKernel
from structio.core.managers.io.simple import SimpleIOManager
from structio.core.managers.signals.sigint import SigIntManager
from structio.core.time.clock import DefaultClock
from structio.core.syscalls import sleep, suspend as _suspend
from structio.core.context import TaskPool, TaskScope
from structio.exceptions import Cancelled, TimedOut, ResourceClosed
from structio.core import task
from structio.core.task import Task, TaskState
from structio.sync import Event, Queue, MemoryChannel, Semaphore, Lock, RLock, emit, on_event, register_event
from structio.abc import Channel, Stream, ChannelReader, ChannelWriter
from structio.io import socket
from structio.io.socket import AsyncSocket
from structio.io.files import (
    open_file,
    wrap_file,
    aprint,
    stdout,
    stderr,
    stdin,
    ainput,
)
from structio.core.run import current_loop, current_task
from structio import thread, parallel
from structio.path import Path


def run(
    func: Callable[[Any, Any], Coroutine[Any, Any, Any]],
    *args,
    restrict_ki_to_checkpoints: bool = False,
    tools: list | None = None,
):
    result = _run.run(
        func,
        FIFOKernel,
        SimpleIOManager(),
        [SigIntManager()],
        DefaultClock(),
        tools,
        restrict_ki_to_checkpoints,
        *args,
    )
    return result


run.__doc__ = _run.__doc__


def create_pool() -> TaskPool:
    """
    Creates a new task pool
    """

    return TaskPool()


def skip_after(timeout) -> TaskScope:
    """
    Creates a new task scope with the
    specified timeout. No error is raised
    when the timeout expires
    """

    result = TaskScope()
    result.timeout = timeout
    result.silent = True
    return result


def with_timeout(timeout) -> TaskScope:
    """
    Creates a new task scope with the
    specified timeout. TimeoutError is raised
    when the timeout expires
    """

    result = TaskScope()
    result.timeout = timeout
    return result


def clock():
    """
    Returns the current clock time of
    the event loop
    """

    return _run.current_loop().clock.current_time()


async def _join(self: Task):
    self.waiters.add(_run.current_task())
    await _suspend()
    if self.state == TaskState.CRASHED:
        raise self.exc
    return self.result


def _cancel(self: Task):
    _run.current_loop().cancel_task(self)


task._joiner = _join

_cancel.__name__ = Task.cancel.__name__
_cancel.__doc__ = Task.cancel.__doc__
Task.cancel = _cancel


__all__ = [
    "run",
    "sleep",
    "create_pool",
    "clock",
    "Cancelled",
    "skip_after",
    "with_timeout",
    "Event",
    "Queue",
    "MemoryChannel",
    "Channel",
    "Stream",
    "ChannelReader",
    "ChannelWriter",
    "Semaphore",
    "TimedOut",
    "Task",
    "TaskState",
    "TaskScope",
    "TaskPool",
    "ResourceClosed",
    "Lock",
    "RLock",
    "thread",
    "open_file",
    "wrap_file",
    "aprint",
    "stderr",
    "stdin",
    "stdout",
    "ainput",
    "current_loop",
    "current_task",
    "Path",
    "parallel"
]
