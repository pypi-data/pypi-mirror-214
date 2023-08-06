import inspect
import functools
from threading import local
from structio.abc import (
    BaseKernel,
    BaseDebugger,
    BaseClock,
    SignalManager,
    BaseIOManager,
)
from structio.exceptions import StructIOException
from structio.core.task import Task
from typing import Callable, Any, Coroutine

_RUN = local()


def current_loop() -> BaseKernel:
    """
    Returns the current event loop in the calling
    thread. Raises a StructIOException if no async
    context exists
    """
    try:
        return _RUN.kernel
    except AttributeError:
        raise StructIOException("must be called from async context") from None


def current_task() -> Task:
    """
    Shorthand for current_loop().current_task
    """

    return current_loop().current_task


def new_event_loop(kernel: BaseKernel):
    """
    Initializes a new event loop using the
    given kernel implementation. Cannot be
    called from an asynchronous context
    """

    try:
        current_loop()
    except StructIOException:
        _RUN.kernel = kernel
    else:
        if not _RUN.kernel.done():
            raise StructIOException(
                "cannot be called from running async context"
            ) from None


def run(
    func: Callable[[Any, Any], Coroutine[Any, Any, Any]],
    kernel: type,
    io_manager: BaseIOManager,
    signal_managers: list[SignalManager],
    clock: BaseClock,
    tools: list[BaseDebugger] | None = None,
    restrict_ki_to_checkpoints: bool = False,
    *args,
):
    """
    Starts the event loop from a synchronous entry point. All
    positional arguments are passed to the given coroutine
    function. If you want to pass keyword arguments, consider
    using functools.partial()
    """

    if not issubclass(kernel, BaseKernel):
        raise TypeError(
            f"kernel must be a subclass of {BaseKernel.__module__}.{BaseKernel.__qualname__}!"
        )
    check = func
    if isinstance(func, functools.partial):
        check = func.func
    if inspect.iscoroutine(check):
        raise StructIOException(
            "Looks like you tried to call structio.run(your_func(arg1, arg2, ...)), that is wrong!"
            "\nWhat you wanna do, instead, is this: structio.run(your_func, arg1, arg2, ...)"
        )
    elif not inspect.iscoroutinefunction(check):
        raise StructIOException(
            "structio.run() requires an async function as its first argument!"
        )
    new_event_loop(
        kernel(
            clock=clock,
            restrict_ki_to_checkpoints=restrict_ki_to_checkpoints,
            io_manager=io_manager,
            signal_managers=signal_managers,
            tools=tools,
        )
    )
    return current_loop().start(func, *args)
