from structio.abc import BaseIOManager, BaseKernel
from structio.core.task import Task, TaskState
from structio.core.run import current_loop, current_task
from structio.io import FdWrapper
import select


class SimpleIOManager(BaseIOManager):
    """
    A simple, cross-platform, select()-based
    I/O manager. This class is only meant to
    be used as a default fallback and is quite
    inefficient and slower compared to more ad-hoc
    alternatives such as epoll or kqueue (it should
    work on most platforms though)
    """

    def __init__(self):
        """
        Public object constructor
        """

        # Maps resources to tasks
        self.readers: dict[FdWrapper, Task] = {}
        self.writers: dict[FdWrapper, Task] = {}

    def pending(self) -> bool:
        return bool(self.readers or self.writers)

    def get_reader(self, rsc: FdWrapper):
        return self.readers.get(rsc)

    def get_writer(self, rsc: FdWrapper):
        return self.writers.get(rsc)

    def _collect_readers(self) -> list[int]:
        """
        Collects all resources that need to be read from,
        so we can select() on them later
        """

        result = []
        for resource in self.readers:
            result.append(resource.fileno())
        return result

    def _collect_writers(self) -> list[int]:
        """
        Collects all resources that need to be written to,
        so we can select() on them later
        """

        result = []
        for resource in self.writers:
            result.append(resource.fileno())
        return result

    def wait_io(self):
        kernel: BaseKernel = current_loop()
        deadline = kernel.get_closest_deadline()
        if deadline == float("inf"):
            deadline = 0
        readable, writable, _ = select.select(
            self._collect_readers(),
            self._collect_writers(),
            [],
            deadline,
        )
        for read_ready in readable:
            for resource, task in self.readers.items():
                if resource.fileno() == read_ready and task.state == TaskState.IO:
                    kernel.reschedule(task)
        for write_ready in writable:
            for resource, task in self.writers.items():
                if resource.fileno() == write_ready and task.state == TaskState.IO:
                    kernel.reschedule(task)

    def request_read(self, rsc: FdWrapper, task: Task):
        current_task().state = TaskState.IO
        self.readers[rsc] = task

    def request_write(self, rsc: FdWrapper, task: Task):
        current_task().state = TaskState.IO
        self.writers[rsc] = task

    def release(self, resource: FdWrapper):
        self.readers.pop(resource, None)
        self.writers.pop(resource, None)

    def release_task(self, task: Task):
        for resource, owner in self.readers.copy().items():
            if owner == task:
                self.readers.pop(resource)
        for resource, owner in self.writers.copy().items():
            if owner == task:
                self.writers.pop(resource)
