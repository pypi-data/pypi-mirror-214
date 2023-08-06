from typing import Any, Callable, TypeVar

T = TypeVar("T")


def curry(f: Callable[..., Any]) -> Callable[..., Any]:
    def curried(*args: Any) -> Any:
        if len(args) >= f.__code__.co_argcount:
            return f(*args)

        def g(*args2: Any) -> Any:
            return curried(*(args + args2))

        return g

    return curried
