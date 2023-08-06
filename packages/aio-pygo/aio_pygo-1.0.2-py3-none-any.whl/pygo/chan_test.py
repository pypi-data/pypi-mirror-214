from pytest import raises

from pygo.chan import Chan, select
from pygo.defer import deferrer
from pygo.go import go


class TestClose:
    async def test_close(self):
        chan = Chan()

        assert not chan.closed

        chan.close()
        assert chan.closed


class TestSend:
    async def test_send(self):
        chan = Chan[str]()

        await chan.send("a")
        value, _ = await chan.receive()
        assert value == "a"

    async def test_closed(self):
        chan = Chan()
        chan.close()

        with raises(Chan.Closed):
            await chan.send(1)


class TestReceive:
    async def test_receive(self):
        chan = Chan[str]()

        await chan.send("a")

        value, open = await chan.receive()
        assert value == "a"
        assert open

        assert len(chan) == 0

    async def test_receive_multiples(self):
        chan = Chan[str]()

        await chan.send("a")
        await chan.send("b")

        assert await chan.receive() == ("a", True)
        assert await chan.receive() == ("b", True)
        assert len(chan) == 0

    async def test_closed(self):
        chan = Chan()
        chan.close()

        value, open = await chan.receive()
        assert value is None
        assert not open

    async def test_close_during_receive(self):
        chan = Chan()
        waiter = Chan()

        async def tester():
            with deferrer() as d:
                d.defer(waiter.close)

                value, open = await chan.receive()
                assert value is None
                assert not open

        go(tester())

        chan.close()

        await waiter.receive()


class TestLen:
    async def test_empty(self):
        chan = Chan[str]()

        assert len(chan) == 0

    async def test_multiple(self):
        chan = Chan[str]()
        await chan.send("a")
        await chan.send("a")

        assert len(chan) == 2

    async def test_receive_multiples(self):
        chan = Chan[str]()

        assert len(chan) == 0
        await chan.send("a")
        await chan.send("b")

        assert len(chan) == 2

        await chan.receive()
        await chan.receive()
        assert len(chan) == 0

    async def test_closed_values(self):
        chan = Chan()
        await chan.send("a")

        chan.close()
        assert len(chan) == 1

    async def test_closed_empty(self):
        chan = Chan()

        chan.close()

        assert len(chan) == 0


class TestEq:
    async def test_equal(self):
        chan = Chan()

        assert chan == chan

    async def test_not_equal(self):
        assert Chan() != Chan()

    async def test_other_type(self):
        assert Chan() != "a"


class TestAIter:
    async def test_aiter(self):
        chan = Chan[int]()
        actual = []

        await chan.send(0)
        await chan.send(1)
        chan.close()

        async for value in chan:
            actual.append(value)

        assert actual == [0, 1]


class TestSelect:
    async def test_first(self):
        chan1 = Chan[str]()
        chan2 = Chan[str]()

        await chan1.send("value")
        match await select(chan1, chan2):
            case [chan, value, True] if chan == chan1:
                assert value == "value"
            case _:
                assert False

    async def test_second(self):
        chan1 = Chan[str]()
        chan2 = Chan[str]()

        await chan2.send("value")
        match await select(chan1, chan2):
            case [chan, value, True] if chan == chan2:
                assert value == "value"
            case _:
                assert False

    async def test_close(self):
        chan1 = Chan[str]()
        chan2 = Chan[str]()

        chan1.close()
        match await select(chan1, chan2):
            case [chan, value, False] if chan == chan1:
                assert value is None
            case _:
                assert False
