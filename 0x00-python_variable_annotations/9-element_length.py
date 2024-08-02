#!/usr/bin/env python3
""" An iterable object """
from typing import Iterable, Sequence, List, Tuple


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """ Type-annotated function element_length that take iterable
        argument
        Args:
            lstr: iterable object
        Return:
            element length
    """
    return [(i, len(i)) for i in lst]
