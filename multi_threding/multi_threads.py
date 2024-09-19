"""
Script that help us to build multi-process in python
"""
# import 
from threading import Thread
from os import cpu_count
from datetime import datetime

# light function
def square_number(n):
    for i in range(n):
        i += i**2
    print(f"i = {i}")
    return i

if __name__ == "__main__":
    ts = datetime.now()
    print(f" Program start @ {ts}")
    #create threads
    threads = list()
    number_process = cpu_count()
    print(f" You have {number_process} cpu count into your computer ")
    print("--"*100)
    for _ in range(number_process):
        t = Thread(target=square_number,args=(100,))
        threads.append(t)
    
    for t in threads:
        t.start()
        print(f" >> {datetime.now()} --- Thread {t} started")
        t.join()
        if not t.is_alive():
            print(f" ### {datetime.now()} ----- Thread {t} terminated")
    
    print("[[[[[DONE]]]]] "*5)
    te = datetime.now()
    print(f"Program ends @ {te}")
    print(f"Total time for all processes = {te-ts}")
    print("--"*100)


