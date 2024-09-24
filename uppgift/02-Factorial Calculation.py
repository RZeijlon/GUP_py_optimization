"""
Exercise 2: Factorial Calculation
Task: Convert the following code to use both 
multi-threading and multiprocessing, 
then compare the timing of each version.

"""

import time
import threading
import multiprocessing
from math import prod

# Recursive factorial function (inefficient for large n)
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)
    
# Iterative factorial calculation for a range (used for threading and multiprocessing)
def factorial_range(start, end):
    # Calculate the product of numbers in the range [start, end]
    return prod(range(start, end + 1))

# Thread worker function to compute the factorial of a given range
# Stores the result in a shared results list
def thread_worker(start, end, results, index):
    results[index] = factorial_range(start, end)

# Process worker function to compute the factorial of a given range
# Puts the result in a shared multiprocessing queue
def process_worker(start, end, queue):
    result = factorial_range(start, end)
    queue.put(result) # Put the result in the queue for the main process to retrieve

if __name__ == "__main__":
    n = 5000  # Large number for factorial
    num_threads = 4  # Split into 4 threads/processes
    chunk_size = n // num_threads  # Divide the factorial calculation into chunks
    
    ### Multi-threading version ###
    # Create a list to store the results from each thread
    thread_results = [1] * num_threads
    threads = []

    # Start timing the multi-threading execution
    start_time = time.time()

    # Split the task into chunks and create threads
    for i in range(num_threads):
        start = i * chunk_size + 1 # Start of the range for this thread
        end = (i + 1) * chunk_size if i != num_threads - 1 else n # End of the range for this thread
        # Create a thread and assign it the task of calculating the factorial for its range
        t = threading.Thread(target=thread_worker, args=(start, end, thread_results, i))
        threads.append(t)
        t.start() # Start the thread

    # Wait for all threads to finish
    for t in threads:
        t.join()

    # Multiply all partial results to get the final factorial
    final_thread_result = prod(thread_results)
    # End timing the multi-threading execution
    end_time = time.time()
    print(f"Factorial calculated with Multi-threading.")
    print(f"Multi-threading Execution Time: {end_time - start_time} seconds")

    ### Multi-processing version ###
    # Create a queue to collect results from processes
    processes = []
    queue = multiprocessing.Queue()

    # Start timing the multi-processing execution
    start_time = time.time()

    # Split the task into chunks and create processes
    for i in range(num_threads):
        start = i * chunk_size + 1 # Start of the range for this process
        end = (i + 1) * chunk_size if i != num_threads - 1 else n # End of the range for this process
        # Create a process and assign it the task of calculating the factorial for its range
        p = multiprocessing.Process(target=process_worker, args=(start, end, queue))
        processes.append(p)
        p.start() # Start the process

    # Wait for all processes to finish
    for p in processes:
        p.join()

    # Collect results from the queue and multiply them
    final_process_result = prod([queue.get() for _ in range(num_threads)])
    # End timing the multi-processing execution
    end_time = time.time()
    print(f"Factorial calculated with Multi-processing.")
    print(f"Multi-processing Execution Time: {end_time - start_time} seconds")
