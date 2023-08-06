from typing import Hashable, Sequence, TypeVar

T = TypeVar("T", bound=Hashable)


def unique(sequence: Sequence[T]) -> T:
    """
    If the entire sequence contains only 1 unique element, return that element.
    If the sequence contains more or less than 1 unique element, raise a ValueError.
    """

    if len(set(sequence)) != 1:
        raise ValueError("Sequence doesn't contain unique elements.")

    return sequence[0]
