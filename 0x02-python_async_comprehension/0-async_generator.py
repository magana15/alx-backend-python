#!/usr/bin/env python3
"""
Module showing async comprehension.
"""
import asyncio
import random
from typing import AsyncGenerator


async def async_generator() -> AsyncGenerator[float, None,]:
    """Looping 10 times, waiting 1 sec each time."""
    for _ in range(10):
        await asyncio.sleep(1)
        yield random.uniform(0, 10)
