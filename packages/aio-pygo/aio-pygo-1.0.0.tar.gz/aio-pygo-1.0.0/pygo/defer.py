from contextlib import contextmanager
from typing import Any, Callable, Generator


class Deferrer:
    def __init__(self) -> None:
        self.__deferred: list[Callable[[], Any]] = []

    def defer(self, callback: Callable[[], Any]):
        self.__deferred.append(callback)

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        for callback in reversed(self.__deferred):
            callback()


@contextmanager
def deferrer() -> Generator[Deferrer, Any, None]:
    defer = Deferrer()
    try:
        yield defer
    finally:
        defer()
