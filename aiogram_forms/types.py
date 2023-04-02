"""
General types.
"""
from typing import Union
from aiogram.utils.i18n.lazy_proxy import LazyProxy  # type: ignore[attr-defined]

TranslatableString = Union[str, LazyProxy]
