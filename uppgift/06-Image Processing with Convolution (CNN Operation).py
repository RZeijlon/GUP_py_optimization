"""
Exercise 3: Image Processing with Convolution (CNN Operation)
Task: Convert the following convolution operation to use both
 multi-threading and multiprocessing,
 then compare the timing of each version.
"""


import numpy as np
import time
from scipy.signal import convolve2d

def convolution(image, kernel):
    return convolve2d(image, kernel, mode='same')

if __name__ == "__main__":
    image = np.random.rand(1024, 1024)
    kernel = np.random.rand(3, 3)
    
    start_time = time.time()
    result = convolution(image, kernel)
    end_time = time.time()
    print(f"Convolution completed.")
    print(f"Normal Execution Time: {end_time - start_time} seconds")
