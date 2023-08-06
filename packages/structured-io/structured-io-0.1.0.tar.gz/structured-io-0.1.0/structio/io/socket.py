from structio.abc import AsyncResource
from structio.io import FdWrapper, WantRead, WantWrite, SSLSocket
from structio.exceptions import ResourceClosed, ResourceBroken
from structio.core.syscalls import wait_readable, wait_writable, checkpoint, closing, release
from functools import wraps
import socket as _socket


@wraps(_socket.socket)
def socket(*args, **kwargs):
    return AsyncSocket(_socket.socket(*args, **kwargs))


class AsyncSocket(AsyncResource):
    """
    Abstraction layer for asynchronous sockets
    """

    def fileno(self):
        return int(self._fd)

    def __init__(
        self,
        sock: _socket.socket,
        close_on_context_exit: bool = True,
        do_handshake_on_connect: bool = True,
    ):
        self._fd = FdWrapper(sock.fileno())
        self.close_on_context_exit = close_on_context_exit
        # Do we perform the TCP handshake automatically
        # upon connection? This is mostly needed for SSL
        # sockets
        self.do_handshake_on_connect = do_handshake_on_connect
        self.socket = sock
        self.socket.setblocking(False)
        # A socket that isn't connected doesn't
        # need to be closed
        self.needs_closing: bool = False

    async def receive(self, max_size: int, flags: int = 0) -> bytes:
        """
        Receives up to max_size bytes from a socket asynchronously
        """

        assert max_size >= 1, "max_size must be >= 1"
        if self._fd == -1:
            raise ResourceClosed("I/O operation on closed socket")
        while True:
            try:
                data = self.socket.recv(max_size, flags)
                await checkpoint()
                return data
            except WantRead:
                await wait_readable(self._fd)
            except WantWrite:
                await wait_writable(self._fd)

    async def receive_exactly(self, size: int, flags: int = 0) -> bytes:
        """
        Receives exactly size bytes from a socket asynchronously.
        """

        # https://stackoverflow.com/questions/55825905/how-can-i-reliably-read-exactly-n-bytes-from-a-tcp-socket
        buf = bytearray(size)
        pos = 0
        while pos < size:
            n = await self.recv_into(memoryview(buf)[pos:], flags=flags)
            if n == 0:
                raise ResourceBroken("incomplete read detected")
            pos += n
        return bytes(buf)

    async def connect(self, address):
        """
        Wrapper socket method
        """

        if self._fd == -1:
            raise ResourceClosed("I/O operation on closed socket")
        while True:
            try:
                self.socket.connect(address)
                if self.do_handshake_on_connect:
                    await self.do_handshake()
                await checkpoint()
                break
            except WantWrite:
                await wait_writable(self._fd)
        self.needs_closing = True

    async def close(self):
        """
        Wrapper socket method
        """

        if self.needs_closing:
            self.socket.close()
            await checkpoint()

    async def accept(self):
        """
        Accepts the socket, completing the 3-step TCP handshake asynchronously
        """

        if self._fd == -1:
            raise ResourceClosed("I/O operation on closed socket")
        while True:
            try:
                remote, addr = self.socket.accept()
                await checkpoint()
                return type(self)(remote), addr
            except WantRead:
                await wait_readable(self._fd)

    async def send_all(self, data: bytes, flags: int = 0):
        """
        Sends all data inside the buffer asynchronously until it is empty
        """

        if self._fd == -1:
            raise ResourceClosed("I/O operation on closed socket")
        sent_no = 0
        while data:
            try:
                sent_no = self.socket.send(data, flags)
                await checkpoint()
            except WantRead:
                await wait_readable(self._fd)
            except WantWrite:
                await wait_writable(self._fd)
            data = data[sent_no:]

    async def shutdown(self, how):
        """
        Wrapper socket method
        """

        if self.fileno() == -1:
            raise ResourceClosed("I/O operation on closed socket")
        if self.socket:
            self.socket.shutdown(how)
            await checkpoint()

    async def bind(self, addr: tuple):
        """
        Binds the socket to an address
        :param addr: The address, port tuple to bind to
        :type addr: tuple
        """

        if self._fd == -1:
            raise ResourceClosed("I/O operation on closed socket")
        self.socket.bind(addr)
        await checkpoint()

    async def listen(self, backlog: int):
        """
        Starts listening with the given backlog
        :param backlog: The socket's backlog
        :type backlog: int
        """

        if self._fd == -1:
            raise ResourceClosed("I/O operation on closed socket")
        self.socket.listen(backlog)
        await checkpoint()

    # Yes, I stole these from Curio because I could not be
    # arsed to write a bunch of uninteresting simple socket
    # methods from scratch, deal with it.

    def settimeout(self, seconds):
        """
        Wrapper socket method
        """

        raise RuntimeError("Use with_timeout() to set a timeout")

    def gettimeout(self):
        """
        Wrapper socket method
        """

        return None

    def dup(self):
        """
        Wrapper socket method
        """

        return type(self)(self.socket.dup(), self.do_handshake_on_connect)

    async def do_handshake(self):
        """
        Wrapper socket method
        """

        if not hasattr(self.socket, "do_handshake"):
            return
        while True:
            try:
                self.socket: SSLSocket  # Silences pycharm warnings
                self.socket.do_handshake()
                await checkpoint()
            except WantRead:
                await wait_readable(self._fd)
            except WantWrite:
                await wait_writable(self._fd)

    async def recvfrom(self, buffersize, flags=0):
        """
        Wrapper socket method
        """

        while True:
            try:
                return self.socket.recvfrom(buffersize, flags)
            except WantRead:
                await wait_readable(self._fd)
            except WantWrite:
                await wait_writable(self._fd)

    async def recv_into(self, buffer, nbytes=0, flags=0):
        """
        Wrapper socket method
        """

        while True:
            try:
                data = self.socket.recv_into(buffer, nbytes, flags)
                await checkpoint()
                return data
            except WantRead:
                await wait_readable(self._fd)
            except WantWrite:
                await wait_writable(self._fd)

    async def recvfrom_into(self, buffer, bytes=0, flags=0):
        """
        Wrapper socket method
        """

        while True:
            try:
                data = self.socket.recvfrom_into(buffer, bytes, flags)
                await checkpoint()
                return data
            except WantRead:
                await wait_readable(self._fd)
            except WantWrite:
                await wait_writable(self._fd)

    async def sendto(self, bytes, flags_or_address, address=None):
        """
        Wrapper socket method
        """

        if address:
            flags = flags_or_address
        else:
            address = flags_or_address
            flags = 0
        while True:
            try:
                data = self.socket.sendto(bytes, flags, address)
                await checkpoint()
                return data
            except WantWrite:
                await wait_writable(self._fd)
            except WantRead:
                await wait_readable(self._fd)

    async def getpeername(self):
        """
        Wrapper socket method
        """

        while True:
            try:
                data = self.socket.getpeername()
                await checkpoint()
                return data
            except WantWrite:
                await wait_writable(self._fd)
            except WantRead:
                await wait_readable(self._fd)

    async def getsockname(self):
        """
        Wrapper socket method
        """

        while True:
            try:
                data = self.socket.getpeername()
                await checkpoint()
                return data
            except WantWrite:
                await wait_writable(self._fd)
            except WantRead:
                await wait_readable(self._fd)

    async def recvmsg(self, bufsize, ancbufsize=0, flags=0):
        """
        Wrapper socket method
        """

        while True:
            try:
                data = self.socket.recvmsg(bufsize, ancbufsize, flags)
                await checkpoint()
                return data
            except WantRead:
                await wait_readable(self._fd)

    async def recvmsg_into(self, buffers, ancbufsize=0, flags=0):
        """
        Wrapper socket method
        """

        while True:
            try:
                data = self.socket.recvmsg_into(buffers, ancbufsize, flags)
                await checkpoint()
                return data
            except WantRead:
                await wait_readable(self._fd)

    async def sendmsg(self, buffers, ancdata=(), flags=0, address=None):
        """
        Wrapper socket method
        """

        while True:
            try:
                data = self.socket.sendmsg(buffers, ancdata, flags, address)
                await checkpoint()
                return data
            except WantRead:
                await wait_writable(self._fd)

    def __repr__(self):
        return f"AsyncSocket({self.socket})"

