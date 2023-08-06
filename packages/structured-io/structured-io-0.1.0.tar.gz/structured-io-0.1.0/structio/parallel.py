# Module inspired by subprocess which allows for asynchronous
# multiprocessing
import os
import structio
import subprocess
from subprocess import (
    CalledProcessError,
    CompletedProcess,
    DEVNULL,
    PIPE
)
from structio.io import FileStream


class Popen:
    """
    Wrapper around subprocess.Popen, but async
    """

    def __init__(self, *args, **kwargs):
        if "universal_newlines" in kwargs:
            # Not sure why? But everyone else is doing it so :shrug:
            raise RuntimeError("universal_newlines is not supported")
        if stdin := kwargs.get("stdin"):
            if stdin not in {PIPE, DEVNULL}:
                # Curio mentions stuff breaking if the child process
                # is passed a stdin fd that is set to non-blocking mode
                os.set_blocking(stdin.fileno(), True)
        # Delegate to Popen's constructor
        self._process: subprocess.Popen = subprocess.Popen(*args, **kwargs)
        self.stdin = None
        self.stdout = None
        self.stderr = None
        if self._process.stdin:
            self.stdin = FileStream(self._process.stdin)
        if self._process.stdout:
            self.stdout = FileStream(self._process.stdout)
        if self._process.stderr:
            self.stderr = FileStream(self._process.stderr)

    async def wait(self):
        status = self._process.poll()
        if status is None:
            status = await structio.thread.run_in_worker(self._process.wait, cancellable=True)
        return status

    async def communicate(self, input=b"") -> tuple[bytes, bytes]:
        async with structio.create_pool() as pool:
            stdout = pool.spawn(self.stdout.readall) if self.stdout else None
            stderr = pool.spawn(self.stderr.readall) if self.stderr else None
            if input:
                await self.stdin.write(input)
                await self.stdin.close()
            # Awaiting a task object waits for its completion and
            # returns its return value!
            out = b""
            err = b""
            if stdout:
                out = await stdout
            if stderr:
                err = await stderr
            return out, err

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        if self.stdin:
            await self.stdin.close()
        if self.stdout:
            await self.stdout.close()
        if self.stderr:
            await self.stderr.close()
        await self.wait()

    def __getattr__(self, item):
        # Delegate to internal process object
        return getattr(self._process, item)


async def run(args, *, stdin=None, input=None, stdout=None, stderr=None, shell=False, check=False):
    """
    Async version of subprocess.run()
    """

    if input:
        stdin = subprocess.PIPE
    async with Popen(args, stdin=stdin, stdout=stdout, stderr=stderr, shell=shell) as process:
        try:
            stdout, stderr = await process.communicate(input)
        except:
            process.kill()
            raise

    status = process.poll()
    if check and status:
        raise CalledProcessError(status, process.args, output=stdout, stderr=stderr)
    return CompletedProcess(process.args, status, stdout, stderr)


async def check_output(args, *, stdin=None, stderr=None, shell=False, input=None):
    """
    Async version of subprocess.check_output
    """

    out = await run(args, stdout=PIPE, stdin=stdin, stderr=stderr, shell=shell,
                    check=True, input=input)
    return out.stdout
