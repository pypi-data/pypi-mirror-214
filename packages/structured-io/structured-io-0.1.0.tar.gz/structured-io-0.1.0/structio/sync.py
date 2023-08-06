# Task synchronization primitives
import structio
from structio.core.syscalls import suspend, checkpoint
from structio.exceptions import ResourceClosed
from structio.core.run import current_task, current_loop
from structio.abc import ChannelReader, ChannelWriter, Channel
from structio.util.ki import enable_ki_protection
from structio.core.task import Task
from collections import deque, defaultdict
from typing import Any, Callable, Coroutine
from functools import partial, wraps


class Event:
    """
    A wrapper around a boolean value that can be waited
    on asynchronously. The majority of structio's API is
    designed on top of/around this class, as it constitutes
    the simplest synchronization primitive there is
    """

    def __init__(self):
        """
        Public object constructor
        """

        self._set = False
        self._tasks: deque[Task] = deque()

    def is_set(self):
        return self._set

    @enable_ki_protection
    async def wait(self):
        """
        Wait until someone else calls set() on
        this event. If the event has already been
        set, this method returns immediately
        """

        if self.is_set():
            await checkpoint()
            return
        self._tasks.append(current_task())
        await suspend()  # We get re-scheduled by set()

    @enable_ki_protection
    def set(self):
        """
        Sets the event, awaking all tasks
        that called wait() on it
        """

        if self.is_set():
            raise RuntimeError("the event has already been set")
        self._set = True
        for waiter in self._tasks:
            current_loop().reschedule(waiter)
        self._tasks.clear()


class Queue:
    """
    An asynchronous FIFO queue
    """

    def __init__(self, maxsize: int | None = None):
        """
        Object constructor
        """

        self.maxsize = maxsize
        # Stores event objects for tasks wanting to
        # get items from the queue
        self.getters: deque[Event] = deque()
        # Stores event objects for tasks wanting to
        # put items on the queue
        self.putters: deque[Event] = deque()
        self.container: deque = deque()

    def __len__(self):
        """
        Returns the length of the queue
        """

        return len(self.container)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({f', '.join(map(str, self.container))})"

    async def __aiter__(self):
        """
        Implements the asynchronous iterator protocol
        """

        return self

    async def __anext__(self):
        """
        Implements the asynchronous iterator protocol
        """

        return await self.get()

    @enable_ki_protection
    async def put(self, item: Any):
        """
        Pushes an element onto the queue. If the
        queue is full, waits until there's
        enough space for the queue
        """

        if self.maxsize and len(self.container) == self.maxsize:
            self.putters.append(Event())
            await self.putters[-1].wait()
        if self.getters:
            self.getters.popleft().set()
        self.container.append(item)
        await checkpoint()

    @enable_ki_protection
    async def get(self) -> Any:
        """
        Pops an element off the queue. Blocks until
        an element is put onto it again if the queue
        is empty
        """

        if not self.container:
            self.getters.append(Event())
            await self.getters[-1].wait()
        if self.putters:
            self.putters.popleft().set()
        result = self.container.popleft()
        await checkpoint()
        return result

    def clear(self):
        """
        Clears the queue
        """

        self.container.clear()

    def reset(self):
        """
        Resets the queue
        """

        self.clear()
        self.getters.clear()
        self.putters.clear()


class MemorySendChannel(ChannelWriter):
    """
    An in-memory one-way channel to send
    data
    """

    def __init__(self, buffer):
        self._buffer = buffer
        self._closed = False

    @enable_ki_protection
    async def send(self, value):
        if self._closed:
            raise ResourceClosed("cannot operate on a closed channel")
        await self._buffer.put(value)

    @enable_ki_protection
    async def close(self):
        self._closed = True
        await checkpoint()

    def writers(self):
        return len(self._buffer.putters)


class MemoryReceiveChannel(ChannelReader):
    """
    An in-memory one-way channel to read
    data
    """

    def __init__(self, buffer):
        self._buffer = buffer
        self._closed = False

    @enable_ki_protection
    async def receive(self):
        if self._closed:
            raise ResourceClosed("cannot operate on a closed channel")
        return await self._buffer.get()

    @enable_ki_protection
    async def close(self):
        self._closed = True
        await checkpoint()

    def pending(self):
        return bool(self._buffer)

    def readers(self):
        return len(self._buffer.getters)


class MemoryChannel(Channel, MemorySendChannel, MemoryReceiveChannel):
    """
    An in-memory, two-way channel between
    tasks with optional buffering
    """

    def __init__(self, buffer_size):
        self._buffer = Queue(buffer_size)
        super().__init__(self._buffer)
        self.reader = MemoryReceiveChannel(self._buffer)
        self.writer = MemorySendChannel(self._buffer)

    @enable_ki_protection
    async def close(self):
        await self.reader.close()
        await self.writer.close()


