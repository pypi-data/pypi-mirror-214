from structio.abc import BaseDebugger


class SimpleDebugger(BaseDebugger):
    def on_start(self):
        print(">> Started")

    def on_exit(self):
        print(f"<< Stopped")
