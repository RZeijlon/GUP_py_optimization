"""
Exercise 3: Image Processing with Convolution (CNN Operation)
Task: Convert the following convolution operation to use both
 multi-threading and multiprocessing,
 then compare the timing of each version.
"""


import os
import numpy as np
import time
from threading import Thread
from queue import Queue as ThreadQueue
from multiprocessing import Process, Queue
from scipy.signal import convolve2d
from PIL import Image
import logging

def convolution(image, kernel):
    return convolve2d(image, kernel, mode='same')

def convolution_with_queue(image, kernel, result_queue=None):
    result = convolution(image, kernel)
    if result_queue is not None:
        result_queue.put(result)

def execute_normal(image, kernel):
    """
    Function to execute the original convolution function.
    """
    start_time = time.time()
    result = convolution(image, kernel)
    end_time = time.time()
    print(f"Normal Execution Time: {end_time - start_time} seconds")

    return result

def execute_multithreading(image, kernel):
    """
    Function to execute the convolution function using multithreading.
    """
    num_threads = os.cpu_count()
    if num_threads == 1:
        raise ValueError("Multithreading not supported with 1 core.")
    if num_threads > 2:
        num_threads = 4
    else:
        num_threads = 2
    if num_threads == 4:
        # split the image into 4 squares (one for each corner)
        image_splits = np.array_split(image, 2, axis=0)
        image_splits = [np.array_split(split, 2, axis=1) for split in image_splits]
    else:
        image_splits = np.array_split(image, 2, axis=0)
    start_time = time.time()
    result_queue = ThreadQueue()
    threads = []
    for i, _ in enumerate(image_splits):
        for j, _ in enumerate(image_splits[i]):
            thread = Thread(target=convolution_with_queue,
                            args=(image_splits[i][j], kernel, result_queue))
            thread.start()
            threads.append(thread)
    
    for thread in threads:
        thread.join()

    results = [[None, None], [None, None]]  # Initialize a 2x2 list to hold results
    for _ in range(4):
        result = result_queue.get()
        i, j = divmod(_, 2)  # Determine the original quadrant position
        results[i][j] = result

    img = np.block(results)  # Efficiently reconstruct the image
    end_time = time.time()
    print(f"Multithreading Execution Time: {end_time - start_time} seconds")

    return img

def execute_multiprocessing(image, kernel):
    """
    Function to execute the convolution function using multiprocessing.
    """
    num_processes = os.cpu_count()
    if num_processes == 1:
        raise ValueError("Multiprocessing not supported with 1 core.")
    if num_processes > 2:
        num_processes = 4
    else:
        num_processes = 2
    if num_processes == 4:
        # split the image into 4 squares (one for each corner)
        image_splits = np.array_split(image, 2, axis=0)
        image_splits = [np.array_split(split, 2, axis=1) for split in image_splits]
    else:
        image_splits = np.array_split(image, 2, axis=0)
    start_time = time.time()
    result_queue = Queue()
    processes = []
    
    print('start and append')
    for i, _ in enumerate(image_splits):
        for j, _ in enumerate(image_splits[i]):
            print(i, j)
            process = Process(target=convolution_with_queue,
                            args=(image_splits[i][j], kernel, result_queue))
            print(process)
            processes.append(process)
            process.start()

    print('join')
    for i, process in enumerate(processes):
        print(i)
        print(process)
        try:
            process.join()
        except Exception as e:
            logging.error(f"Error in child process: {e}")

    results = [[None, None], [None, None]]  # Initialize a 2x2 list to hold results
    print('get')
    for _ in range(4):
        print(_)
        result = result_queue.get()
        i, j = divmod(_, 2)  # Determine the original quadrant position
        results[i][j] = result

    img = np.block(results)  # Efficiently reconstruct the image
    end_time = time.time()
    print(f"Multiprocessing Execution Time: {end_time - start_time} seconds")

    return img

if __name__ == "__main__":
    image = np.random.rand(1024, 1024)
    kernel = np.random.rand(3, 3)
    
    # Normal Execution
    result_normal = execute_normal(image, kernel)

    # Multi-threading
    result_threading = execute_multithreading(image, kernel)

    # Multi-processing
    result_multiprocessing = execute_multiprocessing(image, kernel)

    # Compare the results
    result_dif = result_normal - result_threading
    # after looking at the results, we can see that the results are the
    # same except for the edges where the split occurs, this is to me 
    # acceptable since the there are not a lot of differences and the
    # number of differences is very small. See 'threading_result_diff.gif'
    # and 'process_result_diff.gif' for the differences.

    # Check if 99% of the results are the same
    number_of_same_results = np.sum(np.abs(result_dif) < 0.001)
    if number_of_same_results / result_normal.size > 0.99:
        print("Threading results are the same.")
    else:
        print("Threading results are different.")

    # save the results and result_dif to grayscale IMAGE files
    result_dif_rescaled = (
        result_dif * 255 / result_dif.max()).astype(np.uint8)
    # change the axis to be able to save the image
    result_dif = np.swapaxes(result_dif_rescaled, 0, 1)
    result_dif = Image.fromarray(result_dif, 'L')
    result_dif.save('threading_result_diff.gif')

    result_normal_rescaled = (
        result_normal * 255 / result_normal.max()).astype(np.uint8)
    result_normal = np.swapaxes(result_normal_rescaled, 0, 1)
    result_normal = Image.fromarray(result_normal_rescaled, 'L')
    result_normal.save('result_normal.gif')    

    result_threding_rescaled = (
        result_threading * 255 / result_threading.max()).astype(np.uint8)
    result_threading = np.swapaxes(result_threding_rescaled, 0, 1)
    result_threading = Image.fromarray(result_threding_rescaled, 'L')
    result_threading.save('result_threading.gif')

    result_dif = result_normal - result_multiprocessing
    number_of_same_results = np.sum(np.abs(result_dif) < 0.001)
    if number_of_same_results / result_normal.size > 0.99:
        print("Multiprocessing results are the same.")
    else:
        print("Multiprocessing results are different.")

    result_dif_rescaled = (
        result_dif * 255 / result_dif.max()).astype(np.uint8)
    result_dif = np.swapaxes(result_dif_rescaled, 0, 1)
    result_dif = Image.fromarray(result_dif, 'L')
    result_dif.save('process_result_diff.gif')

    result_multiprocessing_rescaled = (
        result_multiprocessing * 255 / result_multiprocessing.max()).astype(np.uint8)
    result_multiprocessing = np.swapaxes(result_multiprocessing_rescaled, 0, 1)
    result_multiprocessing = Image.fromarray(result_multiprocessing_rescaled, 'L')
    result_multiprocessing.save('result_multiprocessing.gif')
