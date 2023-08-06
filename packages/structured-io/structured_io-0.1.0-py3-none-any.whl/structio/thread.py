# Support module for running synchronous functions as
# coroutines into worker threads and to submit asynchronous
# work to the event loop from a synchronous thread
import structio
import threading
from collections import deque
from structio.abc import BaseKernel
from structio.core.run import current_loop
from typing import Callable, Any, Coroutine
from structio.core.syscalls import checkpoint
from structio.sync import Event, Semaphore, Queue
from structio.util.ki import enable_ki_protection
from structio.exceptions import StructIOException


_storage = threading.local()
# Max number of concurrent threads that can
# be spawned by run_in_worker before blocking
_storage.max_workers = Semaphore(50)


def is_async_thread() -> bool:
    return hasattr(_storage, "parent_loop")


class AsyncThreadEvent(Event):
    """
    An extension of the regular event
    class that is safe to utilize both
    from threads and from async code
    """

    def __init__(self):
        super().__init__()
        self._lock = threading.Lock()
        self._workers: deque[threading.Event] = deque()

    @enable_ki_protection
    def wait_sync(self):
        """
        Like wait(), but synchronous
        """

        with self._lock:
            if self.is_set():
                return
            ev = threading.Event()
            self._workers.append(ev)
        ev.wait()

    @enable_ki_protection
    async def wait(self):
        with self._lock:
            if self.is_set():
                return
        await super().wait()

    @enable_ki_protection
    def set(self):
        with self._lock:
            if self.is_set():
                return
            # We can't just call super().set() because that
            # will call current_loop(), and we may have been
            # called from a non-async thread
            loop: BaseKernel = _storage.parent_loop
            for task in self._tasks:
                loop.reschedule(task)
            # Awakes all threads
            for evt in self._workers:
                evt.set()
            self._set = True


class AsyncThreadQueue(Queue):
    """
    An extension of the regular queue
    class that is safe to use both from
    threaded and asynchronous code
    """

    def __init__(self, max_size):
        super().__init__(max_size)
        self._lock = threading.Lock()

    @enable_ki_protection
    async def get(self):
        evt: AsyncThreadEvent | None = None
        with self._lock:
            if not self.container:
                self.getters.append(AsyncThreadEvent())
                evt = self.getters[-1]
            if self.putters:
                self.putters.popleft().set()
        if evt:
            await evt.wait()
        return self.container.popleft()

    @enable_ki_protection
    async def put(self, item):
        evt: AsyncThreadEvent | None = None
        with self._lock:
            if self.maxsize and self.maxsize == len(self.container):
                self.putters.append(AsyncThreadEvent())
                evt = self.putters[-1]
            if self.getters:
                self.getters.popleft().set()
        if evt:
            await evt.wait()
        self.container.append(item)
        await checkpoint()

    @enable_ki_protection
    def put_sync(self, item):
        """
        Like put(), but synchronous
        """

        evt: AsyncThreadEvent | None = None
        with self._lock:
            if self.maxsize and self.maxsize == len(self.container):
                evt = AsyncThreadEvent()
                self.putters.append(evt)
            if self.getters:
                self.getters.popleft().set()
        if evt:
            evt.wait_sync()
        self.container.append(item)

    @enable_ki_protection
    def get_sync(self):
        """
        Like get(), but synchronous
        """

        evt: AsyncThreadEvent | None = None
        with self._lock:
            if not self.container:
                self.getters.append(AsyncThreadEvent())
                evt = self.getters[-1]
            if self.putters:
                self.putters.popleft().set()
        if evt:
            evt.wait_sync()
        return self.container.popleft()


# Just a bunch of private helpers to run sync/async functions


def _threaded_runner(
    f,
    parent_loop: BaseKernel,
    rq: AsyncThreadQueue,
    rsq: AsyncThreadQueue,
    evt: AsyncThreadEvent,
    *args,
):
    try:
        # Setup thread-local storage so future calls
        # to run_coro() can find this stuff
        _storage.parent_loop = parent_loop
        _storage.rq = rq
        _storage.rsq = rsq
        result = f(*args)
    except BaseException as e:
        rsq.put_sync((False, e))
    else:
        rsq.put_sync((True, result))
    finally:
        # Notify the event loop that the thread
        # has exited
        evt.set()


@enable_ki_protection
async def _coroutine_request_handler(
    events: AsyncThreadQueue, results: AsyncThreadQueue
):
    """
    Runs coroutines on behalf of a thread spawned by structio and
    submits the outcome back to the thread
    """

    while True:
        data = await events.get()
        if not data:
            break
        coro = data
        try:
            result = await coro
        except BaseException as e:
            await results.put((False, e))
        else:
            await results.put((True, result))


@enable_ki_protection
async def _wait_for_thread(
    events: AsyncThreadQueue,
    results: AsyncThreadQueue,
    termination_event: AsyncThreadEvent,
    cancellable: bool = False,
):
    """
    Waits for a thread spawned by structio to complete and
    returns its result. Exceptions are also propagated
    """

    async with structio.create_pool() as pool:
        # If the operation is cancellable, then we're not
        # shielded
        pool.scope.shielded = not cancellable
        # Spawn a coroutine to process incoming requests from
        # the new async thread. We can't await it because it
        # needs to run in the background
        pool.spawn(_coroutine_request_handler, events, results)
        # Wait for the thread to terminate
        await termination_event.wait()
        # Worker thread has exited: we no longer need to process
        # any requests, so we shut our request handler down
        await events.put(None)
    # Wait for the final result from the thread
    success, data = await results.get()
    if success:
        return data
    raise data


