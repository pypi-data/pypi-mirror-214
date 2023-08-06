import traceback
import warnings
from types import FrameType
from structio.abc import (
    BaseKernel,
    BaseClock,
    BaseDebugger,
    BaseIOManager,
    SignalManager,
)
from structio.io import FdWrapper
from structio.core.context import TaskPool, TaskScope
from structio.core.task import Task, TaskState
from structio.util.ki import CTRLC_PROTECTION_ENABLED
from structio.core.time.queue import TimeQueue
from structio.exceptions import StructIOException, Cancelled, TimedOut, ResourceClosed, ResourceBroken
from collections import deque
from typing import Callable, Coroutine, Any
from functools import partial
import signal
import sniffio


class FIFOKernel(BaseKernel):
    """
    An asynchronous event loop implementation
    with a FIFO scheduling policy
    """

    def __init__(
        self,
        clock: BaseClock,
        io_manager: BaseIOManager,
        signal_managers: list[SignalManager],
        tools: list[BaseDebugger] | None = None,
        restrict_ki_to_checkpoints: bool = False,
    ):
        super().__init__(
            clock, io_manager, signal_managers, tools, restrict_ki_to_checkpoints
        )
        self.skip: bool = False
        # Tasks that are ready to run
        self.run_queue: deque[Task] = deque()
        # Data to send back to tasks
        self.data: dict[Task, Any] = {}
        # Have we handled SIGINT?
        self._sigint_handled: bool = False
        # Paused tasks along with their deadlines
        self.paused: TimeQueue = TimeQueue(self.clock)
        # All task scopes we handle
        self.scopes: list[TaskScope] = []
        self.pool = TaskPool()
        self.current_pool = self.pool
        self.current_scope = self.current_pool.scope
        self.current_scope.shielded = False
        self.scopes.append(self.current_scope)
        self._closing = False

    def get_closest_deadline(self):
        return min(
            [
                self.current_scope.get_actual_timeout(),
                self.paused.get_closest_deadline(),
            ]
        )

    def wait_readable(self, resource: FdWrapper):
        self.io_manager.request_read(resource, self.current_task)

    def wait_writable(self, resource: FdWrapper):
        self.io_manager.request_write(resource, self.current_task)

    def notify_closing(self, resource: FdWrapper, broken: bool = False, owner: Task | None = None):
        if not broken:
            exc = ResourceClosed("stream has been closed")
        else:
            exc = ResourceBroken("stream might be corrupted")
        owner = owner or self.current_task
        reader = self.io_manager.get_reader(resource)
        writer = self.io_manager.get_writer(resource)
        if reader and reader is not owner:
            self.throw(reader, exc)
        if writer and writer is not owner:
            self.throw(writer, exc)
        self.reschedule_running()

    def get_closest_deadline_owner(self):
        return self.paused.peek()

    def event(self, evt_name: str, *args):
        if not hasattr(BaseDebugger, evt_name):
            warnings.warn(f"Invalid debugging event fired: {evt_name!r}")
            return
        for tool in self.tools:
            if f := getattr(tool, evt_name, None):
                try:
                    f(*args)
                except BaseException as e:
                    # We really can't afford to have our internals explode,
                    # sorry!
                    warnings.warn(
                        f"Exception during debugging event delivery in {f!r} ({evt_name!r}): {type(e).__name__} -> {e}",
                    )
                    traceback.print_tb(e.__traceback__)
                    # We disable the tool, so it can't raise at the next debugging
                    # event
                    self.tools.remove(tool)

    def done(self):
        if self.entry_point.done():
            return True
        if any([self.run_queue, self.paused, self.io_manager.pending()]):
            return False
        for scope in self.scopes:
            if not scope.done():
                return False
        return True

    def spawn(self, func: Callable[[Any, Any], Coroutine[Any, Any, Any]], *args):
        if isinstance(func, partial):
            name = func.func.__name__ or repr(func.func)
        else:
            name = func.__name__ or repr(func)
        task = Task(name, func(*args), self.current_pool)
        # We inject our magic secret variable into the coroutine's stack frame, so
        # we can look it up later
        task.coroutine.cr_frame.f_locals.setdefault(CTRLC_PROTECTION_ENABLED, False)
        task.pool.scope.tasks.append(task)
        self.run_queue.append(task)
        self.event("on_task_spawn")
        return task

    def spawn_system_task(
        self, func: Callable[[Any, Any], Coroutine[Any, Any, Any]], *args
    ):
        if isinstance(func, partial):
            name = func.func.__name__ or repr(func.func)
        else:
            name = func.__name__ or repr(func)
        task = Task(name, func(*args), self.pool)
        task.coroutine.cr_frame.f_locals.setdefault(CTRLC_PROTECTION_ENABLED, True)
        task.pool.scope.tasks.append(task)
        self.run_queue.append(task)
        self.event("on_task_spawn")
        return task

    def signal_notify(self, sig: int, frame: FrameType):
        match sig:
            case signal.SIGINT:
                self._sigint_handled = True
            case _:
                pass

    def step(self):
        """
        Run a single task step (i.e. until an "await" to our
        primitives somewhere)
        """

        self.current_task = self.run_queue.popleft()
        while self.current_task.done():
            if not self.run_queue:
                return
            self.current_task = self.run_queue.popleft()
        runner = partial(
            self.current_task.coroutine.send, self.data.pop(self.current_task, None)
        )
        if self.current_task.pending_cancellation:
            _runner = partial(self.current_task.coroutine.throw, Cancelled())
        elif self._sigint_handled:
            self._sigint_handled = False
            runner = partial(self.current_task.coroutine.throw, KeyboardInterrupt())
        self.event("before_task_step", self.current_task)
        self.current_task.state = TaskState.RUNNING
        method, args, kwargs = runner()
        if not callable(getattr(self, method, None)):
            # This if block is meant to be triggered by other async
            # libraries, which most likely have different method names and behaviors
            # compared to us. If you get this exception, and you're 100% sure you're
            # not mixing async primitives from other libraries, then it's a bug!
            self.throw(
                self.current_task,
                StructIOException(
                    "Uh oh! Something bad just happened: did you try to mix "
                    "primitives from other async libraries?"
                ),
            )
        # Sneaky method call, thanks to David Beazley for this ;)
        getattr(self, method)(*args, **kwargs)
        self.event("after_task_step", self.current_task)

    def throw(self, task: Task, err: BaseException):
        if task.done():
            return
        if self.current_scope.shielded:
            return
        if task.state == TaskState.PAUSED:
            self.paused.discard(task)
        elif task.state == TaskState.IO:
            self.io_manager.release_task(task)
        self.handle_errors(partial(task.coroutine.throw, err), task)

    def reschedule(self, task: Task):
        if task.done() or task in self.run_queue:
            return
        self.run_queue.append(task)

    def check_cancelled(self):
        if self._sigint_handled:
            self.throw(self.entry_point, KeyboardInterrupt())
        elif self.current_task.pending_cancellation:
            self.cancel_task(self.current_task)
        else:
            # We reschedule the caller immediately!
            self.run_queue.appendleft(self.current_task)

    def schedule_point(self):
        self.skip = True
        self.reschedule_running()

    def sleep(self, amount):
        """
        Puts the current task to sleep for the given amount of
        time as defined by our current clock
        """

        # Just to avoid code duplication, you know
        self.suspend()
        if amount > 0:
            self.event("before_sleep", self.current_task, amount)
            self.current_task.next_deadline = self.clock.deadline(amount)
            self.paused.put(self.current_task, amount)
        else:
            # If sleep is called with 0 as argument,
            # then it's just a checkpoint!
            self.skip = True
            self.reschedule_running()

    def check_scopes(self):
        for scope in self.scopes:
            if scope.get_actual_timeout() <= self.clock.current_time():
                error = TimedOut("timed out")
                error.scope = scope
                self.throw(scope.owner, error)

    def wakeup(self):
        while (
            self.paused
            and self.paused.peek().next_deadline <= self.clock.current_time()
        ):
            task, _ = self.paused.get()
            task.next_deadline = 0
            self.event(
                "after_sleep", task, task.paused_when - self.clock.current_time()
            )
            self.reschedule(task)

    def run(self):
        """
        This is the actual "loop" part
        of the "event loop"
        """

        while not self.done():
            if self.run_queue and not self.skip:
                self.handle_errors(self.step)
            self.skip = False
            if self._sigint_handled and not self.restrict_ki_to_checkpoints:
                self.throw(self.entry_point, KeyboardInterrupt())
            if self.io_manager.pending():
                self.io_manager.wait_io()
            self.wakeup()
            self.check_scopes()
        self.close()

    def reschedule_running(self):
        """
        Reschedules the currently running task
        """

        self.reschedule(self.current_task)

    def handle_errors(self, func: Callable, task: Task | None = None):
        """
        Convenience method for handling various exceptions
        from tasks
        """

        old_name, sniffio.thread_local.name = sniffio.thread_local.name, "structured-io"
        try:
            func()
        except StopIteration as ret:
            # We re-define it because we call step() with
            # this method and that changes the current task
            task = task or self.current_task
            # At the end of the day, coroutines are generator functions with
            # some tricky behaviors, and this is one of them. When a coroutine
            # hits a return statement (either explicit or implicit), it raises
            # a StopIteration exception, which has an attribute named value that
            # represents the return value of the coroutine, if it has one. Of course
            # this exception is not an error, and we should happily keep going after it:
            # most of this code below is just useful for internal/debugging purposes
            task.state = TaskState.FINISHED
            task.result = ret.value
            self.on_success(task)
        except Cancelled:
            # When a task needs to be cancelled, we try to do it gracefully first:
            # if the task is paused in either I/O or sleeping, that's perfect.
            # But we also need to cancel a task if it was not sleeping or waiting on
            # any I/O because it could never do so (therefore blocking everything
            # forever). So, when cancellation can't be done right away, we schedule
            # it for the next execution step of the task. We will also make sure
            # to re-raise cancellations at every checkpoint until the task lets the
            # exception propagate into us, because we *really* want the task to be
            # cancelled
            task = task or self.current_task
            task.state = TaskState.CANCELLED
            task.pending_cancellation = False
            self.event("after_cancel")
            self.on_cancel(task)
        except (Exception, KeyboardInterrupt) as err:
            # Any other exception is caught here
            task = task or self.current_task
            task.exc = err
            err.scope = task.pool.scope
            task.state = TaskState.CRASHED
            self.event("on_exception_raised", task)
            self.on_error(task)
        finally:
            sniffio.thread_local.name = old_name

    def release_resource(self, resource: FdWrapper):
        self.io_manager.release(resource)
        self.reschedule_running()

    def release(self, task: Task):
        """
        Releases the timeouts and associated
        I/O resourced that the given task owns
        """

        self.io_manager.release_task(task)
        self.paused.discard(task)

    def on_success(self, task: Task):
        """
        The given task has exited gracefully: hooray!
        """

        # TODO: Anything else?
        task.pool: TaskPool
        for waiter in task.waiters:
            self.reschedule(waiter)
        if task.pool.done():
            self.reschedule(task.pool.entry_point)
        task.waiters.clear()
        self.event("on_task_exit", task)
        self.io_manager.release_task(task)

    def on_error(self, task: Task):
        """
        The given task raised an exception
        """

        self.event("on_exception_raised", task, task.exc)
        for waiter in task.waiters:
            self.reschedule(waiter)
        self.throw(task.pool.scope.owner, task.exc)
        task.waiters.clear()
        self.release(task)

    def on_cancel(self, task: Task):
        """
        The given task crashed because of a
        cancellation exception
        """

        for waiter in task.waiters:
            self.reschedule(waiter)
        task.waiters.clear()
        self.release(task)
        if task.pool.done():
            self.reschedule(task.pool.entry_point)

    def init_scope(self, scope: TaskScope):
        scope.owner = self.current_task
        self.current_scope.inner = scope
        scope.outer = self.current_scope
        self.current_scope = scope
        self.scopes.append(scope)

    def close_scope(self, scope: TaskScope):
        self.current_scope = scope.outer
        self.scopes.pop()

    def cancel_task(self, task: Task):
        if task.done():
            return
        err = Cancelled()
        err.scope = task.pool.scope
        self.throw(task, err)
        if task.state != TaskState.CANCELLED:
            task.pending_cancellation = True

    def cancel_scope(self, scope: TaskScope):
        scope.attempted_cancel = True
        inner = scope.inner
        if inner and not inner.shielded:
            self.cancel_scope(inner)
        for task in scope.tasks.copy():
            # We make a copy of the list because we
            # need to make sure that tasks aren't
            # removed out from under us
            self.cancel_task(task)
        if scope.done():
            self.reschedule(scope.owner)

    def init_pool(self, pool: TaskPool):
        pool.outer = self.current_pool
        pool.entry_point = self.current_task
        self.current_pool.inner = pool
        self.current_pool = pool

    def close_pool(self, pool: TaskPool):
        self.current_pool = pool.outer

    def suspend(self):
        self.current_task.state = TaskState.PAUSED
        self.current_task.paused_when = self.clock.current_time()

    def setup(self):
        for manager in self.signal_managers:
            manager.install()

    def teardown(self):
        for manager in self.signal_managers:
            manager.uninstall()
