from pytest import raises

from pygo.defer import deferrer


class TestDefer:
    async def test_defer(self):
        actual = []
        with deferrer() as d:
            d.defer(lambda: actual.append(0))

            actual.append(1)

        assert actual == [1, 0]

    async def test_defer_exception(self):
        actual = []

        with raises(ValueError):
            with deferrer() as d:
                d.defer(lambda: actual.append(0))

                actual.append(1)

                raise ValueError()

        assert actual == [1, 0]
