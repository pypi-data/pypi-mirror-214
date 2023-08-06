from structio.exceptions import ResourceBusy


# Yes, I stole trio's idea of the ConflictDetector class. Shut up
class ThereCanBeOnlyOne:
    """
    A simple context manager that raises an error when
    an attempt is made to acquire it from more than one
    task at a time. Can be used to protect sections of
    code handling some async resource that would need locking
    if they were allowed to be called from more than one task
    at a time, but that should never happen (for example, if you
    try to do call await send() on a socket from two different
    tasks at the same time)
    """

    def __init__(self, msg: str):
        self._acquired = False
        self.msg = msg

    def __enter__(self):
        if self._acquired:
            raise ResourceBusy(self.msg)
        self._acquired = True

    def __exit__(self, *args):
        self._acquired = False
