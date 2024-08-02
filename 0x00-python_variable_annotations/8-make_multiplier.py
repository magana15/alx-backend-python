#!/usr/bin/env python3
""" Complex types _ functions """
from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """ Type-annotated function make_multiplier taking a float
        argument.
        Args:
            multiplier: float type.
        Return:
            A function that multiply a float by multiplier
    """
    return lambda multiplier2: multiplier2 * multiplier
