import structio
from structio.core.run import current_loop
from structio.core.task import Task
from structio.core.syscalls import suspend, checkpoint
from typing import Callable, Coroutine, Any
from structio.exceptions import Cancelled, StructIOException


class TaskScope:
    """
    A task scope
    """

    def __init__(
        self,
        timeout: int | float | None = None,
        silent: bool = False,
        shielded: bool = False,
    ):
        """
        Public object constructor
        """

        # When do we expire?
        self.timeout = timeout or float("inf")
        # Do we raise an error on timeout?
        self.silent = silent
        # Has a cancellation attempt been done?
        self.attempted_cancel: bool = False
        # Have we been cancelled?
        self.cancelled: bool = False
        # Can we be indirectly cancelled? Note that this
        # does not affect explicit cancellations via the
        # cancel() method
        self.shielded: bool = shielded
        # Data about inner and outer scopes.
        # This is used internally to make sure
        # nesting task scopes works as expected
        self.inner: TaskScope | None = None
        self.outer: TaskScope | None = None
        # Which tasks do we contain?
        self.tasks: list[Task] = []
        self.owner: Task | None = None

    def cancel(self):
        """
        Cancels the task scope and all the work
        that belongs to it
        """

        current_loop().cancel_scope(self)

    def get_actual_timeout(self):
        """
        Returns the effective timeout of the whole
        cancel scope. This is different from the
        self.timeout parameter because cancel scopes
        can be nested, and we might have a parent with
        a lower timeout than us
        :return:
        """

        if self.outer is None:
            return self.timeout
        current = self.inner
        while current:
            if current.shielded:
                return float("inf")
            current = current.inner
        return min([self.timeout, self.outer.get_actual_timeout()])

    def __enter__(self):
        self.timeout = current_loop().clock.deadline(self.timeout)
        current_loop().init_scope(self)
        return self

    def __exit__(self, exc_type: type, exc_val: BaseException, exc_tb):
        current_loop().close_scope(self)
        if exc_val and isinstance(exc_val, structio.TimedOut):
            self.cancelled = True
            return self.silent
        return False

    def done(self):
        """
        Returns whether the task scope has finished executing
        """

        if self.inner and not self.inner.done():
            return False
        return all(task.done() for task in self.tasks)


class TaskPool:
    """
    A task pool
    """

    def __init__(self):
        """
        Public object constructor
        """

        self.entry_point: Task | None = None
        self.scope: TaskScope = TaskScope(timeout=float("inf"))
        # Data about inner and outer pools.
        # This is used internally to make sure
        # nesting task pools works as expected
        self.inner: TaskPool | None = None
        self.outer: TaskPool | None = None
        # Have we errored out?
        self.error: BaseException | None = None
        # Have we exited? This is so we can forbid reuse of
        # dead task pools
        self._closed: bool = False

    async def __aenter__(self):
        if self._closed:
            raise StructIOException("task pool is closed")
        self.scope.__enter__()
        current_loop().init_pool(self)
        return self

    async def __aexit__(self, exc_type: type, exc_val: BaseException, exc_tb):
        try:
            if exc_val:
                await checkpoint()
                raise exc_val.with_traceback(exc_tb)
            elif not self.done():
                await suspend()
        except Cancelled as e:
            self.error = e
            self.scope.cancelled = True
        except (Exception, KeyboardInterrupt) as e:
            self.error = e
            self.scope.cancel()
        finally:
            current_loop().close_pool(self)
            self.scope.__exit__(exc_type, exc_val, exc_tb)
            self._closed = True
            if self.error:
                raise self.error

    def done(self):
        """
        Returns whether the task pool has finished executing
        """

        return self.scope.done()

    def spawn(
        self, func: Callable[[Any, Any], Coroutine[Any, Any, Any]], *args
    ) -> Task:
        """
        Schedule a new concurrent task for execution in the task pool from the given
        async function. All positional arguments are passed to the underlying coroutine
        (for keyword arguments, consider using functools.partial). A Task object is
        returned. Note that the coroutine is merely scheduled to run and does not begin
        executing until it is picked by the scheduler later on
        """

        return current_loop().spawn(func, *args)
