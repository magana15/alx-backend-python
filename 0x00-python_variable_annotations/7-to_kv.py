#!/usr/bin/env python3
""" Complex types _ string and int float to a tuple """
from typing import List, Union, Tuple


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """function to_kv that takes
        strings, integers / floats as arguments.
        Args:
            k: string type.
            v: int or float type.
        Return:
            Tuple
    """
    return (k, pow(v, 2))
