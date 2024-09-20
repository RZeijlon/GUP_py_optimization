import numpy as np
import time
from threading import Thread
from multiprocessing import Process, Queue

def matrix_multiply(a, b):
    """Performs matrix multiplication using NumPy's dot function."""
    return np.dot(a, b)

def matrix_multiply_thread(a_slice, b, result_list, index):
    """
    Worker function for threading.
    Multiplies a slice of matrix 'a' with 'b' and stores the result in 'result_list' at position 'index'.
    """
    result_list[index] = np.dot(a_slice, b)

def matrix_multiply_process(a_slice, b, queue):
    """
    Worker function for multiprocessing.
    Multiplies a slice of matrix 'a' with 'b' and puts the result into a queue.
    """
    result = np.dot(a_slice, b)
    queue.put(result)

def execute_normal(a, b):
    """Performs normal matrix multiplication and measures execution time."""
    start_time = time.time()
    result = matrix_multiply(a, b)
    end_time = time.time()
    print(f"Normal Execution Time: {end_time - start_time:.4f} seconds")
    return result

def execute_multithreading(a, b, num_threads=4):
    """Performs matrix multiplication using multithreading and measures execution time."""
    threads = []
    results_thread = [None] * num_threads
    a_splits = np.array_split(a, num_threads)

    start_time = time.time()
    for i in range(num_threads):
        # Create and start a new thread for each split of 'a'
        thread = Thread(target=matrix_multiply_thread, args=(a_splits[i], b, results_thread, i))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    # Combine results from all threads
    result = np.vstack(results_thread)
    end_time = time.time()
    print(f"Multithreading Execution Time: {end_time - start_time:.4f} seconds")
    return result

def execute_multiprocessing(a, b, num_processes=4):
    """Performs matrix multiplication using multiprocessing and measures execution time."""
    processes = []
    a_splits = np.array_split(a, num_processes)
    queue = Queue()

    start_time = time.time()
    for i in range(num_processes):
        # Create and start a new process for each split of 'a'
        process = Process(target=matrix_multiply_process, args=(a_splits[i], b, queue))
        processes.append(process)
        process.start()

    # Collect results from the queue
    results_process = []
    for _ in processes:
        results_process.append(queue.get())

    # Wait for all processes to finish
    for process in processes:
        process.join()

    # Combine results from all processes
    result = np.vstack(results_process)
    end_time = time.time()
    print(f"Multiprocessing Execution Time: {end_time - start_time:.4f} seconds")
    return result

if __name__ == "__main__":
    # Generate two random 1000x1000 matrices 'a' and 'b'
    a = np.random.rand(1000, 1000)
    b = np.random.rand(1000, 1000)

    # Perform and time normal matrix multiplication
    result_normal = execute_normal(a, b)

    # Perform and time multithreaded matrix multiplication
    result_threaded = execute_multithreading(a, b)

    # Perform and time multiprocessing matrix multiplication
    result_multiprocessing = execute_multiprocessing(a, b)

    # Verify that all methods produce the same result
    if np.allclose(result_normal, result_threaded) and np.allclose(result_normal, result_multiprocessing):
        print("All methods produce the same result.")
    else:
        print("There is a difference in results between methods. ")
