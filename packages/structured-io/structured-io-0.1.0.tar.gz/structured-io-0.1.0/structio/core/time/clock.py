import random
from timeit import default_timer
from structio.abc import BaseClock


class DefaultClock(BaseClock):
    def __init__(self):
        super().__init__()
        # We add a large random offset to our timer value
        # so users notice the problem if they try to compare
        # them across different runs
        self.offset: int = random.randint(100_000, 1_000_000)

    def start(self):
        pass

    def setup(self):
        pass

    def teardown(self):
        pass

    def current_time(self) -> float:
        return default_timer() + self.offset

    def deadline(self, deadline):
        return self.current_time() + deadline
