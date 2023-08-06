# This is, ahem, inspired by Curio and Trio. See https://github.com/dabeaz/curio/issues/104
import io
import os
from structio.core.syscalls import checkpoint, wait_readable, wait_writable, closing, release
from structio.exceptions import ResourceClosed
from structio.abc import AsyncResource
try:
    from ssl import SSLWantReadError, SSLWantWriteError, SSLSocket
    WantRead = (BlockingIOError, SSLWantReadError, InterruptedError)
    WantWrite = (BlockingIOError, SSLWantWriteError, InterruptedError)
except ImportError:
    WantWrite = (BlockingIOError, InterruptedError)
    WantRead = (BlockingIOError, InterruptedError)
    SSLSocket = None


class FdWrapper:
    """
    A simple wrapper around a file descriptor that
    allows the event loop to perform an optimization
    regarding I/O event registration safely. This is
    because while integer file descriptors can be reused
    by the operating system, instances of this class will
    not (hence if the event loop keeps around a dead instance
    of an FdWrapper, it at least won't accidentally register
    a new file with that same file descriptor). A bonus is
    that this also allows us to always assume that we can call
    fileno() on all objects registered in our selector, regardless
    of whether the wrapped fd is an int or something else entirely
    """

    __slots__ = ("fd", )

    def __init__(self, fd):
        self.fd = fd

    def fileno(self):
        return self.fd

    # Can be converted to an int
    def __int__(self):
        return self.fd

    def __repr__(self):
        return f"<fd={self.fd!r}>"


class AsyncStream(AsyncResource):
    """
    A generic asynchronous stream over
    a file-like object, with buffering
    """

    def __init__(
        self,
        fileobj
    ):
        self.fileobj = fileobj
        self._fd = FdWrapper(self.fileobj.fileno())
        self._buf = bytearray()

    async def _read(self, size: int = -1) -> bytes:
        raise NotImplementedError()

    async def write(self, data):
        raise NotImplementedError()

    async def read(self, size: int = -1):
        """
        Reads up to size bytes from the
        given stream. If size == -1, read
        as much as possible
        """

        if size < 0 and size < -1:
            raise ValueError("size must be -1 or a positive integer")
        if size == -1:
            size = len(self._buf)
        buf = self._buf
        if not buf:
            return await self._read(size)
        if len(buf) <= size:
            data = bytes(buf)
            buf.clear()
        else:
            data = bytes(buf[:size])
            del buf[:size]
        return data

    # Yes I stole this from curio. Sue me.
    async def readall(self):
        chunks = []
        maxread = 65536
        if self._buf:
            chunks.append(bytes(self._buf))
            self._buf.clear()
        while True:
            chunk = await self.read(maxread)
            if not chunk:
                return b''.join(chunks)
            chunks.append(chunk)
            if len(chunk) == maxread:
                maxread *= 2

    async def flush(self):
        pass

    async def close(self):
        """
        Closes the stream asynchronously
        """

        if self.fileno() == -1:
            return
        await self.flush()
        await closing(self._fd)
        await release(self._fd)
        self.fileobj.close()
        self.fileobj = None
        self._fd = -1
        await checkpoint()

    def fileno(self):
        """
        Wrapper socket method
        """

        return int(self._fd)

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        if self.fileno() != -1:
            await self.close()

    def __repr__(self):
        return f"AsyncStream({self.fileobj})"


class FileStream(AsyncStream):
    """
    A stream wrapper around a binary file-like object.
    The underlying file descriptor is put into non-blocking
    mode
    """

    async def _read(self, size: int = -1) -> bytes:
        while True:
            try:
                data = self.fileobj.read(size)
                if data is None:
                    # Files in non-blocking mode don't always
                    # raise a blocking I/O exception and can
                    # return None instead, so we account for
                    # that here
                    raise BlockingIOError()
                return data
            except WantRead:
                await wait_readable(self._fd)

    async def write(self, data):
        # We use a memory view so that
        # slicing doesn't copy any memory
        mem = memoryview(data)
        while mem:
            try:
                written = self.fileobj.write(data)
                if written is None:
                    raise BlockingIOError()
                mem = mem[written:]
            except WantWrite:
                await wait_writable(self._fd)

    async def flush(self):
        if self.fileno() == -1:
            return
        while True:
            try:
                return self.fileobj.flush()
            except WantWrite:
                await wait_writable(self._fd)
            except WantRead:
                await wait_readable(self._fd)

    def __init__(self, fileobj):
        if isinstance(fileobj, io.TextIOBase):
            raise TypeError("only binary mode files can be streamed")
        super().__init__(fileobj)
        os.set_blocking(self.fileno(), False)
