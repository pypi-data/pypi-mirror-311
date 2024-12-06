from typing import Sequence, TypeVar

T = TypeVar("T")


def append(value: T, arr: Sequence[T]) -> Sequence[T]:
    """
    Returns a new list containing the contents of the given list, followed by the given element.
    """

    if isinstance(arr, str):
        return arr + value

    return list(arr) + [value]
