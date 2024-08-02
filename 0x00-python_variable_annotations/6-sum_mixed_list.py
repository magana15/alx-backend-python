#!/usr/bin/env python3
""" Complex types """
from typing import List, Union


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    """ Type-annotated function that takes a list of
        float and integer arguments.
        Args:
            mxd_lst: float and int.
        Return:
            The sum as float.
    """
    return sum(mxd_lst)
