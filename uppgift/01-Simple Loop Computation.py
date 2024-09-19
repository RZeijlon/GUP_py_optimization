"""
Exercise 1: Simple Loop Computation
Task: Convert the following code to use both multi-threading 
and multiprocessing,
then compare the timing of each version.
"""

import time

def simple_task(n):
    total = 0
    for i in range(n):
        total += i
    return total

if __name__ == "__main__":
    start_time = time.time()
    result = simple_task(10**7)
    end_time = time.time()
    print(f"Result: {result}")
    print(f"Normal Execution Time: {end_time - start_time} seconds")


# sijbfgoiusbg