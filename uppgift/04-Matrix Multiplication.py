"""
Exercise 4: Matrix Multiplication (A Common ML Operation)
Task: Convert the following matrix multiplication 
code to use both multi-threading and multiprocessing, 
then compare the timing of each version.
"""

import numpy as np
import time

def matrix_multiply(a, b):
    return np.dot(a, b)

if __name__ == "__main__":
    a = np.random.rand(1000, 1000)
    b = np.random.rand(1000, 1000)

    start_time = time.time()
    result = matrix_multiply(a, b)
    end_time = time.time()
    print(f"Matrix Multiplication completed.")
    print(f"Normal Execution Time: {end_time - start_time} seconds")
