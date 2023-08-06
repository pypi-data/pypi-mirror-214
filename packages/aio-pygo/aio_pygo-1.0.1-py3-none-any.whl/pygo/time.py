import asyncio
from datetime import timedelta

from pygo.chan import Chan
from pygo.go import go


async def after(delay: timedelta) -> Chan[None]:
    timeout = Chan[None]()

    async def sleeper():
        await sleep(delay)
        timeout.close()

    go(sleeper())

    return timeout


async def sleep(delay: timedelta):
    await asyncio.sleep(delay.total_seconds())
