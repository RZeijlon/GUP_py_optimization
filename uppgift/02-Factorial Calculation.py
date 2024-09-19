"""
Exercise 2: Factorial Calculation
Task: Convert the following code to use both 
multi-threading and multiprocessing, 
then compare the timing of each version.

"""

import time

def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

if __name__ == "__main__":
    start_time = time.time()
    result = factorial(5000)
    end_time = time.time()
    print(f"Factorial calculated.")
    print(f"Normal Execution Time: {end_time - start_time} seconds")
