import io
import os
from abc import abstractmethod, ABC
from structio.core.task import Task
from structio.exceptions import StructIOException
from typing import Callable, Any, Coroutine
from types import FrameType


class BaseClock(ABC):
    """
    Abstract base clock class
    """

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def start(self):
        return NotImplemented

    @abstractmethod
    def setup(self):
        return NotImplemented

    @abstractmethod
    def teardown(self):
        return NotImplemented

    @abstractmethod
    def current_time(self):
        return NotImplemented

    @abstractmethod
    def deadline(self, deadline):
        return NotImplemented


class AsyncResource(ABC):
    """
    A generic asynchronous resource which needs to
    be closed properly, possibly blocking. Can be
    used as a context manager (note that only the
    __aexit__ method actually blocks!)
    """

    async def __aenter__(self):
        return self

    @abstractmethod
    async def close(self):
        return NotImplemented

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


class StreamWriter(AsyncResource, ABC):
    """
    Interface for writing binary data to
    a byte stream
    """

    @abstractmethod
    async def write(self, data):
        return NotImplemented


class StreamReader(AsyncResource, ABC):
    """
    Interface for reading binary data from
    a byte stream. The stream implements the
    asynchronous iterator protocol and can
    therefore be used with "async for" loops
    """

    @abstractmethod
    async def _read(self, size: int = -1):
        return NotImplemented


class Stream(StreamReader, StreamWriter, ABC):
    """
    A generic, asynchronous, readable/writable binary stream
    """

    def __init__(self, f):
        if isinstance(f, io.TextIOBase):
            raise TypeError("only binary files can be streamed")
        self.fileobj = f
        self.buf = bytearray()
        os.set_blocking(self.fileobj.fileno(), False)

    @abstractmethod
    async def flush(self):
        """
        Flushes the underlying resource asynchronously
        """

        return NotImplemented


class WriteCloseableStream(Stream, ABC):
    """
    Extension to the Stream class that allows
    shutting down the write end of the stream
    without closing the read side on our end
    nor the read/write side on the other one
    """

    @abstractmethod
    async def eof(self):
        """
        Send an end-of-file on this stream, if possible.
        The resource can still be read from (and the
        other end can still read/write to it), but no more
        data can be written after an EOF has been sent. If an
        EOF has already been sent, this method is a no-op
        """


class ChannelReader(AsyncResource, ABC):
    """
    Interface for reading data from a
    channel
    """

    @abstractmethod
    async def receive(self):
        """
        Receive an object from the channel,
        possibly blocking
        """

        return NotImplemented

    @abstractmethod
    def pending(self):
        """
        Returns if there is any data waiting
        to be read
        """

    @abstractmethod
    def readers(self):
        """
        Returns how many tasks are waiting to
        read from the channel
        """


class ChannelWriter(AsyncResource, ABC):
    """
    Interface for writing data to a
    channel
    """

    @abstractmethod
    async def send(self, value):
        """
        Send the given object on the channel,
        possibly blocking
        """

        return NotImplemented

    @abstractmethod
    def writers(self):
        """
        Returns how many tasks are waiting
        to write to the channel
        """


class Channel(ChannelWriter, ChannelReader, ABC):
    """
    A generic, two-way channel
    """


