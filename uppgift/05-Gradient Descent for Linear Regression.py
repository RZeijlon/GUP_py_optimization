"""
Exercise 5: Gradient Descent for Linear Regression
Task: Convert the following linear 
regression code to use both multi-threading and multiprocessing, 
then compare the timing of each version.
"""


import os
import numpy as np
import time
from threading import Thread
from queue import Queue as ThreadQueue
from multiprocessing import Process, Queue

def gradient_descent(X, y, learning_rate=0.01, iterations=1000):
    m, n = X.shape
    theta = np.zeros(n)
    for _ in range(iterations):
        gradient = X.T @ (X @ theta - y) / m
        theta -= learning_rate * gradient
    return theta

def gradient_descent_with_queue(X, y, learning_rate=0.01, iterations=1000, result_queue=None):
    theta = gradient_descent(X, y, learning_rate, iterations) 
    if result_queue is not None:
        result_queue.put(theta)

def execute_normal(X, y):
    start_time = time.time()
    theta = gradient_descent(X, y, 0.01, 1000)
    end_time = time.time()
    print(f"Normal Execution Time: {end_time - start_time:.4f} seconds")
    return theta

def execute_multithreading(X, y, num_threads=int(os.cpu_count()/2)):
    threads = []
    X_splits = np.array_split(X, num_threads)
    y_splits = np.array_split(y, num_threads)
    result_queue = ThreadQueue()
    theta = None

    start_time = time.time()
    for i in range(num_threads):
        # Create and start a new thread for each split of 'X' and 'y'
        thread = Thread(target=gradient_descent_with_queue, args=(X_splits[i], y_splits[i], 0.01, 1000, result_queue))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to finish
    for thread in threads:
        thread.join()
    
    # Collect results from the queue
    results_process = []
    
    for _ in threads:
        results_process.append(result_queue.get())    

    theta = np.vstack(results_process)
    theta = np.mean(theta, axis=0)

    end_time = time.time()
    print(f"Multithreading Execution Time: {end_time - start_time:.4f} seconds")
    
    if theta is None:
        print("Error: No results from threads.")
        return None  # Or some other appropriate error handling
    
    return theta

def execute_multiprocessing(X, y, num_processes=6):
    processes = []
    X_splits = np.array_split(X, num_processes)
    y_splits = np.array_split(y, num_processes)
    result_queue = Queue()
    theta = None

    start_time = time.time()
    for i in range(num_processes):
        # Create and start a new process for each split of 'X' and 'y'
        process = Process(target=(gradient_descent_with_queue), args=(X_splits[i], y_splits[i], 0.01, 1000, result_queue))
        processes.append(process)
        process.start()

    # Wait for all processes to finish
    for i, process in enumerate(processes):
        process.join()

    # Collect results from the queue
    results_process = []
    for i, _ in enumerate(processes):        
        results_process.append(result_queue.get())

    # Combine results from all processes
    theta = np.vstack(results_process)
    theta = np.mean(theta, axis=0)

    end_time = time.time()
    print(f"Multiprocessing Execution Time: {end_time - start_time:.4f} seconds")
    
    if theta is None:
        print("Error: No results from processes.")
        return None  # Or some other appropriate error handling
    
    return theta


if __name__ == "__main__":
    X = np.random.rand(100000, 3)
    y = np.random.rand(100000)

    result_normal = execute_normal(X, y)
    result_multithreading = execute_multithreading(X, y)
    result_multiprocessing = execute_multiprocessing(X, y)

    print(result_normal)
    print(result_multithreading)
    print(result_multiprocessing)

    if np.allclose(result_normal, result_multithreading, rtol=1e-4):
        print("multithreading method produce the same result as normal.")
    else:
        print("There is a difference in results for multithreading.")
    
    if np.allclose(result_normal, result_multiprocessing, rtol=1e-4):
        print("multiprocessing method produce the same result as normal.")
    else:
        print("There is a difference in results for multiprocessing. ")
    
    
    if np.allclose(result_multithreading, result_multiprocessing, rtol=1e-4):
        print("multithreading and multiprocessing methods produce the same result.")
    else:
        print("There is a difference in results for multithreading and multiprocessing.")