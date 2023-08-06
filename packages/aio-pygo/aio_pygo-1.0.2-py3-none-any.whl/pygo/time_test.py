from datetime import datetime, timedelta

from pygo.chan import select
from pygo.time import after


class TestTime:
    async def test_after(self):
        start_time = datetime.now()

        timeout = await after(timedelta(seconds=1))
        await select(timeout)

        assert datetime.now() - start_time >= timedelta(seconds=1)