class BaseDebugger(ABC):
    """
    The base for all debugger objects
    """

    def on_start(self):
        """
        This method is called when the event
        loop starts executing
        """

        return NotImplemented

    def on_exit(self):
        """
        This method is called when the event
        loop exits entirely (all tasks completed)
        """

        return NotImplemented

    def on_task_schedule(self, task: Task, delay: float):
        """
        This method is called when a new task is
        scheduled (not spawned)

        :param task: The Task that was (re)scheduled
        :type task: :class: structio.objects.Task
        :param delay: The delay, in seconds, after which
            the task will start executing
        :type delay: float
        """

        return NotImplemented

    def on_task_spawn(self, task: Task):
        """
        This method is called when a new task is
        spawned

        :param task: The Task that was spawned
        :type task: :class: structio.objects.Task
        """

        return NotImplemented

    def on_task_exit(self, task: Task):
        """
        This method is called when a task exits

        :param task: The Task that exited
        :type task: :class: structio.objects.Task
        """

        return NotImplemented

    def before_task_step(self, task: Task):
        """
        This method is called right before
        calling a task's run() method

        :param task: The Task that is about to run
        :type task: :class: structio.objects.Task
        """

        return NotImplemented

    def after_task_step(self, task: Task):
        """
        This method is called right after
        calling a task's run() method

        :param task: The Task that has ran
        :type task: :class: structio.objects.Task
        """

        return NotImplemented

    def before_sleep(self, task: Task, seconds: float):
        """
        This method is called before a task goes
        to sleep

        :param task: The Task that is about to sleep
        :type task: :class: structio.objects.Task
        :param seconds: The amount of seconds the
            task wants to sleep for
        :type seconds: int
        """

        return NotImplemented

    def after_sleep(self, task: Task, seconds: float):
        """
        This method is called after a tasks
        awakes from sleeping

        :param task: The Task that has just slept
        :type task: :class: structio.objects.Task
        :param seconds: The amount of seconds the
            task slept for
        :type seconds: float
        """

        return NotImplemented

    def before_io(self, timeout: float):
        """
        This method is called right before
        the event loop checks for I/O events

        :param timeout: The max. amount of seconds
            that the loop will hang for while waiting
            for I/O events
        :type timeout: float
        """

        return NotImplemented

    def after_io(self, timeout: float):
        """
        This method is called right after
        the event loop has checked for I/O events

        :param timeout: The actual amount of seconds
            that the loop has hung for while waiting
            for I/O events
        :type timeout: float
        """

        return NotImplemented

    def before_cancel(self, task: Task):
        """
        This method is called right before a task
        gets cancelled

        :param task: The Task that is about to be cancelled
        :type task: :class: structio.objects.Task
        """

        return NotImplemented

    def after_cancel(self, task: Task) -> object:
        """
        This method is called right after a task
        gets successfully cancelled

        :param task: The Task that was cancelled
        :type task: :class: structio.objects.Task
        """

        return NotImplemented

    def on_exception_raised(self, task: Task, exc: BaseException):
        """
        This method is called right after a task
        has raised an exception

        :param task: The Task that raised the error
        :type task: :class: structio.objects.Task
        :param exc: The exception that was raised
        :type exc: BaseException
        """

        return NotImplemented

    def on_io_schedule(self, stream, event: int):
        """
        This method is called whenever an
        I/O resource is scheduled for listening
        """

        return NotImplemented

    def on_io_unschedule(self, stream):
        """
        This method is called whenever a stream
        is unregistered from the loop's I/O selector
        """

        return NotImplemented


class BaseIOManager(ABC):
    """
    Base class for all I/O managers
    """

    @abstractmethod
    def wait_io(self):
        """
        Waits for I/O and reschedules tasks
        when data is ready to be read/written
        """

        return NotImplemented

    @abstractmethod
    def request_read(self, rsc, task: Task):
        """
        "Requests" a read operation on the given
        resource to the I/O manager from the given
        task
        """

        return NotImplemented

    @abstractmethod
    def request_write(self, rsc, task: Task):
        """
        "Requests" a write operation on the given
        resource to the I/O manager from the given
        task
        """

        return NotImplemented

    @abstractmethod
    def pending(self):
        """
        Returns whether there's any tasks waiting
        to read from/write to a resource registered
        in the manager
        """

        return NotImplemented

    @abstractmethod
    def release(self, resource):
        """
        Releases the given async resource from the
        manager. Note that the resource is *not*
        closed!
        """

        return NotImplemented

    @abstractmethod
    def release_task(self, task: Task):
        """
        Releases ownership of the given
        resource from the given task. Note
        that if the resource is being used by
        other tasks that this method will
        not unschedule it for those as well
        """

        return NotImplemented

    @abstractmethod
    def get_reader(self, rsc):
        """
        Returns the task reading from the given
        resource, if any (None otherwise)
        """

    @abstractmethod
    def get_writer(self, rsc):
        """
        Returns the task writing to the given
        resource, if any (None otherwise)
        """


class SignalManager(ABC):
    """
    A signal manager
    """

    @abstractmethod
    def handle(self, sig: int, frame: FrameType):
        """
        Handles the signal
        """

        return NotImplemented

    @abstractmethod
    def install(self):
        """
        Installs the signal handler
        """

        return NotImplemented

    @abstractmethod
    def uninstall(self):
        """
        Uninstalls the signal handler
        """

        return NotImplemented