@enable_ki_protection
async def _spawn_supervised_thread(f, cancellable: bool = False, *args):
    # Thread termination event
    terminate = AsyncThreadEvent()
    # Request queue. This is where the thread
    # sends coroutines to run
    rq = AsyncThreadQueue(0)
    # Results queue. This is where we put the result
    # of the coroutines in the request queue
    rsq = AsyncThreadQueue(0)
    # This looks like a lot of bookkeeping to do synchronization, but it all has a purpose.
    # The termination event is necessary so that _wait_for_thread can know when to shut
    # down (and, by extension, shut down its workers too). The request and result queues
    # are used to send coroutines and their results back and forth when using run_coro from
    # within the "asynchronous thread". Trying to reduce the amount of primitives turns out
    # to be very hard, because we'd have at least 3 different things (_wait_for_thread,
    # _threaded_runner and _coroutine_request_handler) trying to work on the same resources, which is
    # a hellish nightmare to synchronize properly. For example, _coroutine_request_handler *could* just
    # use a single queue for sending data back and forth, but since it runs in a while loop in order to
    # handle more than one request, as soon as it would put any data onto the queue and then go to the
    # next iteration in the loop, it would (likely, but not always, as it depends on how things get
    # scheduled) immediately call get() again, get something out of queue that it doesn't expect and
    # crash horribly. So this separation is necessary to retain my sanity
    threading.Thread(
        target=_threaded_runner,
        args=(f, current_loop(), rq, rsq, terminate, *args),
        # We start cancellable threads in daemonic mode so that
        # the main thread doesn't get stuck waiting on them forever
        # when their associated async counterpart gets cancelled. This
        # is due to the fact that there's really no way to "kill" a thread
        # (and for good reason!), so we just pretend nothing happened and go
        # about our merry way, hoping the thread dies eventually I guess
        name="structio-worker-thread",
        daemon=cancellable,
    ).start()
    return await _wait_for_thread(rq, rsq, terminate, cancellable)


@enable_ki_protection
async def run_in_worker(
    sync_func,
    *args,
    cancellable: bool = False,
):
    """
    Call the given synchronous function in a separate
    worker thread, turning it into an async operation.
    Must be called from an asynchronous context (a
    StructIOException is raised otherwise). The result
    of the call is returned, and any exceptions that occur
    are propagated back to the caller. This is semantically
    identical to just calling the function itself from within
    the async context, but it has the added benefit of 1) Being
    partially cancellable (with a catch, see below) and 2) If
    the function performs some long-running blocking operation,
    calling it in the main thread is not advisable, as it would
    cause structio's event loop to grind to a halt, meaning that
    timeouts and cancellations don't work, I/O doesn't get scheduled,
    and all sorts of nasty things happen (or rather, don't happen,
    since no work is getting done). In short, don't do long-running
    sync calls in the main thread, use a worker. Also, don't do any
    CPU-bound work in it, or you're likely to negatively affect the main
    thread anyway because CPython is weird and likes to starve-out I/O
    bound threads if there's some CPU-bound workers running (for that kind
    of work, you might want to spawn an entire separate process instead).
    Now, onto cancellations: If cancellable equals False, then the operation
    cannot be canceled in any way (this is the default option). This means
    that even if you set a task scope with a timeout or explicitly cancel
    the pool where this function is awaited, its effects won't be visible
    until after the thread has exited. If cancellable equals True, cancellation
    will cause this function to return early and to abruptly drop the thread:
    keep in mind that it is likely to keep running in the background, as
    structio doesn't make any effort to stop it (it can't). If you call this
    with cancellable=True, make sure the operation you're performing is side-effect-free,
    or you might get nasty deadlocks or race conditions happening.

    Note: If the number of current active thread workers is equal to the value of get_max_worker_count(),
    this function blocks until a slot is available and then proceeds normally.

    """

    if not hasattr(_storage, "parent_loop"):
        _storage.parent_loop = current_loop()
    else:
        try:
            current_loop()
        except StructIOException:
            raise StructIOException("cannot be called from sync context")
    # This will automatically block once
    # we run out of slots and proceed once
    # we have more
    async with _storage.max_workers:
        return await _spawn_supervised_thread(sync_func, cancellable, *args)


@enable_ki_protection
def run_coro(
    async_func: Callable[[Any, Any], Coroutine[Any, Any, Any]], *args, **kwargs
):
    """
    Submits a coroutine for execution to the event loop, passing any
    arguments along the way. Return values and exceptions are propagated
    and from the point of view of the calling thread, this call blocks
    until the coroutine returns
    """

    try:
        current_loop()
        raise StructIOException("cannot be called from async context")
    except StructIOException:
        pass
    if not hasattr(_storage, "parent_loop"):
        raise StructIOException("run_coro requires a running loop in another thread!")
    _storage.rq.put_sync(async_func(*args, **kwargs))
    success, data = _storage.rsq.get_sync()
    if success:
        return data
    raise data


def set_max_worker_count(count: int):
    """
    Sets a new value for the maximum number of concurrent
    worker threads structio is allowed to spawn
    """

    # Everything, to avoid the unholy "global"
    _storage.max_workers = Semaphore(count)


def get_max_worker_count() -> int:
    """
    Gets the maximum number of concurrent worker
    threads structio is allowed to spawn
    """

    return _storage.max_workers.max_size
