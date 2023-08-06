from pulipy.function import curry


def test_currying1():
    @curry
    def add(a: int, b: int) -> int:
        return a + b

    assert add(1)(2) == 3


def test_currying2():
    @curry
    def concat(a: str, b: str) -> str:
        return a + b

    assert concat("Hello, ")("World!") == "Hello, World!"
