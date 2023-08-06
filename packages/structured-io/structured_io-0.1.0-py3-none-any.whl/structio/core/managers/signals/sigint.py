from structio.abc import SignalManager
from types import FrameType
from structio.util.ki import currently_protected
from structio.core.run import current_loop
import warnings
import signal


class SigIntManager(SignalManager):
    """
    Handles Ctrl+C
    """

    def __init__(self):
        self.installed = False

    def handle(self, sig: int, frame: FrameType):
        loop = current_loop()
        if currently_protected():
            loop.signal_notify(sig, frame)
        else:
            raise KeyboardInterrupt()

    def install(self):
        if signal.getsignal(signal.SIGINT) != signal.default_int_handler:
            warnings.warn(
                f"structio has detected a custom SIGINT handler and won't touch it: keep in mind"
                f" this is likely to break KeyboardInterrupt delivery!"
            )
            return
        signal.signal(signal.SIGINT, self.handle)
        self.installed = True

    def uninstall(self):
        if self.installed:
            signal.signal(signal.SIGINT, signal.default_int_handler)
            self.installed = False
