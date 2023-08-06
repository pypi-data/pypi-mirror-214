from asyncio import sleep
from asyncio.queues import Queue, QueueEmpty
from typing import Any, Generic, TypeVar
from uuid import uuid4

ChanType = TypeVar("ChanType")


class Chan(Generic[ChanType]):
    class Empty(Exception):
        ...

    class Closed(Exception):
        ...

    def __init__(self, max_size: int = 0) -> None:
        self.__queue = Queue[ChanType](max_size)
        self.__closed = False
        self.__id = str(uuid4())

    def close(self):
        self.__closed = True

    @property
    def closed(self) -> bool:
        return self.__closed

    def try_next(self) -> ChanType:
        try:
            return self.__queue.get_nowait()
        except QueueEmpty:
            raise self.Empty()

    async def send(self, e: ChanType):
        if self.closed:
            raise self.Closed()

        await self.__queue.put(e)

    async def receive(self) -> tuple[ChanType | None, bool]:
        _, value, open = await select(self)

        return value, open

    async def __anext__(self) -> ChanType:
        _, value, open = await select(self)

        if not open:
            raise StopAsyncIteration()

        return value  # type: ignore

    def __aiter__(self):
        return self

    def __len__(self) -> int:
        return self.__queue.qsize()

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, self.__class__):
            return False

        return self.__id == value.__id


async def select(
    *chans: Chan[Any],
) -> tuple[Chan[Any], Any, bool]:
    while True:
        for chan in chans:
            try:
                value = chan.try_next()
                return (chan, value, True)
            except Chan.Empty:
                ...

            if chan.closed and len(chan) == 0:
                return (chan, None, False)

        # force scheduling
        await sleep(0)
