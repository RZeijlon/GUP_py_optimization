"""
Script that help us to build multi-process in python
"""
# import 
from multiprocessing import Process
from os import cpu_count
from datetime import datetime

#light function
def square_number(n):
    for i in range(n):
        i += i**2
    print(f"i = {i}")
    return i

if __name__ == "__main__":
    #square_number(5)
    # Take ts as time we start our program
    ts=datetime.now()
    print(f"Program start @ {ts}")
    # create my processes
    processes = list()
    # so we will use all cores into our processor
    number_process = cpu_count()
    print(f" You have {number_process} cpu count into your computer")
    print("--"*100)
    for _ in range(number_process):
        p = Process(target=square_number,args=(100,))
        processes.append(p)    
    # run and terminate these processes
    for p in processes:
        p.start()
        print(f" >> {datetime.now()} --- Process {p} started")
        p.join()
        if p.exitcode == 0 :
            print(f" ### {datetime.now()} ----- Process {p} terminated")
    
    print("[[[[[DONE]]]]] "*5)
    te = datetime.now()
    print(f"Program ends @ {te}")
    print(f"Total time for all processes = {te-ts}")
    print("--"*100)