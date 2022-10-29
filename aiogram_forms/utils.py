from itertools import tee, islice, chain
from typing import Any, Iterable, Type, Tuple


def prev_next_iter(items: Iterable[Any]):
    prev_list, items_list, next_list = tee(items, 3)
    prev_list = chain([None], prev_list)
    next_list = chain(islice(next_list, 1, None), [None])
    return zip(prev_list, items_list, next_list)


def get_attrs_of_type(obj: Any, type_: Type) -> Tuple:
    return tuple(
        (key, value)
        for key, value
        in vars(obj).items()
        if isinstance(value, type_)
    )
