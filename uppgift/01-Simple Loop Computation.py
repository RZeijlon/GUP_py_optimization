"""
Exercise 1: Simple Loop Computation
Task: Convert the following code to use both multi-threading 
and multiprocessing,
then compare the timing of each version.
"""

import time
import threading
import multiprocessing

def simple_task(n):
    total = 0
    for i in range(n):
        total += i
    return total

# Wrapper function for threading
def thread_worker(n, results, index):
    results[index] = simple_task(n)

# Wrapper function for multiprocessing
def process_worker(n, queue):
    result = simple_task(n)
    queue.put(result)

if __name__ == "__main__":
    N = 10**7
    num_threads = 4
    split = N // num_threads

    # Multi-threading
    threads = []
    thread_results = [0] * num_threads
    start_time = time.time()
    
    for i in range(num_threads):
        t = threading.Thread(target=thread_worker, args=(split, thread_results, i))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    total_thread_result = sum(thread_results)
    end_time = time.time()
    print(f"Result (Multi-threading): {total_thread_result}")
    print(f"Multi-threading Execution Time: {end_time - start_time} seconds")

    # Multi-processing
    processes = []
    queue = multiprocessing.Queue()
    start_time = time.time()
    
    for i in range(num_threads):
        p = multiprocessing.Process(target=process_worker, args=(split, queue))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    total_process_result = sum([queue.get() for _ in range(num_threads)])
    end_time = time.time()
    print(f"Result (Multi-processing): {total_process_result}")
    print(f"Multi-processing Execution Time: {end_time - start_time} seconds")