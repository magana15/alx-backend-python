#!/usr/bin/env python3
"""
Async coroutine that spawns wait_random n times with the specified max_delay.
"""
import asyncio
from typing import List
wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    """
    Async coroutine that is spawning wait_random
    n times with the specified max_delay.
    """
    tasks = [wait_random(max_delay) for _ in range(n)]
    delays = await asyncio.gather(*tasks)
    return sorted(delays)
