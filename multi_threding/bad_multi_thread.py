"""
script that shows not best version of multi-threading
"""
# import
from pathlib import Path
import threading

# function that open our file account.txt
# and add 1 to the balance in it
def accumulate(thread_id):
    path = Path("account.txt")
    for _ in range(5):
        with path.open() as f:
            balance = int(f.read())
            print(f"id = {thread_id} Read {balance}")
            balance +=1

        with path.open(mode="w") as f:
            f.write(str(balance))
            print(f"id = {thread_id} Wrote {balance}")


if __name__ == "__main__":
    threads = list()
    for index in range(2):
        thread = threading.Thread(target=accumulate,args=(index,))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
