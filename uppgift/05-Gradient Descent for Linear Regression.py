"""
Exercise 5: Gradient Descent for Linear Regression
Task: Convert the following linear 
regression code to use both multi-threading and multiprocessing, 
then compare the timing of each version.
"""

import numpy as np
import time

def gradient_descent(X, y, learning_rate=0.01, iterations=1000):
    m, n = X.shape
    theta = np.zeros(n)
    for _ in range(iterations):
        gradient = X.T @ (X @ theta - y) / m
        theta -= learning_rate * gradient
    return theta

if __name__ == "__main__":
    X = np.random.rand(100000, 3)
    y = np.random.rand(100000)
    
    start_time = time.time()
    theta = gradient_descent(X, y)
    end_time = time.time()
    print(f"Gradient Descent completed.")
    print(f"Normal Execution Time: {end_time - start_time} seconds")
