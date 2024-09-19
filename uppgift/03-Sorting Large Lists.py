"""
Exercise 3: Sorting Large Lists
Task: Convert the following code to use both multi-threading and multiprocessing, 
then compare the timing of each version.
"""

import time
import random

def sort_task(data):
    return sorted(data)

if __name__ == "__main__":
    data = [random.randint(1, 100000) for _ in range(10**6)]
    
    start_time = time.time()
    sorted_data = sort_task(data)
    end_time = time.time()
    print(f"Sorting completed.")
    print(f"Normal Execution Time: {end_time - start_time} seconds")
