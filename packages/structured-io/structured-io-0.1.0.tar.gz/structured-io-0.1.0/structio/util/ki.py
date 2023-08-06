"""
aiosched: Yet another Python async scheduler

Copyright (C) 2022 nocturn9x

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   https:www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import sys
import inspect
from functools import wraps
from types import FrameType


# Special magic module half-stolen from Trio (thanks njsmith I love you)
# that makes Ctrl+C work. P.S.: Please Python, get your signals straight.


# Just a funny variable name that is not a valid
# identifier (but still a string so tools that hack
# into frames don't freak out when they look at the
# local variables) which will get injected silently
# into every frame to enable/disable the safeguards
# for Ctrl+C/KeyboardInterrupt
CTRLC_PROTECTION_ENABLED = "|yes-it-is|"


def critical_section(frame: FrameType) -> bool:
    """
    Returns whether Ctrl+C protection is currently
    enabled in the given frame or in any of its children.
    Stolen from Trio
    """

    while frame is not None:
        if CTRLC_PROTECTION_ENABLED in frame.f_locals:
            return frame.f_locals[CTRLC_PROTECTION_ENABLED]
        if frame.f_code.co_name == "__del__":
            return True
        frame = frame.f_back
    return True


def currently_protected() -> bool:
    """
    Returns whether Ctrl+C protection is currently
    enabled in the current context
    """

    return critical_section(sys._getframe())


def legacy_isasyncgenfunction(obj):
    return getattr(obj, "_async_gen_function", None) == id(obj)


def _ki_protection_decorator(enabled):
    def decorator(fn):
        # In some version of Python, isgeneratorfunction returns true for
        # coroutine functions, so we have to check for coroutine functions
        # first.
        if inspect.iscoroutinefunction(fn):

            @wraps(fn)
            def wrapper(*args, **kwargs):
                # See the comment for regular generators below
                coro = fn(*args, **kwargs)
                coro.cr_frame.f_locals[CTRLC_PROTECTION_ENABLED] = enabled
                return coro

            return wrapper
        elif inspect.isgeneratorfunction(fn):

            @wraps(fn)
            def wrapper(*args, **kwargs):
                # It's important that we inject this directly into the
                # generator's locals, as opposed to setting it here and then
                # doing 'yield from'. The reason is, if a generator is
                # throw()n into, then it may magically pop to the top of the
                # stack. And @contextmanager generators in particular are a
                # case where we often want KI protection, and which are often
                # thrown into! See:
                #     https://bugs.python.org/issue29590
                gen = fn(*args, **kwargs)
                gen.gi_frame.f_locals[CTRLC_PROTECTION_ENABLED] = enabled
                return gen

            return wrapper
        elif inspect.isasyncgenfunction(fn) or legacy_isasyncgenfunction(fn):

            @wraps(fn)
            def wrapper(*args, **kwargs):
                # See the comment for regular generators above
                agen = fn(*args, **kwargs)
                agen.ag_frame.f_locals[CTRLC_PROTECTION_ENABLED] = enabled
                return agen

            return wrapper
        else:

            @wraps(fn)
            def wrapper(*args, **kwargs):
                locals()[CTRLC_PROTECTION_ENABLED] = enabled
                return fn(*args, **kwargs)

            return wrapper

    return decorator


enable_ki_protection = _ki_protection_decorator(True)
enable_ki_protection.__name__ = "enable_ki_protection"
enable_ki_protection.__doc__ = "Decorator to enable keyboard interrupt protection"

disable_ki_protection = _ki_protection_decorator(False)
disable_ki_protection.__name__ = "disable_ki_protection"
disable_ki_protection.__doc__ = "Decorator to disable keyboard interrupt protection"
