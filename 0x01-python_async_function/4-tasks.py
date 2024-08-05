#!/usr/bin/env python3
"""
module that uses asyncio to give tasks
"""
import asyncio
from typing import List

task_wait_random = __import__('3-tasks').task_wait_random


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    """
    Asynchronous coroutine that is spawning task_wait_random n times
    """
    tasks = [task_wait_random(max_delay) for _ in range(n)]
    delays = await asyncio.gather(*tasks)
    return sorted(delays)
