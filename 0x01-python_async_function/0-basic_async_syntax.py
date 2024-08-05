#!/usr/bin/env python3
"""using the random module"""
import asyncio
import random


async def wait_random(max_delay: int = 10) -> float:
    """
    Async Coroutine that wait for a delay randomly .
    """
    delay = random.uniform(0, max_delay)
    await asyncio.sleep(delay)
    return delay
