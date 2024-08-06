#!/usr/bin/env python3
"""
Module for async comprehension
"""


from typing import List
async_generator = __import__('0-async_generator').async_generator


async def async_comprehension() -> List[float]:
    """Return 10 random numbers"""
    result = [i async for i in async_generator()]
    return result
