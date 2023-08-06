from asyncio import Task, get_event_loop
from typing import Any, Callable, Coroutine


def go(fn: Coroutine[Any, Any, None] | Callable[[], Any]) -> Task[None]:
    if isinstance(fn, Coroutine):
        return __async_go(fn)

    return __sync_go(fn)


def __async_go(coroutine: Coroutine[Any, Any, None]) -> Task[None]:
    loop = get_event_loop()
    task = loop.create_task(coroutine)

    return task


def __sync_go(fn: Callable[[], Any]) -> Task[None]:
    async def wrapper():
        return fn()

    return __async_go(wrapper())
