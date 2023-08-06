# Async wrapper for pathlib.Path (blocking calls are run in threads)
import os
from functools import partial, wraps
import structio
import pathlib
from structio.core.syscalls import checkpoint


_SYNC = {
    "as_posix",
    "as_uri",
    "is_absolute",
    "is_reserved",
    "joinpath",
    "match",
    "relative_to",
    "with_name",
    "with_suffix",
}

_ASYNC = {
    "chmod",
    "exists",
    "expanduser",
    "glob",
    "group",
    "is_block_device",
    "is_char_device",
    "is_dir",
    "is_fifo",
    "is_file",
    "is_mount",
    "is_socket",
    "is_symlink",
    "lchmod",
    "lstat",
    "mkdir",
    "owner",
    "read_bytes",
    "read_text",
    "rename",
    "replace",
    "resolve",
    "rglob",
    "rmdir",
    "samefile",
    "stat",
    "symlink_to",
    "touch",
    "unlink",
    "rmdir",
    "write_text",
    "write_bytes",
}


def _wrap(v):
    if isinstance(v, pathlib.Path):
        return Path(v)
    return v


class Path:
    """
    A wrapper to pathlib.Path which executes
    blocking calls using structio.thread.run_in_worker
    """

    def __init__(self, *args):
        self._sync_path: pathlib.Path = pathlib.Path(*args)

    @classmethod
    @wraps(pathlib.Path.cwd)
    async def cwd(*args, **kwargs):
        """
        Like pathlib.Path.cwd(), but async
        """

        # This method is special and can't be just forwarded like the others because
        # it is a class method and I don't feel like doing all the wild metaprogramming
        # stuff that Trio did (which is cool but gooood luck debugging that), so here ya go.
        return _wrap(
            await structio.thread.run_in_worker(pathlib.Path.cwd, *args, **kwargs)
        )

    @classmethod
    @wraps(pathlib.Path.home)
    async def home(*args, **kwargs):
        """
        Like pathlib.Path.home(), but async
        """

        return _wrap(
            await structio.thread.run_in_worker(pathlib.Path.home, *args, **kwargs)
        )

    @wraps(pathlib.Path.open)
    async def open(self, *args, **kwargs):
        """
        Like pathlib.Path.open(), but async
        """

        f = await structio.thread.run_in_worker(self._sync_path.open, *args, **kwargs)
        return structio.wrap_file(f)

    def __repr__(self):
        return f"structio.Path({repr(str(self._sync_path))})"

    def __dir__(self):
        return super().__dir__()

    async def iterdir(self):
        """
        Like pathlib.Path.iterdir(), but async
        """

        # Inspired by https://github.com/python-trio/trio/issues/501#issuecomment-381724137
        func = partial(os.listdir, self._sync_path)
        files = await structio.thread.run_in_worker(func)

        async def agen():
            if not files:
                await checkpoint()
            for name in files:
                yield self._sync_path._make_child_relpath(name)
                await checkpoint()

        return agen()

    def __fspath__(self):
        return os.fspath(self._wrapped)

    def __truediv__(self, other):
        return _wrap(self._sync_path.__truediv__(other))

    def __rtruediv__(self, other):
        return _wrap(self._sync_path.__rtruediv__(other))

    def __getattr__(self, attr: str):
        # We use a similar trick to the one we stole from
        # Trio for async files, except we also wrap sync
        # methods because we want them to return our own
        # Path objects, not pathlib.Path!

        if attr in _SYNC:
            # We duplicate the code here because we only
            # want to forward the stuff in _SYNC and _ASYNC,
            # not everything (like our cwd() classmethod above)
            m = getattr(self._sync_path, attr)

            @wraps(m)
            def wrapper(*args, **kwargs):
                return _wrap(m(*args, **kwargs))

            setattr(self, attr, wrapper)
            return wrapper
        if attr in _ASYNC:
            m = getattr(self._sync_path, attr)

            @wraps(m)
            async def wrapper(*args, **kwargs):
                f = partial(m, *args, **kwargs)
                return _wrap(await structio.thread.run_in_worker(f))

            setattr(self, attr, wrapper)
            return wrapper
        # Falls down to __getattribute__, which may find a cached
        # method we generated earlier!
        raise AttributeError(attr)
