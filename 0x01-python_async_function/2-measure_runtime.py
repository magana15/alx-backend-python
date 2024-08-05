#!/usr/bin/env python3
"""
Module using asyncio to measure runtime
"""
import time
import asyncio


wait_n = __import__('1-concurrent_coroutines').wait_n


def measure_time(n: int, max_delay: int) -> float:
    """
    Measure the total execution time for wait.
    """
    start_time = time.time()
    asyncio.run(wait_n(n, max_delay))
    end_time = time.time()

    total_time = end_time - start_time
    average_time_per_call = total_time / n
    return average_time_per_call
