from types import coroutine
from typing import Any


@coroutine
def syscall(method: str, *args, **kwargs) -> Any | None:
    """
    Lowest-level primitive to interact with the event loop:
    calls a loop method with the provided arguments. This
    function should not be used directly, but through abstraction
    layers. All positional and keyword arguments are passed to
    the method itself and its return value is provided once the
    loop yields control back to us

    :param method: The loop method to call
    :type method: str
    :returns: The result of the method call, if any
    """

    result = yield method, args, kwargs
    return result


async def sleep(amount):
    """
    Puts the caller asleep for the given amount of
    time which is, by default, measured in seconds,
    but this is not enforced: if a custom clock
    implementation is being used, the values passed
    to this function may have a different meaning
    """

    await syscall("sleep", amount)


async def suspend():
    """
    Pauses the caller indefinitely
    until it is rescheduled
    """

    await syscall("suspend")


async def check_cancelled():
    """
    Introduce a cancellation point, but
    not a schedule point
    """

    return await syscall("check_cancelled")


async def schedule_point():
    """
    Introduce a schedule point, but not a
    cancellation point
    """

    return await syscall("schedule_point")


async def checkpoint():
    """
    Introduce a cancellation point and a
    schedule point
    """

    await check_cancelled()
    await schedule_point()


async def wait_readable(rsc):
    return await syscall("wait_readable", rsc)


async def wait_writable(rsc):
    return await syscall("wait_writable", rsc)


async def closing(rsc):
    return await syscall("notify_closing", rsc)


async def release(rsc):
    return await syscall("release_resource", rsc)