class BaseKernel(ABC):
    """
    Abstract kernel base class
    """

    def __init__(
        self,
        clock: BaseClock,
        io_manager: BaseIOManager,
        signal_managers: list[SignalManager],
        tools: list[BaseDebugger] | None = None,
        restrict_ki_to_checkpoints: bool = False,
    ):
        self.clock = clock
        self.current_task: Task | None = None
        self.current_pool: "TaskPool" = None
        self.current_scope: "TaskScope" = None
        self.tools: list[BaseDebugger] = tools or []
        self.restrict_ki_to_checkpoints: bool = restrict_ki_to_checkpoints
        self.io_manager = io_manager
        self.signal_managers = signal_managers
        self.entry_point: Task | None = None
        # Pool for system tasks
        self.pool: "TaskPool" = None

    @abstractmethod
    def wait_readable(self, resource: AsyncResource):
        """
        Schedule the given resource for reading from
        the current task
        """

        return NotImplemented

    @abstractmethod
    def wait_writable(self, resource: AsyncResource):
        """
        Schedule the given resource for reading from
        the current task
        """

        return NotImplemented

    @abstractmethod
    def release_resource(self, resource: AsyncResource):
        """
        Releases the given resource from the scheduler
        """

        return NotImplemented

    @abstractmethod
    def notify_closing(self, resource: AsyncResource, broken: bool = False, owner: Task | None = None):
        """
        Notifies the event loop that a given resource
        is about to be closed and can be unscheduled
        """

        return NotImplemented

    @abstractmethod
    def cancel_task(self, task: Task):
        """
        Cancels the given task individually
        """

        return NotImplemented

    @abstractmethod
    def signal_notify(self, sig: int, frame: FrameType):
        """
        Notifies the event loop that a signal was
        received. If the signal was supposed to trigger
        any exceptions (i.e. SIGINT -> KeyboardInterrupt),
        this handler being called means the current context
        does not allow for an exception to be raised right
        now. Implementors should make sure to remember that
        this method was called and to deliver the appropriate
        exception as soon as possible
        """

        return NotImplemented

    @abstractmethod
    def spawn(self, func: Callable[[Any, Any], Coroutine[Any, Any, Any]], *args):
        """
        Readies a task for execution. All positional arguments are passed
        to the given coroutine (for keyword arguments, use functools.partial)
        """

        return NotImplemented

    @abstractmethod
    def spawn_system_task(
        self, func: Callable[[Any, Any], Coroutine[Any, Any, Any]], *args
    ):
        """
        Spawns a system task. System tasks run in a special internal
        task pool and begin execution in a scope shielded by cancellations
        and with Ctrl+C protection enabled
        """

        return NotImplemented

    @abstractmethod
    def get_closest_deadline(self):
        """
        Returns the closest deadline to be satisfied
        """

        return NotImplemented

    @abstractmethod
    def setup(self):
        """
        This method is called right before startup and can
        be used by implementors to perform extra setup before
        starting the event loop
        """

    @abstractmethod
    def teardown(self):
        """
        This method is called right before exiting, even
        if an error occurred, and can be used by implementors
        to perform extra cleanup before terminating the event loop
        """

    @abstractmethod
    def throw(self, task: Task, err: BaseException):
        """
        Throws the given exception into the given
        task
        """

        return NotImplemented

    @abstractmethod
    def reschedule(self, task: Task):
        """
        Reschedules the given task for further
        execution
        """

        return NotImplemented

    @abstractmethod
    def event(self, evt_name, *args):
        """
        Fires the specified event for every registered tool
        in the event loop
        """

        return NotImplemented

    @abstractmethod
    def run(self):
        """
        This is the actual "loop" part
        of the "event loop"
        """

        return NotImplemented

    @abstractmethod
    def sleep(self, amount):
        """
        Puts the current task to sleep for the given amount of
        time as defined by our current clock
        """

        return NotImplemented

    @abstractmethod
    def suspend(self):
        """
        Suspends the current task until it is rescheduled
        """

        return NotImplemented

    @abstractmethod
    def get_closest_deadline_owner(self) -> Task:
        """
        Similar to get_closest_deadline, but it returns
        the task which will be rescheduled instead of its
        deadline
        """

        return NotImplemented

    @abstractmethod
    def init_scope(self, scope):
        """
        Initializes the given task scope (called by
        TaskScope.__enter__)
        """

        return NotImplemented

    @abstractmethod
    def close_scope(self, scope):
        """
        Closes the given task scope (called by
        TaskScope.__exit__)
        """

        return NotImplemented

    @abstractmethod
    def init_pool(self, pool):
        """
        Initializes the given task pool (called by
        TaskPool.__aenter__)
        """

        return NotImplemented

    @abstractmethod
    def close_pool(self, pool):
        """
        Closes the given task pool (called by
        TaskPool.__aexit__)
        """

        return NotImplemented

    @abstractmethod
    def cancel_scope(self, scope):
        """
        Cancels the given scope
        """

        return NotImplemented

    def start(self, entry_point: Callable[[Any, Any], Coroutine[Any, Any, Any]], *args):
        """
        Starts the event loop from a synchronous entry
        point. This method only returns once execution
        has finished. Normally, this method doesn't need
        to be overridden: consider using setup() and teardown()
        if you need to do some operations before startup/teardown
        """

        self.setup()
        self.event("on_start")
        self.current_pool = self.pool
        self.entry_point = self.spawn(entry_point, *args)
        self.current_pool.scope.owner = self.entry_point
        self.entry_point.pool = self.current_pool
        self.current_pool.entry_point = self.entry_point
        self.current_scope = self.current_pool.scope
        try:
            self.run()
        finally:
            self.teardown()
            self.close(force=True)
        if self.entry_point.exc:
            raise self.entry_point.exc
        self.event("on_exit")
        return self.entry_point.result

    @abstractmethod
    def done(self):
        """
        Returns whether the loop has work to do
        """

        return NotImplemented

    def close(self, force: bool = False):
        """
        Terminates and shuts down the event loop
        This method is meant to be extended by
        implementations to do their own cleanup

        :param force: When force equals false,
            the default, and the event loop is
            not done, this function raises a
            StructIOException
        """

        if not self.done() and not force:
            raise StructIOException("the event loop is running")
