from typing import Any
from structio.core.task import Task, TaskState
from structio.abc import BaseClock
from heapq import heappush, heappop, heapify


class TimeQueue:
    """
    An abstraction layer over a heap queue based on time. This is where
    paused tasks will be put when they are not running

    :param clock: The same clock that was passed to the thread-local event loop.
        It is important for the queue to be synchronized with the loop as this allows
        the sleeping mechanism to work reliably
    """

    def __init__(self, clock: BaseClock):
        """
        Object constructor
        """

        self.clock = clock
        # The sequence float handles the race condition
        # of two tasks with identical deadlines, acting
        # as a tiebreaker
        self.sequence = 0
        self.container: list[tuple[float, int, Task, dict[str, Any]]] = []

    def peek(self) -> Task:
        """
        Returns the first task in the queue
        """

        return self.container[0][2]

    def __len__(self):
        """
        Returns len(self)
        """

        return len(self.container)

    def __contains__(self, item: Task):
        """
        Implements item in self. This method behaves
        as if the queue only contained tasks and ignores
        their timeouts and tiebreakers
        """

        for i in self.container:
            if i[2] == item:
                return True
        return False

    def index(self, item: Task):
        """
        Returns the index of the given item in the list
        or -1 if it is not present
        """

        for i, e in enumerate(self.container):
            if e[2] == item:
                return i
        return -1

    def discard(self, item: Task):
        """
        Discards an item from the queue and
        calls heapify(self.container) to keep
        the heap invariant if an element is removed.
        This method does nothing if the item is not
        in the queue, but note that in this case the
        operation would still take O(n) iterations
        to complete

        :param item: The item to be discarded
        """

        idx = self.index(item)
        if idx != -1:
            self.container.pop(idx)
            heapify(self.container)

    def get_closest_deadline(self) -> float:
        """
        Returns the closest deadline that is meant to expire
        """

        if not self:
            return float("inf")
        return self.container[0][0]

    def __iter__(self):
        """
        Implements iter(self)
        """

        return self

    def __next__(self):
        """
        Implements next(self)
        """

        try:
            return self.get()
        except IndexError:
            raise StopIteration from None

    def __getitem__(self, item: int):
        """
        Implements self[n]
        """

        return self.container.__getitem__(item)

    def __bool__(self):
        """
        Implements bool(self)
        """

        return bool(self.container)

    def __repr__(self):
        """
        Implements repr(self) and str(self)
        """

        return f"TimeQueue({self.container}, clock={self.clock})"

    def put(self, task: Task, delay: float, metadata: dict[str, Any] | None = None):
        """
        Pushes a task onto the queue together with its
        delay and optional metadata

        :param task: The task that is meant to sleep
        :type task: :class: Task
        :param delay: The delay associated with the task
        :type delay: float
        :param metadata: A dictionary representing additional
            task metadata. Defaults to None
        :type metadata: dict[str, Any], optional
        """

        time = self.clock.current_time()
        task.paused_when = time
        task.state = TaskState.PAUSED
        task.next_deadline = task.paused_when + delay
        heappush(self.container, (time + delay, self.sequence, task, metadata))
        self.sequence += 1

    def get(self) -> tuple[Task, dict[str, Any] | None]:
        """
        Gets the first task that is meant to run along
        with its metadata

        :raises: IndexError if the queue is empty
        """

        if not self.container:
            raise IndexError("get from empty TimeQueue")
        _, __, task, meta = heappop(self.container)
        return task, meta
