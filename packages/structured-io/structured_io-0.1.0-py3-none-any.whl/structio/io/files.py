import io
import sys
import structio
from functools import partial
from structio.abc import AsyncResource
from structio.core.syscalls import check_cancelled

# Stolen from Trio
_FILE_SYNC_ATTRS = {
    "closed",
    "encoding",
    "errors",
    "fileno",
    "isatty",
    "newlines",
    "readable",
    "seekable",
    "writable",
    "buffer",
    "raw",
    "line_buffering",
    "closefd",
    "name",
    "mode",
    "getvalue",
    "getbuffer",
}

_FILE_ASYNC_METHODS = {
    "flush",
    "read",
    "read1",
    "readall",
    "readinto",
    "readline",
    "readlines",
    "seek",
    "tell",
    "truncate",
    "write",
    "writelines",
    "readinto1",
    "peek",
}


class AsyncFile(AsyncResource):
    """
    Asynchronous wrapper around regular file-like objects.
    Blocking operations are turned into async ones using threads.
    Note that this class can wrap pretty much anything with a fileno()
    and read/write methods
    """

    def fileno(self):
        return self.handle.fileno()

    def __init__(self, f):
        self._file = f

    @property
    def handle(self) -> io.IOBase:
        """
        Returns the underlying (synchronous!) OS-specific
        handle for the given resource
        """

        return self._file

    def __aiter__(self):
        return self

    async def __anext__(self):
        line = await self.readline()
        if line:
            return line
        else:
            raise StopAsyncIteration

    # Look, I get it, I can't keep stealing stuff from Trio,
    # but come on, it's so good!

    def __getattr__(self, name):
        if name in _FILE_SYNC_ATTRS:
            return getattr(self.handle, name)
        if name in _FILE_ASYNC_METHODS:
            meth = getattr(self.handle, name)

            async def wrapper(*args, **kwargs):
                func = partial(meth, *args, **kwargs)
                return await structio.thread.run_in_worker(func)

            # cache the generated method
            setattr(self, name, wrapper)
            return wrapper
        raise AttributeError(name)

    def __repr__(self):
        return f"structio.AsyncFile({self.handle})"

    def __dir__(self):
        attrs = set(super().__dir__())
        attrs.update(a for a in _FILE_SYNC_ATTRS if hasattr(self.handle, a))
        attrs.update(a for a in _FILE_ASYNC_METHODS if hasattr(self.handle, a))
        return attrs

    async def close(self):
        """
        Closes the file asynchronously. If the operation
        is cancelled, the underlying file object is *still*
        closed!
        """

        # This operation is non-cancellable, meaning it'll run
        # no matter what our event loop has to say about it.
        # After we're done, we'll obviously re-raise the cancellation
        # if necessary. This ensures files are always closed even when
        # the operation gets cancelled
        await structio.thread.run_in_worker(self.handle.close)
        # If we were cancelled, here is where we raise
        await check_cancelled()


async def open_file(
    file,
    mode="r",
    buffering=-1,
    encoding=None,
    errors=None,
    newline=None,
    closefd=True,
    opener=None,
) -> AsyncFile:
    """
    Like io.open(), but async
    """

    return wrap_file(
        await structio.thread.run_in_worker(
            io.open, file, mode, buffering, encoding, errors, newline, closefd, opener
        )
    )


def wrap_file(file) -> AsyncFile:
    """
    Wraps a file-like object into an async
    wrapper
    """

    return AsyncFile(file)


stdin = wrap_file(sys.stdin)
stdout = wrap_file(sys.stdout)
stderr = wrap_file(sys.stderr)


async def aprint(*args, sep=" ", end="\n", file=stdout, flush=False):
    """
    Like print(), but asynchronous
    """

    await file.write(f"{sep.join(map(str, args))}{end}")
    if flush:
        await file.flush()


async def ainput(prompt=None, /):
    """
    Like input(), but asynchronous
    """

    await aprint(prompt, end="", flush=True)
    return (await stdin.readline()).rstrip("\n")
