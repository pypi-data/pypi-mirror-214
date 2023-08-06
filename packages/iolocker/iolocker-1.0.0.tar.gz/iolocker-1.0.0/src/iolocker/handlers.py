# -*- coding: UTF-8 -*-

from abc import ABC, abstractmethod
from typing import IO

from .constants import LOCK
from .core import lock, unlock
from .exceptions import LockFlagsError

__all__ = ["Handler", "FileLocker"]


class Handler(ABC):
    """Base abstract handler."""

    def __init__(self, *args, **kwargs):
        self._args, self._kwargs = args, kwargs

    def __enter__(self) -> IO:
        if not hasattr(self, "_handle"):
            self._handle: IO = self.acquire(*self._args, **self._kwargs)
        return self._handle

    def __exit__(self, exc_type, exc_val, exc_tb):
        if hasattr(self, "_handle"):
            self.release(self._handle)
            del self._handle

    def __delete__(self, instance):
        instance.release()

    @abstractmethod
    def acquire(self, *args, **kwargs):
        raise NotImplementedError(
            f"Method 'acquire()' was not implemented "
            f"in child class {self.__class__.__name__}!"
        )

    @abstractmethod
    def release(self, *args, **kwargs):
        raise NotImplementedError(
            f"Method 'release()' was not implemented "
            f"in child class {self.__class__.__name__}!"
        )


class FileLocker(Handler):
    """File locker."""

    _flags: dict = {
        "w": LOCK.EX,
        "a": LOCK.EX,
        "x": LOCK.EX,
        "r": LOCK.SH,
    }

    def acquire(self, handle: IO, flags: LOCK = None) -> IO:
        """
        Acquire a lock on the given `handle`.
        If `flags` are not provided it will try to guess
        them by reading the handle's operating mode.

        :param handle: The file handle.
        :param flags: The flags to be used to lock the handle.
        :return: The newly locked handle.
        """
        mode = self._get_mode(handle)

        if flags is None:
            flags = self._flags.get(mode)

        elif (mode == "w") and (flags in (LOCK.SH | LOCK.NB)):
            raise LockFlagsError(f"Wrong flags used on this operating mode of the handle (`{mode}`)!")

        lock(handle, flags)
        return handle

    def release(self, handle: IO):
        """Unlock the file handle."""
        unlock(handle)

    @staticmethod
    def _get_mode(handle: IO) -> str:
        """Return the handle's operating mode."""
        mode = handle.mode
        return mode.strip("tb+")
