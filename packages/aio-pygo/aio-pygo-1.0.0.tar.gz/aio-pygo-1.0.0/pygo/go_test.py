from pygo.chan import Chan, select
from pygo.go import go


class TestGo:
    async def test_sync(self):
        c = Chan()

        go(c.close)

        match await select(c):
            case [chan, _, False] if chan == c:
                ...
            case _:
                assert False

    async def test_async(self):
        c = Chan()

        async def my_fn():
            await c.send("a")

        go(my_fn())

        match await select(c):
            case [chan, value, _] if chan == c:
                assert value == "a"
            case _:
                assert False