class Semaphore:
    """
    An asynchronous integer semaphore. The use of initial_size
    is for semaphores which we know that can grow up to max_size
    but that can't right now, say because there's too much load on
    the application and resources are constrained. If it is None,
    initial_size equals max_size
    """

    def __init__(self, max_size: int, initial_size: int | None = None):

        if initial_size is None:
            initial_size = max_size
        assert initial_size <= max_size
        self.max_size = max_size
        # We use an unbuffered memory channel to pause
        # as necessary, kinda like socket.set_wakeup_fd
        # or something? Anyway I think it's pretty nifty
        self.channel: MemoryChannel = MemoryChannel(0)
        self._counter: int = initial_size

    def __repr__(self):
        return f"<structio.Semaphore max_size={self.max_size} size={self._counter}>"

    @property
    def size(self) -> int:
        return self._counter

    @enable_ki_protection
    async def acquire(self):
        """
        Acquires the semaphore, possibly
        blocking if the task counter is
        exhausted
        """

        if self._counter == 0:
            await self.channel.receive()
        self._counter -= 1
        await checkpoint()

    @enable_ki_protection
    async def release(self):
        """
        Releases a slot in the semaphore. Raises RuntimeError
        if there are no occupied slots to release
        """

        if self._counter == self.max_size:
            raise RuntimeError("semaphore is not acquired")
        self._counter += 1
        if self.channel.readers():
            await self.channel.send(None)
        else:
            await checkpoint()

    @enable_ki_protection
    async def __aenter__(self):
        await self.acquire()
        return self

    @enable_ki_protection
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.release()


class Lock:
    """
    An asynchronous single-owner task lock. Unlike
    the lock in threading.Thread, only the lock's
    owner can release it
    """

    def __init__(self):
        self._owner: Task | None = None
        self._sem: Semaphore = Semaphore(1)

    @property
    def owner(self) -> Task | None:
        """
        Returns the current owner of the lock,
        or None if the lock is not being held
        """

        return self._owner

    @property
    def locked(self) -> bool:
        """
        Returns whether the lock is currently
        held
        """

        return self._sem.size == 0

    @enable_ki_protection
    async def acquire(self):
        """
        Acquires the lock, possibly
        blocking until it is available
        """

        await self._sem.acquire()
        self._owner = current_task()

    @enable_ki_protection
    async def release(self):
        """
        Releases the lock if it was previously
        acquired by the caller. If the lock is
        not currently acquired or if it is not
        acquired by the calling task, RuntimeError
        is raised
        """

        if not self.owner:
            raise RuntimeError("lock is not acquired")
        if current_task() is not self.owner:
            raise RuntimeError("lock can only be released by the owner")
        self._owner = None
        await self._sem.release()

    @enable_ki_protection
    async def __aenter__(self):
        await self.acquire()
        return self

    @enable_ki_protection
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.release()


class RLock(Lock):
    """
    An asynchronous, single-owner recursive lock.
    Recursive locks have the property that their
    acquire() method can be called multiple times
    by the owner without deadlocking: each call
    increments an internal counter, which is decremented
    at every call to release(). The lock is released only
    when the internal counter reaches zero
    """

    def __init__(self):
        super().__init__()
        self._acquire_count = 0

    @enable_ki_protection
    async def acquire(self):
        current = current_task()
        if self.owner != current:
            await super().acquire()
        else:
            await checkpoint()
        self._acquire_count += 1

    @property
    def acquire_count(self) -> int:
        """
        Returns the number of times acquire()
        was called by the owner (note that it
        may be zero if the lock is not being
        held)
        """

        return self._acquire_count

    @enable_ki_protection
    async def release(self):
        # I hate the repetition, but it's the
        # only way to make sure that a task can't
        # decrement the counter of a lock it does
        # not own
        current = current_task()
        if self.owner != current:
            await super().release()
        else:
            self._acquire_count -= 1
            if self._acquire_count == 0:
                await super().release()
            else:
                await checkpoint()


_events: dict[str, list[Callable[[Any, Any], Coroutine[Any, Any, Any]]]] = defaultdict(list)


async def emit(evt: str, *args, **kwargs):
    """
    Fire the event and call all of its handlers with
    the event name as the first argument and all other
    positional and keyword arguments passed to this
    function after that. Returns once all events have
    completed execution
    """

    async with structio.create_pool() as pool:
        for func in _events[evt]:
            pool.spawn(partial(func, evt, *args, **kwargs))


def register_event(evt: str, func: Callable[[Any, Any], Coroutine[Any, Any, Any]]):
    """
    Register the given async function for the given event name.
    Note that if the given async function is already registered
    for the chosen event, it will be called once for each time
    this function is called once the associated event is fired
    """

    _events[evt].append(func)


def unregister_event(evt: str, func: Callable[[Any, Any], Coroutine[Any, Any, Any]]):
    """
    Unregisters the given async function from the given event.
    Nothing happens if the given event or async functions are
    not registered yet
    """

    try:
        _events[evt].remove(func)
    except IndexError:
        pass


def on_event(evt: str):
    """
    Convenience decorator to
    register async functions
    to events
    """

    def decorator(f):
        @wraps
        def wrapper(*args, **kwargs):
            f(*args, **kwargs)
        register_event(evt, f)
        return wrapper

    return decorator
