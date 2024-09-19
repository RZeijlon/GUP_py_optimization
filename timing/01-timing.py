"""
script explain how e can use and measure timing into python code
"""
import time

def old_fashion(n)->list:
    i = 0
    result = list()
    while i< n:
        result.append(str(i))
        i +=1
    return result

def modern_function(n):
    return list(map(str,range(n)))

if __name__ == "__main__":
    n = 1_000_000
    # set time before running our code
    time_old_fashion_start = time.time()
    # run our code
    old_fashion(n)
    # get time once finished
    time_old_fashion_end = time.time()
    # print diff.
    print(f"Execution of old fashion = {time_old_fashion_end-time_old_fashion_start}")




