#!/usr/bin/env python3
""" Complex types - list of floats """
from typing import List


def sum_list(input_list: List[float]) -> float:
    """ Type-annotated func sum_list  taking a float argument.
        Args:
            input_list: float.
        Return:
            The sum as  float.
    """
    return sum(input_list)
