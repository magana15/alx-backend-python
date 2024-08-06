#!/usr/bin/env python3
"""
Module for the async comprehension.
"""
import asyncio
import random
from typing import Generator


async def async_generator() -> Generator[float, None, None]:
    """Looping 10 times, then waiting 1 sec each time"""
    for i in range(10):
        await asyncio.sleep(1)
        yield random.random() * 10
