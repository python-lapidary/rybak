from typing import Iterable


class LoopContext(Exception):
    def __init__(self, items: Iterable) -> None:
        self.items = items


def loop_over(items: Iterable) -> None:
    if not isinstance(items, Iterable):
        raise TypeError('items must be an Iterable')
    raise LoopContext(items)
